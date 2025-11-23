#!/bin/bash

if [ -z "$1" ]; then
  echo "No model specified. Please provide a model as an argument."
  echo "Usage: $0 <model>"
  echo "Where <model> can be 'dall_e', 'stable_diffusion', or 'midjourney'"
  exit 1
fi

model=$1

conda activate bafis
export CUDA_VISIBLE_DEVICES=0,1
export HF_HOME=/data/hiwi/thomasklassert/huggingface/

echo "Environment variables set:"
echo "CUDA_VISIBLE_DEVICES=$CUDA_VISIBLE_DEVICES"
echo "HF_HOME=$HF_HOME"

python "${model}.py"
python "${model}.py" --language "english"
python "${model}.py" --data "bafis"
python "${model}.py" --data "bafis" --language "english"
echo "Completed generating dataset for ${model}."