##THIS IS BIN TABLE IN MAKING. KEY Features:similar and different AA count. 
##Authors: Kalyan Sahu, Qiuming Yao
##Affiliation: Integrated Digital Omics Lab (IDOL), School of Computing, University of Nebraska-Lincoln


#imports
import pandas as pd 
import numpy as np
import os
import argparse


#sample_dir="/work/yaolab/shared/2021_milk_2017_metagenome/WOLLY_MAMMUTH/Sweden_samples/sample_ERR5032104/assembly_output/"
#sample_name="mammuth1"

def make_bin_table(sample_dir,sample_name):
    dst=pd.read_csv(os.path.join(sample_dir,"DAS_TOOL/das_tool_output_DASTool_summary.tsv"),sep='\t',header=0)
    print(dst,"this is the das tool file")
    dst_selective=dst[['bin','bin_score','SCG_completeness','SCG_redundancy']]
    t1_coding=pd.read_csv(os.path.join(sample_dir,"ASSEMBLY_SNP_ANNOTATION/Table_1_assembly_mapping_result_coding.csv"),sep=",",header=0)
    t1_coding_selective=t1_coding[['scaffold','coding_region']].groupby('scaffold').size().to_frame().reset_index()
    t1_coding_selective.columns=['scaffold','num_coding_mutation']

    t2_noncoding=pd.read_csv(os.path.join(sample_dir,"ASSEMBLY_SNP_ANNOTATION/Table_2_assembly_mapping_result_noncoding.csv"),sep=",",header=0)
    t2_noncoding_selective=t2_noncoding[['scaffold']].groupby('scaffold').size().to_frame().reset_index()
    t2_noncoding_selective.columns=['scaffold','num_noncoding_mutation']

    t1_t2_merge=pd.merge(t1_coding_selective,t2_noncoding_selective,on='scaffold',how='outer').fillna(0)

    t5_aa=pd.read_csv(os.path.join(sample_dir,"ASSEMBLY_SNP_ANNOTATION/Table_5_assembly_AA_mapping_result.csv"),sep=",",header=0)
    t5_aa_selective=t5_aa[['SCAFFOLD','protein_id','ALT_AA','REF_AA']]
    same_aa_dict=dict()
    diff_aa_dict=dict()
    for i in t5_aa_selective.index:
        scaffold=t5_aa_selective.loc[i]["SCAFFOLD"]
        alt=t5_aa_selective.loc[i]["ALT_AA"]
        ref=t5_aa_selective.loc[i]["REF_AA"]
        if scaffold not in same_aa_dict:
            same_aa_dict[scaffold]=0
        if scaffold not in diff_aa_dict:
            diff_aa_dict[scaffold]=0
        if alt==ref:
            same_aa_dict[scaffold]=same_aa_dict[scaffold]+1
        else:
            diff_aa_dict[scaffold]=diff_aa_dict[scaffold]+1
    scaffold_list=list()
    same_aa_count_list=list()
    diff_aa_count_list=list()
    for scaffold in same_aa_dict.keys():
        same_aa_count=same_aa_dict[scaffold]
        diff_aa_count=diff_aa_dict[scaffold]
        scaffold_list.append(scaffold)
        same_aa_count_list.append(same_aa_count)
        diff_aa_count_list.append(diff_aa_count)

    t5_aa_count_data = {'scaffold': scaffold_list, 'same_aa_count': same_aa_count_list, 'diff_aa_count': diff_aa_count_list}
    t5_aa_count_df = pd.DataFrame.from_dict(t5_aa_count_data)

    t6_species=pd.read_csv(os.path.join(sample_dir,"ASSEMBLY_SNP_ANNOTATION/Table_6_assembly_bin_species.csv"),sep=",",header=0)
    t6_species_selective=t6_species[['bin','P','C','O','F','G','S','coverage','Genome size','N50 (scaffolds)','Coding density',
                                     'total_mutation_count_by_instrain','total_mutation_count_by_metaIMP','scaffold']]

    species_aa_merge=pd.merge(t6_species_selective,t5_aa_count_df,how='left',on='scaffold')
 
    intermediate_table=pd.merge(species_aa_merge,t1_t2_merge,on='scaffold',how='left')

    final_merge=pd.merge(intermediate_table,dst_selective,on='bin',how="left")

    final_merge['sample_name']=[sample_name]*final_merge.shape[0]
    output_file=sample_dir+"/ASSEMBLY_SNP_ANNOTATION/Table_9_bin_AA.csv"
    print(output_file,"this is the output file")
    final_merge.to_csv(output_file,index=None, sep = '\t')
    return final_merge


def main():
    parser = argparse.ArgumentParser(prog='step6_assembly_based',description='this method creates table 9, with bin information and AA count')
    subparser = parser.add_subparsers(dest='subcommand',help ='enter the output folder, samplename')
    
    assembly_bin_aa_parser=subparser.add_parser("bin_aa_map", help = " This function maps binning tables to their annotations")
    assembly_bin_aa_parser.add_argument("-i", dest="output_folder", type=str, help="output folder eg./path/to/metaIMP_output_folder as input")
    assembly_bin_aa_parser.add_argument("-s", dest="sample_name",  type=str, help="this will be the sample ID")
    
    args = parser.parse_args()
    
    if args.subcommand=='bin_aa_map':
        sample_dir=args.output_folder
        sample_name=args.sample_name
        print("---------------Start to do assembly AA map")
        make_bin_table(sample_dir,sample_name)
        print("---------------End assembly AA map")
    else:
        print("Wrong input. Check parameters")
