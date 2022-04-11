#This script runs the Assembly mapping between SNPS provided by INSTRAIN and ANNOTATIONS provided by EGGNOG
#Inputs are provided in MAIN_ASSEMBLY_PROCESSING.SH
#THERE ARE FOUR INPUTS TO THIS SCRIPT:  1) SNPS FILE/FOLDER PATH OBTAINED FROM INSTRAIN
#					2) ANNOTATIONS FILE/FOLDER PATH OBTAINED FROM EGGNOG
#					3) MERGEDFILE PATH OBTAINED FROM CHECKM BINNING (ASSEMBLY_BINNING.SH)
#					4) OUTPUT FOLDER PATH

instrain=$1
eggnog=$2
mergedfile=$3
output=$4

if [ ! -d "$output" ] ; then
        mkdir $output
fi

DIR="${BASH_SOURCE[0]}"
DIR="$(dirname "$DIR")"

echo 'starting assembly mapping'
cd ./python_scripts/
python $DIR/python_scripts/Assembly_mapping.py a_map -i $instrain -e $eggnog -m $mergedfile -o $output

echo 'assembly mapping complete'

imusage=$(free | awk '/Mem/{printf("RAM Usage: %.2f%\n Mbits"), $3/1000000}' |  awk '{print $3}' | cut -d"." -f1)
echo "Current Memory Usage for ${BASH_SOURCE[0]} is: $imusage MBits"

echo "metaIMP step 5 complete. starting step_6"
