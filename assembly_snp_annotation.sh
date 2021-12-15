#this script runs the assembly mapping. inputs are provided in main.sh

echo 'loading python module'
module load python/3.6


instrain=$1
eggnog=$2
mergedfile=$3
output=$4

echo 'starting assembly mapping'
cd /work/yaolab/shared/2021_milk_2017_metagenome/PIPELINE_TESTING/python_scripts/
python Assembly_mapping.py a_map -i $instrain -e $eggnog -m $mergedfile -o $output

echo 'assembly mapping complete'
