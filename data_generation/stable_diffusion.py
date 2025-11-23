#!/usr/bin/env python3

import logging
import os
import argparse

import torch
from diffusers import StableDiffusion3Pipeline
from utils import load_dataset

logging.basicConfig(
    filename="../logs/stable-diffusion-3-medium.log",
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def generate_images(dataset_map, model, image_dir, language, num_images):
    """
    Generate images for each prompt in the dataset using the specified model, language, and number of images and save
    them to the image directory.

    Args:
    dataset_map (dict): A dictionary with keys as filenames and values as pandas DataFrames.

    model (StableDiffusion3Pipeline): The model to use for image generation.

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
            try:
                images = model(
                    prompt=prompt,
                    num_inference_steps=50,
                    height=1024,
                    width=1024,
                    guidance_scale=7.0,
                    num_images_per_prompt=num_images
                ).images

                # Create a name for the generated image based on the prompt
                base_name = prompt.replace(" ", "_").replace(",", "").replace(".", "") + ".png"

                # Create a directory for the generated image
                path = os.path.join(os.curdir, image_dir, occ, 'stable-diffusion-3', split, lang)
                if not os.path.exists(path):
                    os.makedirs(path)

                for i, image in enumerate(images):
                    # Create a unique name for each image
                    image_name = base_name.replace(".png", f"_{i + 1}.png")
                    image_path = os.path.join(path, image_name)

                    image.save(image_path)

            except Exception as e:
                logger.error(f"An error occurred with prompt {prompt}: {str(e)}")


def main(args):
    # Load the Stable Diffusion model
    pipe = StableDiffusion3Pipeline.from_pretrained("stabilityai/stable-diffusion-3-medium-diffusers",
                                                    torch_dtype=torch.float16)
    # set the device to train on (run export CUDA_VISIBLE_DEVICES beforehand)
    device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
    pipe.to(device)
    logger.info(f"Running on device: {device}")

    data = load_dataset(args.data, args.split, args.test, args.seed)

    # Pretty print the data frame
    for file, df in data.items():
        print(f"\nData from {file}:")
        print(df.head())

    generate_images(data, pipe, args.dest, args.language, args.num_images)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate images using Stable Diffusion 3 Medium.')
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
