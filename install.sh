#This script creates a new custom environment provided by the user
#All dependencies for metaimp are installed using this script

install_singularity=$1
echo "Creating new user environemnt"

mamba create -n $USER_ENV_NAME

echo " Activating $USER_ENV_NAME"

current_env="$(basename $CONDA_PREFIX)"

if [[ "$current_env" != "$USER_ENV_NAME" ]]; then
    echo "----trying source activate---"
    source activate $USER_ENV_NAME
fi

current_env="$(basename $CONDA_PREFIX)"

if [[ "$current_env" != "$USER_ENV_NAME" ]]; then
    echo "---trying conda activate---"
    if [ "$(command -v conda)" ]; then
        echo "conda is working..."
        conda activate $USER_ENV_NAME
    fi
fi

current_env="$(basename $CONDA_PREFIX)"

if [[ "$current_env" != "$USER_ENV_NAME" ]]; then
    echo "---trying conda activate with initializing bashrc---"
    if [ "$(command -v conda)" ]; then
        echo "conda is working..."
        conda init bash
        source ~/.bashrc
        echo "conda activate $USER_ENV_NAME"
       conda activate $USER_ENV_NAME
    fi
fi

echo "---conda prefix : $CONDA_PREFIX"

current_env="$(basename $CONDA_PREFIX)"
if [[ "$current_env" != "$USER_ENV_NAME" ]]; then
    echo "the environment cannot be activated"
    exit 1
fi

if [ "$(command -v module)" ]; then
  echo 'Unload any existed python'
  module unload python
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
mamba install -y -c conda-forge biopython=1.76
mamba install -y -c bioconda midas
#MIDAS corrupts SAMTOOLS binary files. INSTALL SAMTOOLS AGAIN in the last step.
mamba install -y -c conda-forge -c bioconda -c defaults instrain
mamba install -y -c bioconda samtools=1.14
mamba install -y -c anaconda scikit-bio

#updated ulitity.py
cp $metaIMP_path/python_scripts/utility.py $CONDA_PREFIX/lib/python3.7/site-packages/midas/
#Copying MIDAS utility.py to user environment where MIDAS is installed

if [[ "$install_singularity" == "-s" ]]; then
	mamba install -y -c conda-forge singularity
fi

#important tools
#mamba install -y -c conda-forge biopython=1.76
#mamba install -y -c bioconda midas
#MIDAS corrupts SAMTOOLS binary files. INSTALL SAMTOOLS AGAIN in the last step.
#mamba install -y -c conda-forge -c bioconda -c defaults instrain
#mamba install -y -c bioconda samtools=1.14
#updated ulitity.py
#cp $metaIMP_path/python_scripts/utility.py $CONDA_PREFIX/lib/python3.7/site-packages/midas/
#Copying MIDAS utility.py to user environment where MIDAS is installed

echo " All dependencies are installed. Deactivating $USER_ENV_NAME"
conda deactivate

