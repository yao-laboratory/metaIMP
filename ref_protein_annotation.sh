
genes_folder=$1
patric_folder=$2
snps_folder=$3
output_folder=$4

echo 'this is reference based mapping'


if [ ! -d "$output_folder" ] ; then
        mkdir $output_folder
fi

DIR="${BASH_SOURCE[0]}"
DIR="$(dirname "$DIR")"

python $DIR/python_scripts/Reference_mapping.py ref_map -pf $patric_folder -sf $snps_folder -o $output_folder
echo 'completed reference_mapping. Good luck!!!'

echo 'creating VCF reference output file'
python $DIR/python_scripts/VCF_converter_reference.py vcf_map_reference -i $output_folder -o $output_folder
echo 'VCF file created for reference process'

echo 'calculating Amino acid mutations'
python $DIR/python_scripts/Reference_AA_mapping.py aa_map_reference -i $output_folder -o $output_folder
#echo 'aa_map_reference -i $output_folder -o $output_folder'
echo 'AA mutations calcuated'
