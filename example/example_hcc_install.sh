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

#metaimp path downloaded by user
metaIMP_path=/work/yaolab/shared/2021_milk_2017_metagenome/metaimp_tesing_github/metaIMP
#create user environment
export USER_ENV_NAME=YAOLAB_METAIMP_MIDAS_TESTING

##############################################################
#USER DOES NOT NEED TO CHANGE ANYTHING FROM HERE
##############################################################
module purge
#you may still have conda available in your cloud, double check
module load mamba
echo " Starting installation in $USER_ENV_NAME "
$metaIMP_path/install.sh

echo " Starting installation testing in $USER_ENV_NAME "
$metaIMP_path/install_test.sh

echo " All installations and dependency testing is complete. Please check log files for updates "


