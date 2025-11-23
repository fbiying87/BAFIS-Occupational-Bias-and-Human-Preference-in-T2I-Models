#!/usr/bin/env python3

import logging
import os
import argparse
import time

import backoff
import openai
from openai import RateLimitError

from utils import load_dataset, save_image_from_url
from dotenv import load_dotenv

logging.basicConfig(
    filename="../logs/dall_e.log",
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Set up OpenAI client
client = openai.OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    organization="org-NA9PZJdlAiXYeOoOxP0rZ2s5",
)


@backoff.on_exception(backoff.expo, RateLimitError)
def generate_image(prompt, model_name):
    """
    Generate an image using OpenAIs API with the specified model and prompt.
    This function uses exponential backoff to handle rate limit errors.

    Args:
    prompt (str): The prompt to generate an image for.

    model_name (str): The name of the model to use for image generation.

    Returns:
    response: The response from the OpenAI API.
    """
    return client.images.generate(
        prompt=prompt,
        model=model_name,
        n=1,
        quality="standard",
        response_format="url",
        size="1024x1024",
        style="natural",
    )


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

    for file, data in dataset_map.items():
        split = file.split(".")[0]

        occupations = data['occupation']

        if lang not in data:
            logger.error(f"Language {lang} not found in {file}")
            continue
        prompts = data[lang]

        for occ, prompt in zip(occupations, prompts):
            for i in range(num_images):
                try:
                    response = generate_image(prompt, model_name)
                    logger.info(f"Response for prompt {prompt}: {response.data[0]}")

                    image_url = response.data[0].url

                    # Create a name for the generated image based on the prompt
                    image_name = prompt.replace(" ", "_").replace(",", "").replace(".", "") + ".png"

                    # Create a directory for the generated image
                    path = os.path.join(os.curdir, image_dir, occ, model_name, split, lang)
                    if not os.path.exists(path):
                        os.makedirs(path)

                    image_path = os.path.join(path, image_name)
                    if os.path.exists(image_path):
                        image_path = os.path.join(path, image_name.replace(".png", f"_{int(time.time())}.png"))

                    save_image_from_url(image_url, image_path)

                except openai.OpenAIError as e:
                    logger.error(f"An error occurred with prompt {prompt}: {str(e)}")


def main(args):
    data = load_dataset(args.data, args.split, args.test, args.seed)

    # Pretty print the data frame
    for file, df in data.items():
        print(f"\nData from {file}:")
        print(df.head())

    generate_images(data, args.model, args.dest, args.language, args.num_images)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate images using DALL-E.')
    parser.add_argument('--model', default='dall-e-3', type=str,
                        help='which model to evaluate')
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
