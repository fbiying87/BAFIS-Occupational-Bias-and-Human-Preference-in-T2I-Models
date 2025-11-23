#!/usr/bin/env python3

import logging
import os
import argparse
import time

from midjourney_api import MidjourneyAPI
from utils import load_dataset

logging.basicConfig(
    filename="../logs/midjourney.log",
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def generate_images(dataset_map, model_name, image_dir, language, num_images):
    """
    Generate images for each prompt in the dataset using the specified model, language, and number of images and save
    them to the image directory.

    Args:
    dataset_map (dict): A dictionary with keys as filenames and values as pandas DataFrames.

    model_name (str): The name of the model to use for image generation.

    image_dir (str): The directory to save the images to.

    language (str): The language to prompt in. Can be "english" or "german", except for the splits "direct_feminine"
    and "german_gender_star", which are only available in German.

    num_images (int): The number of images to generate per prompt.
    """
    # Map language to column name in the dataset
    lang = "de" if language == "german" else "en"

    # Initialize the API
    api = MidjourneyAPI()

    for file, data in dataset_map.items():
        split = file.split(".")[0]

        occupations = data['occupation']

        if lang not in data:
            logger.error(f"Language {lang} not found in {file}")
            continue
        prompts = data[lang]

        for occ, prompt in zip(occupations, prompts):
            response = api.imagine(prompt)
            if response is None:
                logger.error(f"Failed to generate image for {occ}")
                continue
            time.sleep(50)

            try:
                api.upscale_images(num_images)
            except Exception as e:
                logger.error(f"Failed to upscale images for {occ}: {str(e)}")
                continue
            time.sleep(2)

            # Create a directory for the generated images
            path = os.path.join(os.curdir, image_dir, occ, model_name, split, lang)
            if not os.path.exists(path):
                os.makedirs(path)

            download_path = str(os.path.join(image_dir, occ, model_name, split, lang))
            try:
                api.download_images(download_path)
            except Exception as e:
                logger.error(f"Failed to download images for {occ}: {str(e)}")
                continue
            time.sleep(2)


def main(args):
    data = load_dataset(args.data, args.split, args.test, args.seed)

    # Pretty print the data frame
    for file, df in data.items():
        print(f"\nData from {file}:")
        print(df.head())

    generate_images(data, args.model, args.dest, args.language, args.num_images)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate images using Midjourney v6.1.')
    parser.add_argument('--model', default='midjourney-v6-1', type=str,
                        help='Which model to evaluate')
    parser.add_argument('--data', default='magbig', type=str,
                        help='Which dataset to use')
    parser.add_argument('--split', default=None, type=str,
                        help='Which split of the dataset to use')
    parser.add_argument('--language', default='german', type=str,
                        choices=['english', 'german'],
                        help='What languages to prompt in')
    parser.add_argument('--num_images', default=4, type=int,
                        help='How many images to generate per prompt')
    parser.add_argument('--dest', default="../images", type=str,
                        help='What folder to save images in')
    parser.add_argument('--test', default=False, type=bool,
                        help='Whether to test the dataset or not')
    parser.add_argument('--seed', default=42, type=int,
                        help='Random seed for reproducibility')

    arguments = parser.parse_args()
    main(arguments)
