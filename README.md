# BAFIS: Dataset + Framework to assess occupational Bias and Human Preference in modern Text-to-image Models

![License CC](https://img.shields.io/badge/license-CC-green.svg?style=plastic)
![Format PNG](https://img.shields.io/badge/format-PNG-green.svg?style=plastic)
![Resolution 1024×1024](https://img.shields.io/badge/resolution-1024×1024-green.svg?style=plastic)
![Images 20000](https://img.shields.io/badge/images-20,000-green.svg?style=plastic)

![BAFIS overview image](/bafis_banner.jpg)

## Paper (coming soon)

This is the official repository of the paper: BAFIS: Dataset + Framework to assess occupational Bias and Human Preference in modern Text-to-image Models. The paper can be found [here]().

## Scope

In this repo, you can find the link to dataset with the generated images used in our user study.

You will also find code to generate a novel set of images on your own.

## Short Description

BAFIS is a research project that aims to investigate how language differences influence bias in modern Text-to-Image models such as _Stable Diffusion 3 Medium_, _FLUX.1-dev_,_Playground v2.5_, _Midjourney_ and _DALL-E 3_ and whether people can subjectively assess this bias.

As part of the project, we generated a dataset of synthetic images using the preceding models with multi-lingual text prompts from the [MAGBIG](https://huggingface.co/datasets/felfri/MAGBIG) dataset, which focuses on prompts for occupational portraits. The dataset is limited to images generated for the prompt languages _English_ and _German_.

Additionally we added group prompts (e.g. "A photo of the faces of a group of accountants.") to these prompts resulting in a combined number of _1057_ unique prompts. All prompt groups used in this project can be found in the folder [prompts](/prompts/).

For each prompt, we generated _4_ images using the models mentioned above resulting in a total of _21140_ high-quality PNG images at 1024×1024 resolution. These images serve as the basis for the evaluation by the participants of our user study.

The images are provided in the form of a _filtered_ dataset. The dataset has been filtered using [DeepFace](https://github.com/serengil/deepface) (with YOLOv8 as the detection backend) to exclude images that lack discernible faces.

### Dataset

The dataset is available via [Zenodo](https://zenodo.org/records/14025071).

### Metadata

Each version of the dataset includes a `metadata.json` file specifying image information in a machine-readable format:

```
{
  "0": {                                                            # Image index
    "occupation": "accountant",                                     # Occupation
    "model": "dall-e-3",                                            # Model used to generate the image
    "prompt_group": "bafis_occupations_groups",                     # Prompt group identifier
    "language": "en",                                               # Language of the prompt (en or de)
    "prompt": "A photo of the faces of a group of accountants.",    # Prompt
  },
  ...
}
```

### Dataset Generation

To generate the dataset on your own, you need to set up environment variables for the different models. Create a `.env` file with the following content:

```
# Dataset Generation
# DALL-E 3 Script
OPENAI_API_KEY=YOUR_OPENAI_API_KEY
# Midjourney Script
MIDJOURNEY_AUTH=YOUR_MIDJOURNEY_AUTH_TOKEN
MIDJOURNEY_APPLICATION_ID=YOUR_MIDJOURNEY_APPLICATION_ID
MIDJOURNEY_GUILD_ID=YOUR_MIDJOURNEY_GUILD_ID
MIDJOURNEY_CHANNEL_ID=YOUR_MIDJOURNEY_CHANNEL_ID
MIDJOURNEY_SESSION_ID=YOUR_MIDJOURNEY_SESSION_ID
MIDJOURNEY_DATA_VERSION=YOUR_MIDJOURNEY_DATA_VERSION
MIDJOURNEY_DATA_ID=YOUR_MIDJOURNEY_DATA_ID
```

To obtain the Midjourney environment variables, please complete the following steps:

1. Create a Midjourney account at [Midjourney](https://midjourney.com/)
2. With the same Discord account you used for your midjourney subscription, create a new server and add the midjourney bot to this server.
3. Navigate to your discord server, open your developer console and open the network tab.
4. Activate the midjourney bot with the slash command /imagine followed by a prompt, then click on the interactions option.
5. Navigate to the Headers tab and save your Authorization key. (=MIDJOURNEY_AUTH)
6. Navigate to the Payload window and save your application_id (=MIDJOURNEY_APPLICATION_ID), guild_id (=MIDJOURNEY_GUILD_ID), channel_id (=MIDJOURNEY_CHANNEL_ID), session_id (=MIDJOURNEY_SESSION_ID), and under data the version (=MIDJOURNEY_DATA_VERSION) and id (=MIDJOURNEY_DATA_ID)values from the JSON.

There are 5 scripts for dataset generation using different models:

- `data_generation/stable_diffusion.py` for Stable Diffusion 3 Medium
- `data_generation/playground.py` for Playground v2.5
- `data_generation/dall_e.py` for DALL-E 3
- `data_generation/flux.py` for Flux.1
- `data_generation/midjourney.py` for Midjourney

Before running the scripts you need prompt data in the `data` folder. In the repository, there is a `data` folder containing the MAGBIG prompts and BAFIS prompts. You can extend the dataset with your own prompts. All prompt files should be `.csv` files with the following keys:

```
occupation, en, de
```

To run the scripts, you may need to install different dependencies. Please reference the scripts imports directly for the required dependencies.
**Note:** To run the `flux.py` script, you need to install the `diffuers` package from [source](https://github.com/huggingface/diffusers).

## Folder Structure

```
├── project                         project folder
│   ├── data_generation             scripts for dataset generation using our different models
│   ├── prompts                     prompts for dataset generation in .csv format
├── bafis_banner.jpg                demo image
├── LICENSE.txt                     License
└── README.md                       README
```

## Citation (coming soon)

If you use the data in this repository, please cite our paper:

```
@misc{klassert2025,
      title={BAFIS: Dataset + Framework to assess occupational Bias and Human Preference in modern Text-to-image Models},
      author={Thomas Klassert, Adrian Ulges, and Biying Fu},
      year={2025},
      eprint={},
      archivePrefix={arXiv},
      primaryClass={cs.CV}
}
```

## License

This project is licensed under the CC BY 4.0 license. See the LICENSE file for more information. Copyright (c) 2025 RheinMain University for Applied Sciences, Wiesbaden, Germany
