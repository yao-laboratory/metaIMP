MetaIMP
This is a test of new line \n
We are using \n to test new line \n
Ignore \n
Delete these lines after testing \n

-------------
INTRODUCTION
-------------
metaIMP is an integrated metagenomic pipeline which allows users to identify mutations and their respective protein annotations using a pipeline model. In this document, we list out the steps to be followed by a user to successfully complete assembly and reference based methods of metagenomic analysis. Users can choose either the assembly or reference method to begin processing of two paired-end files provided as input in FASTA format.

-------------
INSTALLATION
-------------
metaIMP requires a cocktail of Java, Python and Linux scripts in order to provide the most accurate analysis of user's metagenome data. Backend is based on Linux, which can be accessedusing any unix terminal.

To download metaIMP from Github, use : git clone https://github.com/yao-laboratory/metaIMP

After the repo is cloned, user can run the following shell script to install their custom python environment
```
export $USER_ENVIRONMENT

1) ./install.sh
2) ./install_test.sh
```
These tools are required to be installed for metaIMP:
samtools
quast
bowtie2
spades
metabat2
checkm-genome
das_tool
phylophlan
instrain
eggnog-mapper
midas
kraken2
fastqc
singularity


These python packages are required for metaIMP:
```
python/3.6
pandas
Bio
```

These steps describes how to create, update and verify a virtual python environment to run our pipeline:

1) Verify conda is installed and check version number 
```
conda info
```
2) Update conda to the current version 
```
conda update conda
```
3) List the environment you have ever created
```
conda env list
```
4) Install a package included in Anaconda 
```
conda install *PACKAGENAME*
```
5) Create a new environment (example name: metaIMP_env) 
6) Install Python 3.8 
```  
conda create -n metaIMP_env python=3.8.12
```
7) Install pacakges for python in the new environment
```
pip install biopython 1.79

pip install pandas 1.3.5
```
8) Activate new environment 
```
conda activate metaIMP_env
```
9) Now your new environment is ready to use metaIMP python codes.
10) Proceed with step 4 if any missing packages are found
11) Deleting environment
```
conda remove --name metaIMP_env
```
12) Sharing environment with a friend
```
conda metaIMP_env export > environment.yml
conda env create -f environment.yml
```
-------------
TUTORIAL
-------------

metaIMP is an integrated metagenomic pipeline which allows users to identify mutations and their respective protein annotations using a pipeline model. In this document, we list out the steps to be followed by a user to successfully complete assembly and reference based methods of metagenomic analysis. Users can choose either the assembly or reference method to begin processing of two paired-end files provided as input in FASTA format.
The users must download the metaIMP repository and use the local folder path of the repo as input to all the sh scripts.

```
STEP 0: Download fastq files from NCBI (http://ncbi.nlm.nih.gov)

STEP 1: Assembly based method

* Submit stand alone job for assembly pipeline using the stand alone example jobs in the Example folder.

* Submit job from Open-Science Grid (OSG) using example OSG jobs in the Example folder. 

* Submit job from UNL's Holland Computing Center (HCC) server using using HCC jobs in the Example folder.

STEP 2: Reference based method

* Submit stand alone job for reference pipeline using

* Submit job from Open-Science Grid (OSG) using

* Submit job from UNL's Holland Computing Center (HCC) server using
```

----------------------
COMMAND LINE AND INPUT
----------------------
In this pipeline, the user will need to provide the following information:

1) Input paired-end file path
2) Output folder path
3) Number of threads
4) Minimum contig length ( OPTIONAL) (ASSEMBLY ONLY) - if the user wants to filter contigs after assembly process, this option should be used.
5) Path to metaIMP directoryEnvironment variable calling

Users must run install.sh to create an environment for metaIMP. Next, users can either use the stand-alone version or the OSG version
from the examples folder to complete their analysis.

```
1) read1 = Forward paired-end file (FASTQ)
2) read2 = Reverse paired-end file (FASTQ)
3) sampleID = sample name used in renaming the fastq reads and later processing
4) output_folder= Output folder path
5) min_thread= Total number of threads
6) min_contig_length (OPTIONAL) = filter contigs based on minimum length (ex: 1000)
```
------
OUTPUT
------
ASSEMBLY PIPELINE OUTPUT FOLDER OUTLINE:


METASPADES

	SAM FILE

	BAM FILE
	
	BAM SORTED FILE
	
	CONTIGS.FASTA


BINS

```
CHECKM FOLDER
	
MERGEDFILE.FNA
```

INSTRAIN

EGGNOG

DAS_TOOL

QUAST

FASTQC

LOG

ASSEMBLY SNP ANNOTATION

---------------------------------------------------------------------------------
---------------------------------------------------------------------------------
<pre>
   ASSEMBLY OUTPUT FOLDER
   |--ASSEMBLY SNP ANNOTATION 
   |-- METASPADES </br>
   |   |-- CONTIGS.FASTA </br>
   |   |-- COVERAGE.TXT </br> 
   |   |-- ALN.SAM.GZ </br>
   |   |-- DEPTH.TXT </br>
   |-- BINS </br>
   |   |-- CHECKM </br>
   |-- EGGNOG </br>
   |-- INSTRAIN </br>
   |-- DAS_TOOL </br>
   |-- PHYLOPHLAN </br>
   |-- KRAKEN </br>
   |-- FASTQC </br>
   |-- QUAST </br>
   |-- LOG FOLDER </br>
   |-- TEMP FOLDER </br>
</pre>

MIDAS

```
SPECIES

GENES

SNPS
```

FASTQC

LOG

REFERENCE SNP ANNOTATION

----
TIPS
----
In order to install dependencies independently for this pipeline using conda/mamba, use the following commands:


1) How to use log file

Users can resume at any step by erasing the log file of a particular process and then restarting the pipeline.

```
cd ./log_folder

rm preprocessing.log

sbatch example_stand_along_job.sh

```


2) Use your own contig file

Users can replace the contig.fasta file created by metaIMP post-assembly and resume metaIMP pipeline. This would allow users to use a pre-existing contig file.



---------------------------------------------------------------------------------------
