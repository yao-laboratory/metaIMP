"""
This program allows the user to convert the reference and reference ased output files
to VCF file format

#reference_VCF

##############################################################################
"""


#IMPORTS

import pandas as pd


#CREATE A FUNCTION TO CALL IN 2 ARGUMENTS
#all files in REFERENCE_SNPS_ANNOTATION folder

def vcf_converter_all_files(reference_snp_annotations, output_path):
    snp_annotation_files_list=os.listdir(reference_snp_annotations)
    
    
    for files in snp_annotation_files_list:
        vcf_file_input=files
        vcf_converter(vcf_file_input, output_path)

#CREATE A FUNCTION TO CALL IN 2 ARGUMENTS
#single file

def vcf_converter(reference_mapping_fullpath_filename, final_vcf_output_file): 
    #defining paths to final output from reference_mapping and vcf_output_file
    reference_input_df=pd.read_csv(reference_mapping_fullpath_filename,sep=",",index=None)
    
    
    if reference_input_df.shape[0] != 0:
        print(reference_mapping_fullpath_filename," is not empty, converting into VCF")
        vcf_column_names = ['#CHROM', 'POS','ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'MetaIMP_ID']
        vcf_reference_df = pd.DataFrame(columns=vcf_column_names)
        
        #create empty lists to store vcf_column_information
        contig_id_list = list()
        position_list = list()
        ref_base_list = list()
        var_base_list = list()
        INFO_string_list=list()
        metaimp_id_list=list()
        for i in reference_input_df.index:
            contig_id_list.append(reference_input_df['ref_id'].loc[i])
            position_list.append(reference_input_df['ref_pos'].loc[i])

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
            metaimp_id="MetaIMP_"+str(i+1)
            metaimp_id_list.append(metaimp_id)
            
            vcf_reference_df['#CHROM']=contig_id_list
            vcf_reference_df['POS']=position_list
            vcf_reference_df['ID']=['.']*len(contig_id_list)
            vcf_reference_df['REF']=ref_base_list
            vcf_reference_df['ALT']=var_base_list
            vcf_reference_df['QUAL']=['.']*len(contig_id_list)
            vcf_reference_df['FILTER']=['.']*len(contig_id_list)
            vcf_reference_df['INFO']=INFO_string_list
            vcf_reference_df['MetaIMP_ID']=metaimp_id_list
                       
            reference_input_df['MetaIMP_ID']=metaimp_id_list
            
            
            
            outputfilename=join(reference_mapping_fullpath_filename,+"_VCF")

            with open(outputfilename, 'w') as f:
                f.write('# This is my comment\n')
                f.write('# This is my comment\n')
            
            
            vcf_reference_df.to_csv(outputfilename, index=None, mode='a',sep="\t")

                      
    else:
        print(reference_mapping,"this midas_patric_mapping file is empty. skipping this file")
   
def main():
    parser = argparse.ArgumentParser(prog='step5_reference_based',description='this method converts the reference based mapping to VCF file')
    subparser = parser.add_subparsers(dest='subcommand',help ='enter the outputfilepath')
    
    vcf_file_parser = subparser.add_argument("vcf_map_reference", help = "This function converts file reference based mapping species file to VCF format")
    vcf_file_parser.add_argument("-i",dest="reference_mapping_files", type=str, help= 'reference based input file eg./path/to/REFERENCE_SNP_ANNOTATION')
    vcf_file_parser.add_argument("-o",dest="vcf_files", type=str, help= 'output file destination eg./path/to/OUTPUT_FOLDER')
    
    args = parser.parse_args()
    if args.subcommand=='vcf_map_reference':
        reference_files=args.reference_mapping_files
        output_files=args.vcf_files
        print(reference_files,output_files)
        vcf_converter_all_files(reference_files, output_files)
    else:
        print("Wrong input. Check parameters")

if __name__ == "__main__":
        main()
    
    
    
    

    
    
