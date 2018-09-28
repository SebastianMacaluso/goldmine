#!/bin/bash

#SBATCH --job-name=train_scandalcv
#SBATCH --output=train_scandalcv_%a.log
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=32GB
#SBATCH --time=7-00:00:00
#SBATCH --gres=gpu:1

source activate goldmine
cd /scratch/jb6504/goldmine/goldmine

./train.py lotkavolterra scandalcv -i ${SLURM_ARRAY_TASK_ID} --samplesize 1000 --alpha 0.01 --trainsample train_focus --modellabel model_focus --debug
./train.py lotkavolterra scandalcv -i ${SLURM_ARRAY_TASK_ID} --samplesize 2000 --alpha 0.01 --trainsample train_focus --modellabel model_focus --debug
./train.py lotkavolterra scandalcv -i ${SLURM_ARRAY_TASK_ID} --samplesize 5000 --alpha 0.01 --trainsample train_focus --modellabel model_focus --debug
./train.py lotkavolterra scandalcv -i ${SLURM_ARRAY_TASK_ID} --samplesize 10000 --alpha 0.01 --trainsample train_focus --modellabel model_focus --debug
./train.py lotkavolterra scandalcv -i ${SLURM_ARRAY_TASK_ID} --samplesize 20000 --alpha 0.01 --trainsample train_focus --modellabel model_focus --debug
./train.py lotkavolterra scandalcv -i ${SLURM_ARRAY_TASK_ID} --samplesize 50000 --alpha 0.01 --trainsample train_focus --modellabel model_focus --debug
./train.py lotkavolterra scandalcv -i ${SLURM_ARRAY_TASK_ID} --samplesize 100000 --alpha 0.01 --trainsample train_focus --modellabel model_focus --debug
./train.py lotkavolterra scandalcv -i ${SLURM_ARRAY_TASK_ID} --samplesize 200000 --alpha 0.01 --trainsample train_focus --modellabel model_focus --debug