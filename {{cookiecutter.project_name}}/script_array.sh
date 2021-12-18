#!/bin/bash
# Lines starting with #SBATCH allow you to specify job parameters.
# For details, see https://docs.gwdg.de/doku.php?id=en:services:application_services:high_performance_computing:running_jobs_slurm
#SBATCH -C scratch2  # require access to the scratch folder (DO NOT CHANGE)
#SBATCH -n 1  # use 1 core per task
#SBATCH -t 1:00:00  # run time of 1 hour
#SBATCH --array=0-8  # how many tasks in the array


# Init conda
module load anaconda3
source $ANACONDA3_ROOT/etc/profile.d/conda.sh

# If you have your own version of miniconda installed on the cluster
# replace the above to lines with this:
# source /usr/users/$CLUSTER_USER/miniconda3/etc/profile.d/conda.sh

# Activate the conda environment
conda activate $CONDA_ENV_NAME
# Change to the directory with your scripts and data
cd /scratch/$CLUSTER_USER/$CLUSTER_FOLDER


# CHANGE THIS TO YOUR LIKING
# Currently, this runs script.py
python3 script_array.py
