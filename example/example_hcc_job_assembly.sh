#!/bin/bash
#SBATCH --job-name=hcc_assembly
#SBATCH --nodes=1
#SBATCH --time=24:00:00
#SBATCH --mem=96gb
#SBATCH --ntasks-per-node=8
#SBATCH --output=hcc_assembly.%J.out
#SBATCH --error=hcc_assembly.%J.err


#Example HCC Assembly job
#metaimp path: Repository downloaded by user from Github
metaIMP_path=/home/yaolab/ksahu2/.ssh/metaIMP
export USER_ENV_NAME=metaimp_env
#Kraken database path
kraken_db_path=/work/HCC/BCRF/app_specific/kraken/2.0
export KRAKEN_DATABASE=$kraken_db_path
#Phylophlan database path
phylophlan_db_name=SGB.Jan19
export PHYLOPHLAN_DATABASE=$phylophlan_db_name
#Eggnog database path
eggnog_db_name=/work/HCC/BCRF/app_specific/eggnog-mapper/2.1.3
export EGGNOG_DIAMOND_DATABASE=$eggnog_db_name
#export eggnog_db_name=$EGGNOG_DIAMOND_DATABASE

#Inputs- FASTQ/FASTA paired-end files
fastq1=/work/yaolab/shared/2021_milk_2017_metagenome/MIT_DATA/sample_SRR9205542/SRR9205542_1.fastq
fastq2=/work/yaolab/shared/2021_milk_2017_metagenome/MIT_DATA/sample_SRR9205542/SRR9205542_2.fastq
sampleID=SRR9205542
#output_folder_assembly path
output_folder_assembly=/work/yaolab/shared/2021_milk_2017_metagenome/MIT_DATA/sample_SRR9205542/assembly_output

#number of threads to be used by metaSPADES and Instrain
threads=8

#Minimum_contig_length for filtering. THIS IS OPTIONAL
con_len=1000


#user environment name
#env_var=$USER_ENV_NAME


#modules for assembly_binning.sh:

echo "loading modules for assembly_binning.sh"
module load python/3.8 
module load spades/3.14
module load quast/5.0
module load bowtie/2.3
module load samtools/1.9
module load metabat2/2.15
module load checkm-genome/1.1
module load fastqc/0.11
module load kraken2/2.0.8-beta
module load das_tool/1.1
module load usearch/11.0
module load phylophlan/3.0
#modules for assembly_contig_annotation.sh:
echo "loading modules for assembly_contig_annotation.sh"
module load eggnog-mapper/2.1
ml megahit/1.1
#modules for assembly_snp_calling.sh:
module load instrain/1.3
export PYTHONNOUSERSITE=1



echo " "
echo "###########################################################################################################"
echo "$metaIMP_path/main_assembly_processing.sh $fastq1 $fastq2 $sampleID $output_folder_assembly $threads $con_len"
$metaIMP_path/main_assembly_processing_new.sh $fastq1 $fastq2 $sampleID $output_folder_assembly $threads $con_len

echo " "
echo "###########################################################################################################"

