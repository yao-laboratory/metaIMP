Tools used:


#Tools which directly contribute to the assembly pipeline:

BBMap
Metaspades
Samtools
Bowtie
Metabat
CheckM
Instrain
Eggnog
STEP 5 python code


---------------------------------------------------------------------------------------
#For quality control and analysis of bins (No direct contribution to the pipeline - mutation and annotations)  :

QCTools
MetQuast
Das_tool
Kraken
Phylophlan
----------------------------------------------------------------------------------------
#This section describes how to create a virtual python environment to run our pipeline:
Steps:

1) Verify conda is installed, check version number : conda info
2) Update conda to the current version : conda update conda
3) List the environment you have ever created : conda env list
4) Install a package included in Anaconda : conda install PACKAGENAME  
5) Create a new environment (example name: metaIMP_env), install Python 3.5 : conda create -n metaIMP_env python=3.5 
6) Activate new environment : conda activate metaIMP_env
7) Now your new environment is ready to use metaIMP python codes.
8) Proceed with step 4 if any missing packages are found
9) Deleting environment:conda remove --name metaIMP_env
	a) Deleting a package: conda remove package
10) Sharing environment with a friend: 
	a) conda metaIMP_env export > environment.yml 
	b) conda env create -f environment.yml

-------------------------------------------





----------------------------------------------------

#ASSEMBLY PIPELINE OUTPUT OUTLINE:
OUTPUT FOLDER
|_______METASPADES FOLDER
| |_____SAM FILE
| |_____BAM FILE
| |_____BAM SORTED FILE
| |_____CONTIGS.FASTA
|
|_______BINS FOLDER
| |_____CHECKM FOLDER
| |_____ MERGEDFILE.FNA
| 
|_______INSTRAIN FOLDER
|_______EGGNOG RESULTS
|_______PHYLOPHLAN FOLDER
|_______KRAKEN FOLDER
|_______QUAST FOLDER
|_______DAS_TOOL FOLDER
|_______QC TOOL FOLDER
|_______ASSEMBLY SNP ANNOTATION

---------------------------------------

#REFERENCE PIPELINE OUTPUT OUTLINE:

OUTPUT FOLDER
|
|__________MIDAS FOLDER
| |________MIDAS SPECIES
| |________MIDAS GENES
| | |______UPDATED PATRIC FILES (WITH FIG_ID PREFIX- PATRIC.CSV) AND PATRIC ANNOTATIONS ( FEATURE.CSV)
| |________MIDAS SNPS
|__________REFERENCE SNP ANNOTATIONS

---------------------------------------

----------------------------------------------------------------------------------------
#Tools which directly contribute to the reference pipeline:

Midas
Patric
STEP 5 python code
----------------------------------------------------------------------------------------


#Python modules used:

Bio- This module needs to be installed-- pip install biopython
os
argparse
pandas - This module needs to be installed - pip install pandas
gzip

--------------------------------------
