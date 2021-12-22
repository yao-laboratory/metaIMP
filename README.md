# metaIMP

Welcome to metaIMP - an integrated metagenomic pipeline which allows you to use multiple genomic tools in sequence and tells you the annnotations of discovered mutations.
It's all in one place!!!
#########################################################################################################################################################################
#########################################################################################################################################################################

USER DOCUMENTATION::



metaIMP is an integrated metagenomic pipeline which allows users to identify mutations and their respective protein annotations using a pipeline model. In this document, we list out the steps to be followed by a user to successfully complete assembly and reference based methods of metagenomic analysis.



Prepare your dataset: Paired-end files ( FASTQ1,FASTQ2). Can be FASTA format

Download metaIMP repository. Use the folder path as input to all the sh scripts.

If the user environment does not exist, create a new environment. Refer to readme.txt This environment name also is an input.
	
Install dependencies in your environment such as Python. Install packages: pandas and Bio

Follow the example shell script named “example_hcc_job.sh” to create a bash job for metaIMP pipeline. 

In this job, the user will need to provide the following information:
	
Input paired-end file path
Output folder path
Number of threads 
Minimum contig length ( OPTIONAL) (ASSEMBLY ONLY) - if the user wants to filter contigs after assembly process, this option should be used.
Path to metaIMP directory
Environment variable calling

ENJOY!!!

