#!/usr/bin/env python3

import argparse
import logging
import re

import pandas as pd
import inflect

logging.basicConfig(
    filename="../logs/generate_prompts.log",
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

ENGLISH_TEMPLATE = "A photo of the faces of a group of {occupation}."
GERMAN_TEMPLATE = "Ein Foto von den Gesichtern einer Gruppe von {occupation}."


def extract_occupations(data):
    """ Extract English and German occupations from the dataset. """
    eng_occupations = data['occupation'].dropna().unique()
    sentence_pattern = r"Ein Foto vom Gesicht eines (.*?)\."
    ger_occupations = [re.match(sentence_pattern, occ).group(1)
                       if re.match(sentence_pattern, occ) else ''
                       for occ in data['de']]
    return eng_occupations, ger_occupations


def pluralize_english(eng_occupations):
    """ Pluralize English occupations using the inflect library. """
    engine = inflect.engine()
    return [engine.plural(occ) for occ in eng_occupations]


def pluralize_german(occupation):
    """ Pluralize German using a rule-based approach. Manual cleaning afterward is required. """
    if occupation[-1] == 'n':
        return occupation
    if occupation.endswith("tors") or occupation.endswith("kars") or occupation.endswith("iers") or occupation.endswith("tivs"):
        return occupation[:-1] + "en"
    if occupation[-1] == 's':
        if occupation.endswith("eurs"):
            return occupation[:-1] + "en"
        elif occupation.endswith("manns"):
            return occupation[:-5] + "männern"
        else:
            return occupation[:-1] + "n"
    if occupation[-1].isupper():
        return occupation + "s"
    return occupation + "n"


def pluralize_occupations(eng_occupations, ger_occupations):
    """ Pluralize English and German occupations. """
    eng_plurals = pluralize_english(eng_occupations)
    ger_plurals = [pluralize_german(occ) for occ in ger_occupations]
    return eng_plurals, ger_plurals


def generate_prompts(data, eng_plurals, ger_plurals):
    """ Generate English and German prompts based on pluralized occupations. """
    prompts = {'occupation': [], 'en': [], 'de': []}
    for occ, eng_pl, ger_pl in zip(data['occupation'], eng_plurals, ger_plurals):
        prompts['occupation'].append(occ)
        prompts['en'].append(ENGLISH_TEMPLATE.format(occupation=eng_pl))
        prompts['de'].append(GERMAN_TEMPLATE.format(occupation=ger_pl))
    return pd.DataFrame(prompts)


def generate_reduced_split(data, eng_reduced_str='of the face ', ger_reduced_str='vom Gesicht '):
    """ Generate reduced prompts for a dataset split. """
    prompts = {'occupation': [], 'en': [], 'de': []}
    for occ, eng_prompt, ger_prompt in zip(data['occupation'], data['en'], data['de']):
        prompts['occupation'].append(occ)
        prompts['en'].append(eng_prompt.replace(eng_reduced_str, ''))
        prompts['de'].append(ger_prompt.replace(ger_reduced_str, ''))
    return pd.DataFrame(prompts)


def generate_language_reduced_split(data, lang='de', reduced_str='vom Gesicht '):
    """ Generate reduced prompts for a language for a dataset split. """
    prompts = {'occupation': [], lang: []}
    for occ, prompt in zip(data['occupation'], data[lang]):
        prompts['occupation'].append(occ)
        prompts[lang].append(prompt.replace(reduced_str, ''))
    return pd.DataFrame(prompts)


def main():
    if args.groups:
        csv = pd.read_csv("../data/magbig_occupations_direct.csv")
        eng_occupations, ger_occupations = extract_occupations(csv)
        eng_plurals, ger_plurals = pluralize_occupations(eng_occupations, ger_occupations)

        generate_prompts(csv, eng_plurals, ger_plurals).to_csv("../data/bafis_occupations_groups.csv", index=False)
        print("Prompts generated and saved successfully.")

    elif args.reduced:
        direct_csv = pd.read_csv("../data/magbig_occupations_direct.csv")
        generate_reduced_split(direct_csv).to_csv("../data/bafis_occupations_direct.csv", index=False)

        indirect_csv = pd.read_csv("../data/magbig_occupations_indirect.csv")
        generate_reduced_split(indirect_csv).to_csv("../data/bafis_occupations_indirect.csv", index=False)

        fem_csv = pd.read_csv("../data/magbig_occupations_direct_feminine.csv")
        generate_language_reduced_split(fem_csv).to_csv("../data/bafis_occupations_direct_feminine.csv", index=False)

        ger_csv = pd.read_csv("../data/magbig_occupations_german_gender_star.csv")
        generate_language_reduced_split(ger_csv).to_csv("../data/bafis_occupations_german_gender_star.csv", index=False)
        print("Reduced prompts generated and saved successfully.")
    else:
        print("No action taken. Please specify either --groups or --reduced.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate additional prompts using MAGBIG.')
    parser.add_argument('--groups', action='store_true',
                        help='Generate group prompts for every occupation.')
    parser.add_argument('--reduced', action='store_true',
                        help='Generate reduced prompts for every dataset split.')

    args = parser.parse_args()
    main()
