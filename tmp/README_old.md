

metaIMP

An integrated metagenomic pipeline which allows you to use multiple genomic tools in sequence and tells you the annnotations of discovered mutations.

Description:



metaIMP is an integrated metagenomic pipeline which allows users to identify mutations and their respective protein annotations using a pipeline model. In this document, we list out the steps to be followed by a user to successfully complete assembly and reference based methods of metagenomic analysis.



Prepare your dataset: Paired-end files ( FASTQ1,FASTQ2). Can be FASTA format

Download metaIMP repository. Use the folder path as input to all the sh scripts.
	
Install dependencies in your environment such as Python. Install packages: pandas and Bio

Follow the example shell script named “example_hcc_job.sh” to create a bash job for metaIMP pipeline. 

In this job, the user will need to provide the following information:
	
Input paired-end file path
Output folder path
Number of threads 
Minimum contig length ( OPTIONAL) (ASSEMBLY ONLY) - if the user wants to filter contigs after assembly process, this option should be used.
Path to metaIMP directory
Environment variable calling

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
5) Create a new environment (example name: metaIMP_env), install Python 3.8 : conda create -n metaIMP_env python=3.8.12 
6) Install pacakges for python in the new environment: pip install biopython 1.79, pip install pandas 1.3.5
6) Activate new environment : conda activate metaIMP_env
7) Now your new environment is ready to use metaIMP python codes.
8) Proceed with step 4 if any missing packages are found
9) Deleting environment:conda remove --name metaIMP_env
	a) Deleting a package: conda remove package
10) Sharing environment with a friend: 
	a) conda metaIMP_env export > environment.yml 
	b) conda env create -f environment.yml

-------------------------------------------

In order to install dependencies for this pipeline using conda/mamba, use the following commands:

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
mamba install -c conda-forge singularity



----------------------------------------------------

#ASSEMBLY PIPELINE OUTPUT OUTLINE:
OUTPUT FOLDER <br />
|______METASPADES FOLDER <br />
| |_____SAM FILE <br />
| |___BAM FILE <br />
| |____BAM SORTED FILE <br />
| |___CONTIGS.FASTA <br />
|
|______BINS FOLDER <br /> 
| |_____CHECKM FOLDER <br />
| |____ MERGEDFILE.FNA <br />
| 
|_INSTRAIN FOLDER <br />
|_EGGNOG RESULTS <br /> 
|_PHYLOPHLAN FOLDER <br />
|_______KRAKEN FOLDER <br />
|_______QUAST FOLDER <br />
|_______DAS_TOOL FOLDER <br />
|_______QC TOOL FOLDER <br />
|_______ASSEMBLY SNP ANNOTATION <br />

---------------------------------------

#REFERENCE PIPELINE OUTPUT OUTLINE:

OUTPUT FOLDER
|
|__________MIDAS FOLDER <br />
| |________MIDAS SPECIES <br />
| |________MIDAS GENES <br />
| | |______UPDATED PATRIC FILES (WITH FIG_ID PREFIX- PATRIC.CSV) AND PATRIC ANNOTATIONS ( FEATURE.CSV) <br />
| |________MIDAS SNPS <br />
|__________REFERENCE SNP ANNOTATIONS <br />


We also create a empty temporary folder called 'temp' in the output folders for both ASSEMBLY PIPELINE and REFERENCE PIPELINE. User can move any non-essential file to this folder.

---------------------------------------
---------------------------------------

------------------
Script descripton:
------------------


---------
PRE-PROCESSING:
---------

preprocessing.sh: Takes in 2 paired-end FASTQ/FASTA files to filter using BBMAP. 

---------
---------

---------
ASSEMBLY:
---------

1) assembly_binning.sh: Performs binning.  CONTIGS.FASTA file -> SAM file -> BAM FILE -> BAM SORTED FILE -> DEPTH.TXT FILE -> BINNING -> CHECKM BINNING
2) assembly_contig_annotation.sh:          Performs anntotion using EGGNOG. MERGEDFILE (FROM CHECKM BINS) -> ANNOTATIONS 
3) assembly_snp_calling.sh:                Calls mutations (SNPS) using INSTRAIN. BAM SORTED FILE + CONTIGS.FASTA + NUMBER OF THREADS + MERGEDFILE -> OUTPUT_FOLDER
4) assembly_snp_annotation.sh:             Performs mapping between SNPS and their annotations. INSTRAIN + MERGEDFILE + EGGNOG -> OUTPUT_FOLDER
5) main_assembly_processing.sh:            Calls steps 1,2,3 and 4 after pre-processing. Inputs: 1) FASTQ1 2) FASTQ2 3)OUTPUT_FOLDER PATH 4)NUMBER OF THREADS 
					   5)MINIMUM CONTIG LENGTH (OPTIONAL) 6)ENVIRONMENT VARIABLE NAME
---------

---------
REFERENCE:
---------

1) ref_species_genes_snps.sh:     MIDAS performs identification of species, their genes and mutations (SNPs) using a reference database. 1) FASTQ1 2) FASTQ2 3) OUTPUT_FOLDER
2) ref_snp_annotation.sh:         This shell script has multiple purposes. First, it optimizes the output from MIDAS/GENES folder. Then this file can be used as input for annotation using PATRIC.
			          The annotations can be mapped with the mutations (MIDAS/SNPS) using this script. GENES FOLDER + PATRIC FOLDER + SNPS FOLDER -> OUTPUT FOLDER
3) main_reference_processing.sh:  Calls steps 1,2 and 3 after pre-processing. Inputs: 1) FASTQ1 2) FASTQ2 3)OUTPUT_FOLDER PATH 4)ENVIRONMENT VARIABLE NAME


---------
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
These modules are used in scripts which can found in the 'example' folder.
These modules are maintained by Holland Computing Centre  @ University of Nebraska, Lincoln.
We highly recommend users to acquire exact version of the tools we have mentioned below.
______________________________________

MODULE LOADS:
--------------------------------------


REFERENCE PIPELINE:
-------------------

PREPROCESSING.SH:

BBMAP - java/12
-------------------

REF_SPECIES_GENES_SNPS.SH:


module purge
module load midas/1.3
module load samtools/1.9
--------------------


REF_SNP_ANNOTATION:

module load singularity/3.7

-------------------------------



________________________________________


ASSEMBLY PIPELINE:
------------------


ASSEMBLY_BINNING.SH:

module load spades/3.14
module load quast/5.0
module load bowtie/2.3
module load bowtie/2.3
module load samtools/1.9
module load samtools/1.9
module load metabat2/2.15
module load checkm-genome/1.1
--------------------------------

assembly_contig_annotation.sh:

module load eggnog-mapper/2.1


--------------------------------

ASSEMBLY_SNP_ANNOTATION.SH: 

module load python/3.6

-------------------------------
ASSEMBLY_SNP_CALLING.SH:

module load instrain/1.3
#module load python/3.6
#module load biopython/py27/1.74
export PYTHONNOUSERSITE=1

