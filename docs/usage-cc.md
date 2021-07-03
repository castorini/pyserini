# Computer Canada (CC) Supplemental Instructions for Dense Retrieval

### Get started

For general CC setup, please refer to [this link](https://github.com/castorini/onboarding/edit/master/docs/cc-guide.md).

### Submitting jobs through SLURM using the interactive way

For dense retrieval, once you have `ssh`ed to the cc server (currently at the login node). To get into a compute node, the interactive way (get a shell) is using
the following command (make sure you have specified which resource account (jimmy's) to charge for your job, instructions are provided in [this link](https://github.com/castorini/onboarding/blob/master/docs/cc-guide.md#submitting-jobs-through-slurm)):

 `srun --mem=128G --cpus-per-task=32 --time=24:0:0 --pty zsh`
 
Change `zsh` to `bash` if you prefer bash and add this argument `--gres=gpu:<device_name>:<number_of_devices>` if you need a GPU where `<device_name>` can be `v100l`
for example. Please adjust numbers in the argument accordingly to your usage.

Once you are in a compute node (the above waiting process usually takes some time), use `squeue -u <your_user_name>` to check your status. Make sure you have cleared the `PYTHON_PATH` environment variable `export PYTHON_PATH=`

Refer to [this link](https://github.com/castorini/onboarding/blob/master/docs/cc-guide.md#create-a-virtual-environment) to create a conda environment. Once you have created
a new environment in Conda, install all packages you need using conda-forge repo: `conda install -c conda-forge <package_name>`. If you get `ImportError:C extension: /lib64/libc.so.6`, please install the 
package again using the previous command.

Before you run any pyserini dense retrieval task, please make sure you have installed the newest pyserini (`pip install .` in the root directory of pyserini)

If you have any question using CC on dense retrieval, please feel free to msg me (Arthur Chen@Slack) or check CC documentation
