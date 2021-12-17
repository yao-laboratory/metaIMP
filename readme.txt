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

ASSEMBLY PIPELINE OUTPUT OUTLINE:

OUTPUT FOLDER
|
|_______METASPADES FOLDER
| |_____SAM FILE
| |_____BAM FILE
| |_____BAM SORTED FILE
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

REFERENCE PIPELINE OUTPUT OUTLINE:

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


Python modules used:

Bio- This module needs to be installed-- pip install biopython
os
argparse
pandas - This module needs to be installed - pip install pandas
gzip

--------------------------------------
