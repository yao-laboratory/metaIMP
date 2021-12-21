#!/bin/bash
#SBATCH --job-name=main
#SBATCH --nodes=1
#SBATCH --time=24:00:00
#SBATCH --mem=96gb
#SBATCH --output=main.%J.out
#SBATCH --error=main.%J.err




#modules for assembly_binning.sh:

echo "loading modules for assembly_binning.sh"
module load spades/3.14
module load quast/5.0
module load bowtie/2.3
#module load bowtie/2.3
#module load samtools/1.9
module load samtools/1.9
module load metabat2/2.15
module load checkm-genome/1.1




#modules for assembly_contig_annotation.sh:
echo "loading modules for assembly_contig_annotation.sh"
module load eggnog-mapper/2.1



#modules for assembly_snp_annotation.sh:
echo " no need to load python module. exists in env "




#modules for assembly_snp_calling.sh:
module load instrain/1.3
export PYTHONNOUSERSITE=1

#env_var_func() {
#	echo "metaimp_env"
#}
#this was an attempt to use function. probably delete this. use simple names

export USER_ENV_NAME=metaimp_env

fastq1=/work/yaolab/shared/2021_milk_2017_metagenome/MIT_DATA/sample_SRR9205535/SRR9205535_1.fastq
fastq2=/work/yaolab/shared/2021_milk_2017_metagenome/MIT_DATA/sample_SRR9205535/SRR9205535_2.fastq
output_folder_assembly=/work/yaolab/shared/2021_milk_2017_metagenome/MIT_DATA/sample_SRR9205535/assembly_output
threads=8
con_len=0
env_var=$USER_ENV_NAME


./main_assembly_processing.sh $fastq1 $fastq2 $output_folder_assembly $threads $con_len $env_var

mkdir $output_folder_assembly/temp

output_folder_reference=/work/yaolab/shared/2021_milk_2017_metagenome/MIT_DATA/sample_SRR9205535/reference_output
./main_reference_processing.sh $fastq1 $fastq2 $output_folder_reference

mkdir $output_folder_reference/temp
