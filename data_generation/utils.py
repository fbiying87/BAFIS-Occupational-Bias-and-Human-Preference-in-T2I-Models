import os
import pandas as pd
import requests


def load_dataset(dataset, split, test, seed):
    """
    Load the dataset.

    Args:
    dataset (str): The prefix of dataset files to be loaded (e.g. "magbig").

    split  (str): The split of the dataset to use. Can be "direct", "direct_feminine", "german_gender_star",
    "indirect" or "groups". If None, all splits are used.

    test (bool): Whether to test the dataset or not.

    seed (int): Random seed for reproducibility.

    Returns:
    dict: A dictionary with keys as filenames and values as pandas DataFrames.
    """
    data_folder = "../data"
    files = os.listdir(data_folder)
    dataset_map = {}

    if split:
        # Filter files that start with the dataset name and end with .csv and include the specified split
        filtered_files = [file for file in files if file.startswith(dataset) and file.endswith('.csv')
                          and split in file]
    else:
        # Filter files that start with the dataset name and end with .csv
        filtered_files = [file for file in files if file.startswith(dataset) and file.endswith('.csv')]

    for file in filtered_files:
        file_path = os.path.join(data_folder, file)
        try:
            data_frame = pd.read_csv(file_path)
            if test:
                # Sample 1% of the data for testing
                data_frame = data_frame.sample(frac=0.01, random_state=seed)
                dataset_map[file] = data_frame
            else:
                dataset_map[file] = data_frame
        except Exception as e:
            print(f"Error loading data from {file_path}: {e}")

    return dataset_map


def save_image_from_url(image_url, image_path):
    """
    Downloads and saves an image from a URL to a specified path.

    Args:
    image_url (str): The URL of the image to download.

    image_path (str): The path to save the image to.
    """
    try:
        response = requests.get(image_url)
        response.raise_for_status()
        with open(image_path, "wb") as f:
            f.write(response.content)
    except requests.RequestException as e:
        print(f"Error downloading image from {image_url}: {e}")