#!/bin/bash
#SBATCH -J norta_14
#SBATCH -o norta_14.out
#SBATCH -e norta_14.err
#SBATCH -p normal
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -t 46:30:00
#SBATCH --mail-user=ashutosh.shukla@utexas.edu
#SBATCH --mail-type=all
#SBATCH -A Extreme-Weather-Even

# setup
# module load python3/3.7.0

# enter the repo directory
cd /home1/07346/ashukla/Norta/TwoStageModel/

# run the python script
python3 stochastic_run.py --scenario_id 14
