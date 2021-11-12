# {{cookiecutter.project_name}}

## Local set up:
- Edit `env.yaml` to contain the packages your job needs.
- Initialize the project `fab init` - this will run a command on the cluster that creates all the necessary folders. This will also push all files to the cluster
- Make the environment locally: `fab make_env_local`
- Make the environment on the cluster: `fab make_env_cluster`
- _IMPORTANT_: If you have installed miniconda on the cluster yourself, you need to replace these lines in edit `script.sh`:

    ```sh
    module load anaconda3
    source $ANACONDA3_ROOT/etc/profile.d/conda.sh
    ```
with this line:

    ```sh
    source /usr/users/{{cookiecutter.cluster_user_name}}/miniconda3/etc/profile.d/conda.sh
    ```
This assumes that `miniconda3` is the location of the installation folder for miniconda in your home directory on the cluster. If not, change the folder name accordingly.


## Configure your scripts

### Individual jobs
- `script.sh` will activate the conda env and run `script.py` - edit both to your liking.
- Lines in `script.sh` starting with `#SBATCH` are used to configure the job - request GPUs, more memory, a specific run time. For details, see [HPC @ GWDG](https://docs.gwdg.de/doku.php?id=en:services:application_services:high_performance_computing:running_jobs_slurm).

### Array jobs
- This is great if you want to run the same job with different data files or run the same analysis with different parameter sets.
- Edit `script_array.sh`. This line `#SBATCH --array=0-8` will make your python script run 8 times. Each of the 8 jobs can be identified using a task id, which is available to each job via the environment variable `SLURM_ARRAY_TASK_ID`. You can access this variable in python via `task_id = os.environ['SLURM_ARRAY_TASK_ID']`. You can then use the `task_id` as an index into a list of files or a list of parameters. See `script_array.py` for an example. _Caution:_ `task_id` is a string variable and needs to be cast to an int to be used for indexing via `task_id = int(task_id)`.


## Run your job:
- Push all data to the cluster to make sure all files are there: `fab push`
- Submit the script: `fab submit:script.sh` or `fab submit:script_array.sh`
- You can check the status of the job: `fab status`
- Pull the jobs logs and results: `fab pull`
- In case things didn't work: Check the local `log` folder for error messages.

