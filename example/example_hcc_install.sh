#!/bin/bash
#SBATCH --job-name=HCC_ENV_INSTALL
#SBATCH --nodes=1
#SBATCH --time=2:00:00
#SBATCH --mem=4gb
#SBATCH --output=HCC_ENV_INSTALL.%J.out
#SBATCH --error=HCC_ENV_INSTALL.%J.err


#All the dependencies are installed in custom user environment
#This script is an example of how to install dependencies on HCC cluster
#This script is an example of testing the installed dependencies

metaIMP_path=/home/yaolab/ksahu2/.ssh/metaIMP
export USER_ENV_NAME=metaimp_env

module purge
#you may still have conda available in your cloud, double check
module load mamba
echo " Starting installation in $USER_ENV_NAME "
$metaIMP_path/install.sh

echo " Starting installation testing in $USER_ENV_NAME "
$metaIMP_path/install_test.sh

echo " All installations and dependency testing is complete. Please check log files for updates "


