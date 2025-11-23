import argparse
import os
from PIL import Image


def compress_images_to_webp(source_dir, target_dir):
    """
    Compress all images in the source directory to webp format
    and recreate the directory structure in the target directory.

    Args:
        source_dir(str): The directory containing the images to convert.
        target_dir(str): The directory where the converted images will be saved.
    """
    for root, _, files in os.walk(source_dir):
        relative_path = os.path.relpath(root, source_dir)
        target_path = os.path.join(target_dir, relative_path)
        os.makedirs(target_path, exist_ok=True)

        for file in files:
            if file.lower().endswith('.png'):
                source_file_path = os.path.join(root, file)
                target_file_path = os.path.join(target_path, os.path.splitext(file)[0] + '.webp')

                with Image.open(source_file_path) as img:
                    img.save(target_file_path, 'WEBP')


def compress_images_to_thumbnail(source_dir, target_dir):
    """
    Compress all images in the source directory to a thumbnail of 128x128 pixels
    and recreate the directory structure in the target directory.

    Args:
        source_dir(str): The directory containing the images to convert.
        target_dir(str): The directory where the converted images will be saved.
    """
    for root, _, files in os.walk(source_dir):
        relative_path = os.path.relpath(root, source_dir)
        target_path = os.path.join(target_dir, relative_path)
        os.makedirs(target_path, exist_ok=True)

        for file in files:
            if file.lower().endswith('.png'):
                source_file_path = os.path.join(root, file)
                target_file_path = os.path.join(target_path, os.path.splitext(file)[0] + '.png')

                with Image.open(source_file_path) as img:
                    img.thumbnail((128, 128))
                    img.save(target_file_path, 'PNG')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Compress image dataset')
    parser.add_argument('--source_directory', default='../images', type=str,
                        help='Path to the directory containing the images to compress')
    parser.add_argument('--target_directory', default='../images_thumbnail', type=str,
                        help='Path to the directory where the compressed images will be saved')

    args = parser.parse_args()

    compress_images_to_thumbnail(args.source_directory, args.target_directory)
    print("Compression complete.")
