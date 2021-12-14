module load python/3.6

genes_folder=$1
patric_folder=$2
snps_folder=$3
output_folder=$4

echo 'this is reference based mapping'

cd /work/yaolab/shared/2021_milk_2017_metagenome/PIPELINE_TESTING/python_scripts/

python Reference_mapping.py -add_figid -gf $genes_fodler -pf $patric_folder

echo 'finished adding fig_ids to peg_ids. now run patric.sh first to get the annotation. then last step is to map the annotation with midas by running the ref_map command'

python Reference_mapping.py -ref_map -pf $patric_folder -sf $snps_folder -o $output_folder

echo 'completed reference_mapping. Good luck!!!'

