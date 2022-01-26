#!/bin/bash
#SBATCH --job-name=env_test
#SBATCH --nodes=1
#SBATCH --time=24:00:00
#SBATCH --mem=96gb
#SBATCH --output=env_test.%J.out
#SBATCH --error=env_test.%J.err

#this job is an example to test the installed dependencies on HCC cluster
source activate metaimp_env2

samtools view -h
bowtie2 -h
spades.py -h
quast.py-h
metabat2 -h
checkm lineage_wf -h
DAS_Tool -h
phylophlan_metagenomic -h
inStrain profile -h
emapper.py -h
run_midas.py -h
kraken2 -h
fastqc -h

conda deactivate
