#!/bin/bash
#SBATCH --job-name=env_inst
#SBATCH --nodes=1
#SBATCH --time=2:00:00
#SBATCH --mem=4gb
#SBATCH --output=env_inst.%J.out
#SBATCH --error=env_inst.%J.err

#this script is an example of how to install dependencies on HCC cluster

module unload python
source activate metaimp_env2

module load mamba

mamba install -y -c bioconda samtools
mamba install -y -c bioconda quast
mamba install -y -c bioconda bowtie2
mamba install -y -c bioconda spades
mamba install -y -c bioconda metabat2
mamba install -y -c bioconda checkm-genome
mamba install -y -c bioconda das_tool
mamba install -y -c bioconda phylophlan
mamba install -y -c conda-forge -c bioconda -c defaults instrain
mamba install -y -c bioconda eggnog-mapper
mamba install -y -c bioconda midas
mamba install -y -c bioconda kraken2
mamba install -y -c bioconda fastqc

conda deactivate

