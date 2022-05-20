#!/usr/bin/env python
# coding: utf-8

# In[1]:


"""
This program allows the user to convert the reference and reference ased output files
to VCF file format

#reference_VCF

##############################################################################
"""


#IMPORTS

import pandas as pd
import datetime
import argparse
import os


#CREATE A FUNCTION TO CALL IN 2 ARGUMENTS
#all files in REFERENCE_SNPS_ANNOTATION folder




def vcf_converter_all_files(reference_snp_annotation_folder, output_path):
    
    path=reference_snp_annotation_folder
    dir_list=next(os.walk(path))[1]
    #os.path.join(path, "User/Desktop", "file.txt"
    for species in dir_list:
        #filename=species+"_patric_midassnps.csv"
        filename="Table_1_reference_mapping"+species+"coding.csv"
        print("*********************************")
        print("\n \n \n ")
        print("THIS IS FILENAME WHICH IS INPUT TO VCF CONVERTER:", filename)
        final_filename=os.path.join(reference_snp_annotation_folder,species,filename)
        output_path=os.path.join(reference_snp_annotation_folder,species)
        vcf_converter(final_filename, output_path)

    ##NEWLY COPIED.

    #dir_list=list()

    #for root, dirs, files in os.walk(".", topdown=False):
    #    for name in files:
    #        filename=os.path.join(root, name)
    #        print(filename)
    #    for name in dirs:
    #        dir_list=os.path.join(root, name)
    #        print(dir_list)
    #        if filename.endswith(".csv"):
    #            #vcf_file_input=os.path.join(dir_list, filename)
    #            vcf_converter(dir_list, output_path)
            #list_of_dir=next(os.walk('.'))[1] #this is a list
    #for species in range (0, len(list_of_dir)):
    #snp_annotation_files_list=os.listdir(species)
    #print(snp_annotation_files)
        
    #for filename in snp_annotation_files_list:
            #if filename.endswith(".csv"):
            #    vcf_file_input=os.path.join(reference_snp_annotation_folder, filename)
            #    vcf_converter(vcf_file_input, output_path)




def vcf_converter_all_files_old(reference_snp_annotation_folder, output_path):

    snp_annotation_files_list=os.listdir(reference_snp_annotation_folder)
       
    for filename in snp_annotation_files_list:
        if filename.endswith(".csv"):
            vcf_file_input=os.path.join(reference_snp_annotation_folder, filename)
            vcf_converter(vcf_file_input, output_path)

#CREATE A FUNCTION TO CALL IN 2 ARGUMENTS
#single file

