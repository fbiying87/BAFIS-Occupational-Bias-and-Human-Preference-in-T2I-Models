import argparse
import os
import json
import shutil
from pathlib import Path
import pandas as pd


def enumerate_dataset(source_dir, target_dir, metadata_file='metadata.json'):
    """
    Enumerate all images in the source directory, extract their metadata and save them to the target directory.

    Args:
        source_dir (str): The directory containing the images to convert.
        target_dir (str): The directory where the converted images will be saved.
        metadata_file (str): Name of the JSON file to store metadata.
    """
    os.makedirs(target_dir, exist_ok=True)
    image_counter = 0
    metadata_dict = {}

    for root, _, files in os.walk(source_dir):
        png_files = sorted([f for f in files if f.lower().endswith('.png')])

        for file in png_files:
            source_file = os.path.join(root, file)

            path_parts = Path(os.path.relpath(root, source_dir)).parts

            if len(path_parts) < 4:
                continue

            metadata = {
                'occupation': path_parts[0],
                'model': path_parts[1],
                'prompt_group': path_parts[2],
                'language': path_parts[3]
            }

            new_filename = f"{image_counter}.png"
            target_file = os.path.join(target_dir, new_filename)
            shutil.copy2(source_file, target_file)

            metadata_dict[str(image_counter)] = metadata
            image_counter += 1

    metadata_path = os.path.join(target_dir, metadata_file)
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(metadata_dict, f, indent=2, ensure_ascii=False)

    print(f"Processed {image_counter} images")
    print(f"Metadata saved to {metadata_path}")


def add_prompt_to_metadata(metadata_file='metadata.json'):
    """
    Add prompt to metadata.

    Args:
        metadata_file (str): Name of the JSON file to store metadata.
    """
    with open(metadata_file, 'r', encoding='utf-8') as f:
        metadata_dict = json.load(f)

    for key in metadata_dict:
        # Look up the prompt for each image
        if metadata_dict[key]['prompt_group'] == 'bafis_occupations_groups':
            df = pd.read_csv('../data/bafis_occupations_groups.csv')
            row = df.loc[df['occupation'] == metadata_dict[key]['occupation']]
            prompt = row[metadata_dict[key]['language']].values[0]
        elif metadata_dict[key]['prompt_group'] == 'magbig_occupations_direct':
            df = pd.read_csv('../data/magbig_occupations_direct.csv')
            row = df.loc[df['occupation'] == metadata_dict[key]['occupation']]
            prompt = row[metadata_dict[key]['language']].values[0]
        elif metadata_dict[key]['prompt_group'] == 'magbig_occupations_direct_feminine':
            df = pd.read_csv('../data/magbig_occupations_direct_feminine.csv')
            row = df.loc[df['occupation'] == metadata_dict[key]['occupation']]
            prompt = row[metadata_dict[key]['language']].values[0]
        elif metadata_dict[key]['prompt_group'] == 'magbig_occupations_indirect':
            df = pd.read_csv('../data/magbig_occupations_indirect.csv')
            row = df.loc[df['occupation'] == metadata_dict[key]['occupation']]
            prompt = row[metadata_dict[key]['language']].values[0]
        else :
            prompt = None

        metadata_dict[key]['prompt'] = prompt

    with open(metadata_file, 'w', encoding='utf-8') as f:
        json.dump(metadata_dict, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Enumerate images in a directory and save their metadata to a JSON file.')
    parser.add_argument('--source_directory', default='../images', type=str,
                        help='Path to the directory containing the images')
    parser.add_argument('--target_directory', default='../images_dataset', type=str,
                        help='Path to the directory where the converted images will be saved')

    args = parser.parse_args()

    enumerate_dataset(args.source_directory, args.target_directory)
    add_prompt_to_metadata(metadata_file=os.path.join(args.target_directory, 'metadata.json'))
    print("Enumeration complete.")
