#This script allows users to test installed dependencies in custom created 
#Custom environment was created using install.sh

USER_ENV=$1
source activate $USER_ENV

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
