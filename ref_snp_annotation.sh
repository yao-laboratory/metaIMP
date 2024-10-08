genes_folder=$1
patric_folder=$2
snps_folder=$3
output_folder=$4
output_folder_final=$output_folder/REFERENCE_SNP_ANNOTATION
echo 'this is reference based mapping'


if [ ! -d "$output_folder" ] ; then
        mkdir $output_folder
fi

DIR="${BASH_SOURCE[0]}"
DIR="$(dirname "$DIR")"

python $DIR/python_scripts/Reference_mapping.py add_figid -gf $genes_folder -pf $patric_folder

echo 'finished adding fig_ids to peg_ids. now run patric.sh first to get the annotation. then last step is to map the annotation with midas by running the ref_map command'

for f in $patric_folder/*.patric.csv
do
       echo 'we are now processing all genes files to which 'fig_id' tag is added and these files will now run through PATRIC DATABASE'
	echo 'currently processing'$f
        apptainer exec docker://unlhcc/patric p3-get-feature-data --col=1 --attr aa_length --attr aa_sequence  --attr aa_sequence_md5 --attr accession --attr alt_locus_tag \
                --attr annotation --attr classifier_round --attr classifier_score --attr date_inserted --attr date_modified --attr ec --attr end --attr feature_id --attr feature_type \
                --attr figfam_id  --attr gene --attr gene_id --attr genome_id --attr genome_name --attr go --attr location --attr na_length --attr na_sequence --attr na_sequence_md5 \
                --attr notes --attr owner  --attr p2_feature_id --attr pathway --attr patric_id --attr pgfam_id --attr plfam_id --attr product --attr property --attr protein_id \
                --attr public --attr refseq_locus_tag --attr segments --attr sequence_id --attr start --attr strand --attr subsystem --attr taxon_id \
                --attr text --attr user_read --attr user_write --attr function \
                < $f > ${f%%.*}.feature.csv
done


echo 'completed mapping PEG_IDs to PATRIC'

#python $DIR/python_scripts/Reference_mapping.py ref_map -pf $patric_folder -sf $snps_folder -o $output_folder
#echo 'completed reference_mapping. Good luck!!!'

#echo 'creating VCF reference output file'
#python $DIR/python_scripts/VCF_converter_reference.py vcf_map_reference -i $output_folder -o $output_folder
#echo 'VCF file created for reference process'

#echo 'calculating Amino acid mutations'
#python $DIR/python_scripts/Reference_AA_mapping.py aa_map_reference -i $output_folder -o $output_folder
#echo 'aa_map_reference -i $output_folder -o $output_folder'
#echo 'AA mutations calcuated'
