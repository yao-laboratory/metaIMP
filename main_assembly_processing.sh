#!/bin/bash
#SBATCH --job-name=assembly
#SBATCH --nodes=1
#SBATCH --time=24:00:00
#SBATCH --mem=48gb
#SBATCH --output=assembly.%J.out
#SBATCH --error=assembly%J.err


A=/work/yaolab/shared/2021_milk_2017_metagenome/MIT_DATA/sample_SRR9205533/SRR9205533_1.fastq.filtered_1.fastq
B=/work/yaolab/shared/2021_milk_2017_metagenome/MIT_DATA/sample_SRR9205533/SRR9205533_2.fastq.filtered_2.fastq
C=/work/yaolab/shared/2021_milk_2017_metagenome/MIT_DATA/sample_SRR9205533/error_corrected/
t=8
D=1000
/home/yaolab/ksahu2/.ssh/metaIMP/assembly_binning.sh $A $B $C $t $D
