#!/usr/bin/env python
# coding: utf-8

# In[9]:


"""
This program allows the user to convert the assembly and reference ased output files
to VCF file format

#ASSEMBLY_VCF

##############################################################################
"""


#IMPORTS

import pandas as pd
import datetime
import argparse
import os
from argparse import ArgumentParser

#CREATE A FUNCTION TO CALL IN 2 ARGUMENTS

def vcf_converter(assembly_mapping_result_file, final_vcf_path):
    #defining paths to final output from assembly_mapping and vcf_output_file
    #assembly_mapping_result=os.path.join(assembly_mapping_result,'assembly_mapping_result.csv')
    assembly_input_df= pd.read_csv(assembly_mapping_result_file)
    
    #define vcf column names: https://samtools.github.io/hts-specs/VCFv4.2.pdf
    #define dataframe for VCF columns
    vcf_column_names = ['#CHROM', 'POS','ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'MetaIMP_ID']
    vcf_assembly_df = pd.DataFrame(columns = vcf_column_names)
    
    #create empty lists for the following columns:
    contig_id_list = list()
    position_list = list()
    ref_base_list = list()
    var_base_list = list()
    metaimp_id_list = list()
    INFO_string_list=list()
    
    
    #loop for updating the VCF_dataframe
    for i in assembly_input_df.index:
        #appending all the lists
        contig_id_list.append(assembly_input_df.loc[i]['scaffold'])
        position_list.append(assembly_input_df['position'].loc[i])
        ref_base_list.append(assembly_input_df['ref_base'].iloc[i])
        var_base_list.append(assembly_input_df['var_base'].loc[i])
        metaimp_id_list.append(assembly_input_df['MetaIMP_ID'].loc[i])


        ref_base=assembly_input_df.loc[i]['ref_base']
        ref_count=assembly_input_df.loc[i][ref_base]
        alt_base=assembly_input_df.loc[i]['var_base']
        alt_count=assembly_input_df.loc[i][alt_base]
        frequency=alt_count/(alt_count+ref_count)

        depth = assembly_input_df['position_coverage'].loc[i]
        information_string="NS=1;DP="+str(depth)+";"+"AF="+str(frequency)+";"
        INFO_string_list.append(information_string)

        #metaimp_id="MetaIMP_"+str(i+1)
        #metaimp_id_list.append(metaimp_id)
        
        
    #update VCF_dataframe    
    vcf_assembly_df['#CHROM']=contig_id_list
    vcf_assembly_df['POS']=position_list
    vcf_assembly_df['ID']=['.']*len(contig_id_list)
    vcf_assembly_df['REF']=ref_base_list
    vcf_assembly_df['ALT']=var_base_list
    vcf_assembly_df['QUAL']=['.']*len(contig_id_list)
    vcf_assembly_df['FILTER']=['.']*len(contig_id_list)
    vcf_assembly_df['INFO']=INFO_string_list
    vcf_assembly_df['MetaIMP_ID']=metaimp_id_list
    
    
    #assembly_input_df['MetaIMP_ID']=metaimp_id_list
    
    filename = os.path.basename(assembly_mapping_result_file)

    outputfilename=os.path.join(final_vcf_path, filename.replace(".csv",".vcf"))
    
    
    #write into .vcf file
    with open(outputfilename, 'w') as f:
        f.write('##fileformat=VCFv4.2\n')
        f.write('##fileDate='+str(datetime.datetime.now())+'\n')
        f.write('##source=metaIMP_v1\n')     
        f.write('##reference=contigs.fasta')
        f.write('##phasing=none')
        f.write('##INFO=<ID=NS,Number=1,Type=Integer,Description=\"Number of Samples With Data\"> \n'+
                '##INFO=<ID=DP,Number=1,Type=Integer,Description=\"Total Depth\"> \n'+
                '##INFO=<ID=AF,Number=A,Type=Float,Description=\"Allele Frequency\"> \n'+
                '##INFO=<ID=AA,Number=1,Type=String,Description=\"Ancestral Allele\"> \n'+
                '##INFO=<ID=DB,Number=0,Type=Flag,Description=\"dbSNP membership, build 129\"> \n'+
                '##INFO=<ID=H2,Number=0,Type=Flag,Description=\"HapMap2 membership\"> \n'+
                '##FILTER=<ID=q10,Description=\"Quality below 10\"> \n'+
                '##FILTER=<ID=s50,Description=\"Less than 50% of samples have data\"> \n'+
                '##FORMAT=<ID=GT,Number=1,Type=String,Description=\"Genotype\"> \n'+
                '##FORMAT=<ID=GQ,Number=1,Type=Integer,Description=\"Genotype Quality\"> \n'+
                '##FORMAT=<ID=DP,Number=1,Type=Integer,Description=\"Read Depth\"> \n'+
                '##FORMAT=<ID=HQ,Number=2,Type=Integer,Description=\"Haplotype Quality\"> \n')
        
            
            
    vcf_assembly_df.to_csv(outputfilename, index=None, mode='a',sep="\t")


#main function to call the vcf_converter function
def main():
    parser = argparse.ArgumentParser(prog='step6_assembly_based_VCF',description='this method converts the assembly based mapping to VCF file')
    subparser = parser.add_subparsers(dest='subcommand',help ='enter the outputfilepath')
    
    vcf_file_parser = subparser.add_parser("vcf_map_assembly", help = "This function converts assembly based mapping result to VCF file")
    vcf_file_parser.add_argument("-i",dest="assembly_mapping_files", type=str, help= 'assembly based input file eg./path/to/assembly_output/ASSEMBLY_SNP_ANNOTATION/somefile.csv')
    vcf_file_parser.add_argument("-o",dest="vcf_file_directory", type=str, help= 'output file destination eg./path/to/OUTPUT_FOLDER')
    
    args = parser.parse_args()
    
    if args.subcommand=='vcf_map_assembly':
        assembly_files=args.assembly_mapping_files
        output_files=args.vcf_file_directory
        print(assembly_files,output_files)
        vcf_converter(assembly_files, output_files)
    else:
        print("Wrong input. Check parameters")
        
    
    
    

if __name__ == "__main__":
        main()





