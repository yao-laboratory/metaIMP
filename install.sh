#This script creates a new custom environment provided by the user
#All dependencies for metaimp are installed using this script

echo "Creating new user environemnt"

mamba create -n $USER_ENV_NAME

echo " Activating $USER_ENV_NAME"

current_env="$(basename $CONDA_PREFIX)"

if [[ "$current_env" != "$USER_ENV_NAME" ]]; then
    source activate $USER_ENV_NAME
fi

current_env="$(basename $CONDA_PREFIX)"

if [[ "$current_env" != "$USER_ENV_NAME" ]]; then
    conda activate $USER_ENV_NAME
fi

current_env="$(basename $CONDA_PREFIX)"
if [[ "$current_env" != "$USER_ENV_NAME" ]]; then
    echo "the environment cannot be activated"
    exit 1
fi

mamba install -y python=3.7
echo " Python 3.7 is installed"

mamba install -y -c bioconda quast
mamba install -y -c bioconda bowtie2
mamba install -y -c bioconda spades
mamba install -y -c bioconda metabat2
mamba install -y -c bioconda checkm-genome
mamba install -y -c bioconda das_tool
mamba install -y -c bioconda phylophlan
mamba install -y -c bioconda eggnog-mapper
mamba install -y -c bioconda kraken2
mamba install -y -c bioconda fastqc
mamba install -y -c bioconda usearch
mamba install -y -c conda-forge singularity

#important tools

mamba install -y -c conda-forge biopython=1.76
mamba install -y -c bioconda midas
#MIDAS corrupts SAMTOOLS binary files. INSTALL SAMTOOLS AGAIN in the last step.
mamba install -y -c conda-forge -c bioconda -c defaults instrain
mamba install -y -c bioconda samtools=1.14

echo " All dependencies are installed. Deactivating $USER_ENV_NAME"
conda deactivate

