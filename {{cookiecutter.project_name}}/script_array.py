import pandas as pd
import numpy as np
import colorcet as cc
import xarray
import time
import os
import itertools

# make a bunch of parameters - one for each task_id
# since script_array.sh runs a task with 9 jobs, we can run a 3x3 parameter grid search
param1 = [1, 2, 3]
param2 = [100, 200, 300]
# create parameter combinations
params = list(itertools.product(param1, param2))
print(f"The array jobs will use these parameters:")
print(params)

# get the task_id
task_id = os.environ['SLURM_ARRAY_TASK_ID']
print(f"Running array job #{task_id}.")

# use the task_id as an index into params
# task id is a string, so we need to cast it to int
task_params = params[int(task_id)]

print(f"Using parameters: {task_params}.")
print(f'Saving to "res/results_{task_id}.txt"')
np.savetxt(f'res/results_{task_id}.txt', task_params)
