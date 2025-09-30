#!/bin/bash
#SBATCH --job-name=touch
#SBATCH --nodes=1
#SBATCH --time=24:00:00
#SBATCH --mem=10gb
#SBATCH --ntasks-per-node=8
#SBATCH --output=touch.%J.out
#SBATCH --error=touch.%J.err
#SBATCH --partition=yaolab,batch,guest



#folder=/work/yaolab/shared/2025_01_infant/
folder=/work/yaolab/shared/2025_04_complex_infant_fecal/
cd $folder

find . \( -type f -o -type d \) -exec touch {} +

echo "find . -type f -exec touch {} +"
