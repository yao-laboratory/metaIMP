#!/bin/bash

demo=/path/to/demo.fastq.gz #obtain this from Humann3
my_bowtie_db=/work/HCC/BCRF/app_specific/metaphlan/4/vJun23_202403/
my_index=mpa_vJun23_CHOCOPhlAnSGB_202403

module load humann/3.9

output_folder=$PWD/Human3_Test_With_Demo_With_Full_Code

humann --input $demo --output $output_folder  --protein-database /work/HCC/BCRF/app_specific/humann/3/3.9/uniref/uniref50 --metaphlan-options "--bowtie2db $my_bowtie_db --index $my_index"

humann_renorm_table --input $output_folder/genefamilies.tsv \
    --output $output_folder/genefamilies-cpm.tsv --units cpm --update-snames

humann_regroup_table --input $output_folder/genefamilies-cpm.tsv \
    --output $output_folder/rxn-cpm.tsv --groups uniref50_rxn

humann_regroup_table --input $output_folder/genefamilies-cpm.tsv \
    --output $output_folder/rxn-cpm.tsv --groups uniref50_rxn

scp $output_folder/humann_temp/metaphlan_bugs_list.tsv $output_folder/metaphlan_profile.tsv
