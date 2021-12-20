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

echo 'starting assembly mapping'
cd ./python_scripts/
python Assembly_mapping.py a_map -i $instrain -e $eggnog -m $mergedfile -o $output

echo 'assembly mapping complete'
