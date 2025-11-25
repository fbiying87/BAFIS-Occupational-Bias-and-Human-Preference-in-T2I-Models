# BAFIS-Occupational-Bias-in-T2I-Models
BAFIS: Dataset + Framework to assess occupational Bias and Human Preference in modern Text-to-image Models

Thomas Klassert, Adrian Ulges, and Biying Fu

Code in this repo is developed by Thomas Klassert.
More details will follow soon...

## Note
This is the official repository of the paper: BAFIS: Dataset + Framework to assess occupational Bias and Human Preference in modern Text-to-image Models. The paper can be found in [here]().

## Scope:
In this repo, you can find the link to dataset with images generated in the publication.

You will also find code to generate a novel set of images on your own.

## Examples of generated images
![overview](bafis_banner.jpg)

## Dataset
Dataset can be downloaded from this page: https://zenodo.org/records/14025071 
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


### Dataset Generation
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

### Folder Structure

```
├── project                         project folder
│   ├── data_generation             scripts for dataset generation using our different models
│   ├── data                        data folder including MAGBIG prompts
├── bafis_banner.jpg                demo image
├── .gitignore                      gitignore
└── README.md                       README
```


## Citation
if you use the data in this repository, please cite the following paper:
```
@misc{klassert2024,
      title={BAFIS: Dataset + Framework to assess occupational Bias and Human Preference in modern Text-to-image Models}, 
      author={Thomas Klassert, Adrian Ulges, and Biying Fu},
      year={2025},
      eprint={},
      archivePrefix={arXiv},
      primaryClass={cs.CV}
}
```

## License
This project is licensed under the terms of the Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0) license. Copyright (c) 2021 RheinMain Universtiy for Applied Sciences, Wiesbaden, Germany
