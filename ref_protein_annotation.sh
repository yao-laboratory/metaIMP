
genes_folder=$1
patric_folder=$2
snps_folder=$3
output_folder=$4
midas_species_folder=$output_folder/MIDAS/species/species_profile.txt
output_folder_final=$output_folder/REFERENCE_SNP_ANNOTATION
echo 'this is reference based mapping'


if [ ! -d "$output_folder" ] ; then
        mkdir $output_folder
fi

DIR="${BASH_SOURCE[0]}"
DIR="$(dirname "$DIR")"

#python $DIR/python_scripts/Reference_mapping.py ref_map -pf $patric_folder -sf $snps_folder -o $output_folder_final
echo 'completed reference_mapping. Good luck!!!'

echo 'creating VCF reference output file'
python $DIR/python_scripts/VCF_converter_reference.py vcf_map_reference -i $output_folder_final -o $output_folder_final
echo 'VCF file created for reference process'

echo 'calculating Amino acid mutations'
python $DIR/python_scripts/Reference_AA_mapping.py aa_map_reference -i $output_folder_final -o $output_folder_final
echo 'aa_map_reference -i $output_folder -o $output_folder'
echo 'AA mutations calcuated'


echo "species summary is being created at $(date)"
python $DIR/python_scripts/Reference_species_summary.py species_mut_count -m $midas_species_folder -n $output_folder_final
echo "species summary is done at $(date)"

echo "starting ec and go map"

python $DIR/python_scripts/Reference_EC_mapping.py ec_map -i $output_folder_final -o $output_folder_final
echo "python $DIR/python_scripts/Reference_EC_mapping.py ec_map -i $output_folder_final -o $output_folder_final"

python $DIR/python_scripts/Reference_GO_mapping.py go_map -i $output_folder_final -o $output_folder_final

echo "finished ec go map $(date)"
