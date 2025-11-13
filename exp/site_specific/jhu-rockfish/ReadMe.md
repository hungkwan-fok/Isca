
# Instructions for running Isca on JHU Rockfish

These instructions are intended to get you up-and-running with a simple Held-Suarez test case. They assume you are starting with a default user environment on Rockfish, so some changes might be needed if you have already modified your environment. 

This is assuming that you have already downloaded Isca on Rockfish. Before you can run Isca, you'll need to set up a conda enviroment for Isca (this means it will have all the right versions of the various packages on which it depends). 

First, load anaconda 
```{bash}
module load anaconda
```

Then, create the conda environment with the required packages

```{bash}
conda create -n isca_env python ipython
conda activate isca_env
cd Isca/src/extra/python
pip install -r requirements.txt
```

Install Isca
```
pip install -e .
```

You should see a message
```
Successfully installed Isca
```

Finally, we'll need to update the `~/.bashrc` file. Add the following lines (change the directories to fit your preference and configuration):

```{bash}
# directory of the Isca source code
export GFDL_BASE=scatch16/$USER/Isca
# "environment" configuration for bc4
export GFDL_ENV=jhu-rockfish
# temporary working directory used in running the model
export GFDL_WORK=/scratch16/$USER/Isca_work
# directory for storing model output
export GFDL_DATA=/scratch16/$USER/Isca_out
```

Make the relevant directories if you haven't already.

Now everything should be set up and we can try a test run. The following should compile and run 12 months of a Held-Suarez test case, at T42 resolution spread over 16 cores. 

```{bash}
cd Isca/exp/site-specific/jhu-rockfish
sbatch isca_slurm_job.sh
```

This should produce a slurm file showing the progress as it compiles and runs. All being well, after about 20 minutes the job should complete.