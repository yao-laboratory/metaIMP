#This script creates a new custom environment provided by the user
#All dependencies for metaimp are installed using this script

echo "Creating new user environemnt"

conda create -n $USER_ENV_NAME
conda install -y python=3.7

echo " Python 3.7 is installed"
echo " Activating $USER_ENV_NAME"
source activate $USER_ENV_NAME
 
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
mamba install -y -c bioconda usearch
mamba install -c conda-forge singularity

echo " All dependencies are installed. Deactivating $USER_ENV_NAME"
conda deactivate

