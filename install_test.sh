#This script allows users to test installed dependencies in custom created 
#Custom environment was created using install.sh

echo " Activating $USER_ENV_NAME"
source activate $USER_ENV_NAME

echo " Testing commands for the following:
	ASSEMBLY BASED PIPELINE:
	1.Samtools
	2.Bowtie
	3.MetaSpades
	4.Quast
	5.Metabat
	5.CheckM
	6.DAS_TOOL
	7.PHYLOPHLAN
	8.INSTRAIN
	9.EGGNOG
	10.KRAKEN

	REFERENCE BASED PIPELINE:
	1.MIDAS
	2.SINGULARITY

	FASTQC is common installation to both the pipelines"

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
