#!/bin/bash

#SBATCH --job-name=test_rolr
#SBATCH --output=log_test_rolr_%a.log
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=32GB
#SBATCH --time=1-00:00:00
# #SBATCH --gres=gpu:1

source activate goldmine
cd /scratch/jb6504/goldmine/goldmine

./test.py lotkavolterra rolr -i ${SLURM_ARRAY_TASK_ID} --samplesize 1000 --ratiogrid --score --testsample test_focus --modellabel model_focus
./test.py lotkavolterra rolr -i ${SLURM_ARRAY_TASK_ID} --samplesize 2000 --ratiogrid --score --testsample test_focus --modellabel model_focus
./test.py lotkavolterra rolr -i ${SLURM_ARRAY_TASK_ID} --samplesize 5000 --ratiogrid --score --testsample test_focus --modellabel model_focus
./test.py lotkavolterra rolr -i ${SLURM_ARRAY_TASK_ID} --samplesize 10000 --ratiogrid --score --testsample test_focus --modellabel model_focus
./test.py lotkavolterra rolr -i ${SLURM_ARRAY_TASK_ID} --samplesize 20000 --ratiogrid --score --testsample test_focus --modellabel model_focus
./test.py lotkavolterra rolr -i ${SLURM_ARRAY_TASK_ID} --samplesize 50000 --ratiogrid --score --testsample test_focus --modellabel model_focus
./test.py lotkavolterra rolr -i ${SLURM_ARRAY_TASK_ID} --samplesize 100000 --ratiogrid --score --testsample test_focus --modellabel model_focus
./test.py lotkavolterra rolr -i ${SLURM_ARRAY_TASK_ID} --samplesize 200000 --ratiogrid --score --testsample test_focus --modellabel model_focus