from fabric.api import run, local, env
import os
import yaml
from pprint import pprint

print('Loading config from `config.yaml`')
with open('config.yaml', 'r') as f:
    env_vars = yaml.load(f, Loader=yaml.SafeLoader)
pprint(env_vars)

full_path = os.path.dirname(os.path.abspath(__file__))
LOCAL_FOLDER = os.path.split(full_path)[-1]
print(f'Local folder name is "{LOCAL_FOLDER}".')


if 'CLUSTER_USER' in env_vars:
    USER = env_vars['CLUSTER_USER']
else:
    USER = os.environ['USER']

env.hosts = [f"{USER}@gwdu103.gwdg.de"]
FOLDER = f"/scratch/{USER}/{LOCAL_FOLDER}"
REMOTE = "{0}@gwdu103.gwdg.de:" + FOLDER
LOCAL = './'


def _rsync(source, target, delete=False, excludes=[], fix_perms=False):
    RSYNC = 'rsync -rvltHhz --update --progress'
    if delete:  # delete files on target
        RSYNC += ' --delete'

    if fix_perms:  # set perms to read and write (and execute?) for all
        RSYNC += ' --no-p --no-g --chmod=ugo=rwX'

    for exclude in excludes:  # exclude files/directories
        RSYNC += ' --exclude="{0}"'.format(exclude)

    RSYNC += " {0} {1}".format(source, target)
    local(RSYNC)


def push(delete=False, excludes=['fig', 'res', '.*'], fix_perms=True):
    _rsync(LOCAL, REMOTE.format(USER), delete, excludes, fix_perms)


def pull(delete=False, excludes=['dat*'], fix_perms=True):
    _rsync(REMOTE.format(USER), '../', delete, excludes, fix_perms)


def make_env_cluster(env_file="env.yaml", env_name=None):
    if env_name is None:
        env_name = env_vars['CONDA_ENV_NAME']

    run(f"""umask g+rwx; module load anaconda3;
            source $ANACONDA3_ROOT/etc/profile.d/conda.sh;
            cd {FOLDER};
            conda env create -f {env_file} -n {env_name}""")

def make_env_local(env_file="env.yaml", env_name=None):
    if env_name is None:
        env_name = env_vars['CONDA_ENV_NAME']

    run(f"""cd {FOLDER};
            conda env create -f {env_file} -n {env_name}""")


def init():
    print(f'Creating "{FOLDER}" on the cluster, with sub directories "res", "log", and "fig"')
    run(f"""umask g+rwx;
            mkdir {FOLDER};
            mkdir {FOLDER}/res;
            mkdir {FOLDER}/log;
            mkdir {FOLDER}/fig""")
    push()


def submit(script_name, env_name=None):
    """Submit script to cluster.

    Usage:
    `fab submit:script_name`
    """
    cmd = "umask g+rwx"

    # set env vars on cluster
    for key, val in env_vars.items():
        cmd += f'; export {key}={val}'
    cmd += f'; export CLUSTER_FOLDER={LOCAL_FOLDER}'

    if env_name is not None:
        cmd += f'; export CONDA_ENV_NAME={env_name}'
    # construct rest of the command
    cmd += f"; cd {FOLDER}; sbatch -o {FOLDER}/log/slurm-%j.out {FOLDER}/{script_name}"

    run(cmd)


def status():
    run(f'squeue -u {USER}')