def vcf_converter(reference_mapping_fullpath_filename, final_vcf_path): 
    #defining paths to final output from reference_mapping and vcf_output_file
    print("start reading"+reference_mapping_fullpath_filename)
    reference_input_df=pd.read_csv(reference_mapping_fullpath_filename)
    print("finish reading"+reference_mapping_fullpath_filename)
    
    if reference_input_df.shape[0] != 0:
        print(reference_mapping_fullpath_filename," is not empty, converting into VCF")
                
        #define vcf column names: https://samtools.github.io/hts-specs/VCFv4.2.pdf
        #define dataframe for VCF column
        
        vcf_column_names = ['#CHROM', 'POS','ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO',] #'MetaIMP_ID']
        vcf_reference_df = pd.DataFrame(columns=vcf_column_names)
        
        #create empty lists for the following columns:
        contig_id_list = list()
        position_list = list()
        ref_base_list = list()
        var_base_list = list()
        INFO_string_list=list()
        metaimp_id_list=list()

        #loop for updating the VCF_dataframe

        for i in reference_input_df.index:
            contig_id_list.append(reference_input_df['ref_id'].loc[i])
            position_list.append(reference_input_df['ref_pos'].loc[i])
            metaimp_id_list.append(reference_input_df['MetaIMP_ID'].loc[i])
            depth=reference_input_df['depth'].loc[i]
            count=dict()
            count['A']=reference_input_df.loc[i]['count_a']
            count['C']=reference_input_df.loc[i]['count_c']
            count['T']=reference_input_df.loc[i]['count_t']
            count['G']=reference_input_df.loc[i]['count_g']
            ref_base=reference_input_df.loc[i]['ref_allele']
            ref_base_list.append(ref_base)
            ref_count=count[ref_base]
            frequency_dict=dict()
            if count['A']>0 and ref_base!='A':
                frequency=count['A']/(count['A']+ref_count)
                frequency_dict['A']=frequency
            if count['C']>0 and ref_base!='C':
                frequency=count['C']/(count['C']+ref_count)
                frequency_dict['C']=frequency
            if count['T']>0 and ref_base!='T':
                frequency=count['T']/(count['T']+ref_count)
                frequency_dict['T']=frequency
            if count['G']>0 and ref_base!='G':
                frequency=count['G']/(count['G']+ref_count)
                frequency_dict['G']=frequency

            ALT_bases=','.join(list(frequency_dict.keys()))
            value_list= [str(frequency_dict[key]) for key in frequency_dict.keys()]
            joined_value_string=','.join(value_list)
            AF_string="AF="+joined_value_string

            var_base_list.append(ALT_bases)

            information_string="NS=1;DP="+str(depth)+";"+AF_string+";"
            INFO_string_list.append(information_string)
            
            #metaimp_id="MetaIMP_"+str(i+1)
            #metaimp_id_list.append(metaimp_id)
        

        #update VCF_dataframe
        vcf_reference_df['#CHROM']=contig_id_list
        vcf_reference_df['POS']=position_list
        vcf_reference_df['ID']=['.']*len(contig_id_list)
        vcf_reference_df['REF']=ref_base_list
        vcf_reference_df['ALT']=var_base_list
        vcf_reference_df['QUAL']=['.']*len(contig_id_list)
        vcf_reference_df['FILTER']=['.']*len(contig_id_list)
        vcf_reference_df['INFO']=INFO_string_list
        vcf_reference_df['MetaIMP_ID']=metaimp_id_list
                       
        
            
            
        filename = os.path.basename(reference_mapping_fullpath_filename)
        outputfilename=os.path.join(final_vcf_path, filename.replace(".csv",".vcf"))
        

        #write into .vcf file

        with open(outputfilename, 'w') as f:
            f.write('##fileformat=VCFv4.2\n')
            f.write('##fileDate='+str(datetime.datetime.now())+'\n')
            f.write('##source=metaIMP_v1\n')     
            f.write('##reference=http://lighthouse.ucsf.edu/MIDAS/midas_db_v1.2.tar.gz\n')
            f.write('##phasing=none\n')
            f.write('##INFO=<ID=NS,Number=1,Type=Integer,Description=\"Number of Samples With Data\"> \n'+
                    '##INFO=<ID=DP,Number=1,Type=Integer,Description=\"Total Depth\"> \n' +
                    '##INFO=<ID=AF,Number=A,Type=Float,Description=\"Allele Frequency\"> \n' +
                    '##INFO=<ID=AA,Number=1,Type=String,Description=\"Ancestral Allele\"> \n' +
                    '##INFO=<ID=DB,Number=0,Type=Flag,Description=\"dbSNP membership, build 129\"> \n' +
                    '##INFO=<ID=H2,Number=0,Type=Flag,Description=\"HapMap2 membership\"> \n' +
                    '##FILTER=<ID=q10,Description=\"Quality below 10\"> \n' +
                    '##FILTER=<ID=s50,Description=\"Less than 50% of samples have data\"> \n' +
                    '##FORMAT=<ID=GT,Number=1,Type=String,Description=\"Genotype\"> \n' +
                    '##FORMAT=<ID=GQ,Number=1,Type=Integer,Description=\"Genotype Quality\"> \n'+
                    '##FORMAT=<ID=DP,Number=1,Type=Integer,Description=\"Read Depth\"> \n'+
                    '##FORMAT=<ID=HQ,Number=2,Type=Integer,Description=\"Haplotype Quality\"> \n')
           
        vcf_reference_df.to_csv(outputfilename, index=None, mode='a',sep="\t")

                      
    else:
        print(reference_mapping,"this midas_patric_mapping file is empty. skipping this file")
   
#main function to call the vcf_converter function

def main():
    parser = argparse.ArgumentParser(prog='step6_reference_based',description='this method converts the reference based mapping to VCF file')
    subparser = parser.add_subparsers(dest='subcommand',help ='enter the outputfilepath')
    
    vcf_file_parser = subparser.add_parser("vcf_map_reference", help = "This function converts file reference based mapping species file to VCF format")
    vcf_file_parser.add_argument("-i",dest="reference_mapping_files_folder", type=str, help= 'reference based input folder containing all csv files eg./path/to/REFERENCE_SNP_ANNOTATION')
    vcf_file_parser.add_argument("-o",dest="vcf_file_path", type=str, help= 'output file destination eg./path/to/OUTPUT_FOLDER')
    
    args = parser.parse_args()
    if args.subcommand=='vcf_map_reference':
        reference_files=args.reference_mapping_files_folder
        output_files=args.vcf_file_path
        print(reference_files,output_files)
        vcf_converter_all_files(reference_files, output_files)
    else:
        print("Wrong input. Check parameters")
    
if __name__ == "__main__":
        main()

