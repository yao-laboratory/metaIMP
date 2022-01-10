"""
This program allows the user to convert the assembly and reference based output files
to VCF file format

#ASSEMBLY_VCF

##############################################################################
"""


#IMPORTS

import pandas as pd


#CREATE A FUNCTION TO CALL IN 2 ARGUMENTS

def vcf_converter(assembly_mapping_result, final_vcf_file):
    #defining paths to final output from assembly_mapping and vcf_output_file
    assembly_mapping_result=os.path.join(assembly_mapping_result,'assembly_mapping_result.csv')
    assembly_input_df= pd.read_csv(assembly_mapping_result)
    
    
    vcf_column_names = ['#CHROM', 'POS','ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'MetaIMP_ID']
    vcf_assembly_df = pd.DataFrame(columns = vcf_column_names)
    
    
    contig_id_list = list()
    position_list = list()
    ref_base_list = list()
    var_base_list = list()
    metaimp_id_list = list()
    INFO_string_list=list()
    
    
    
    for i in assembly_input_df.index:
        contig_id_list.append(assembly_input_df.loc[i]['scaffold'])
        position_list.append(assembly_input_df['position'].loc[i])
        ref_base_list.append(assembly_input_df['ref_base'].iloc[i])
        var_base_list.append(assembly_input_df['var_base'].loc[i])

        ref_base=assembly_input_df.loc[i]['ref_base']
        ref_count=assembly_input_df.loc[i][ref_base]
        alt_base=assembly_input_df.loc[i]['var_base']
        alt_count=assembly_input_df.loc[i][alt_base]
        frequency=alt_count/(alt_count+ref_count)

        depth = assembly_input_df['position_coverage'].loc[i]
        information_string="NS=1;DP="+str(depth)+";"+"AF="+str(frequency)+";"
        INFO_string_list.append(information_string)

        metaimp_id="MetaIMP_"+str(i+1)
        metaimp_id_list.append(metaimp_id)
        
        
    vcf_assembly_df['#CHROM']=contig_id_list
    vcf_assembly_df['POS']=position_list
    vcf_assembly_df['ID']=['.']*len(contig_id_list)
    vcf_assembly_df['REF']=ref_base_list
    vcf_assembly_df['ALT']=var_base_list
    vcf_assembly_df['QUAL']=['.']*len(contig_id_list)
    vcf_assembly_df['FILTER']=['.']*len(contig_id_list)
    vcf_assembly_df['INFO']=INFO_string_list
    vcf_assembly_df['MetaIMP_ID']=metaimp_id_list
    
    
    assembly_input_df['MetaIMP_ID']=metaimp_id_list
    
    outputfilename=join(assembly_mapping_result,+"_VCF")

            with open(outputfilename, 'w') as f:
                f.write('# This is my comment\n')
                f.write('# This is my comment\n')
            
            
    assembly_input_df.to_csv(outputfilename, index=None, mode='a',sep="\t")

def main():
    parser = argparse.ArgumentParser(prog='step5_assembly_based',description='this method converts the assembly based mapping to VCF file')
    subparser = parser.add_subparsers(dest='subcommand',help ='enter the outputfilepath')
    
    vcf_file_parser = subparser.add_argument("vcf_map_assembly", help = "This function converts assembly based mapping result to VCF file")
    vcf_file_parser.add_argument("-i",dest="assembly_mapping_files", type=str, help= 'assembly based input file eg./path/to/assembly_output/ASSEMBLY_SNP_ANNOTATION')
    vcf_file_parser.add_argument("-o",dest="vcf_files", type=str, help= 'output file destination eg./path/to/OUTPUT_FOLDER')
    
    args = parser.parse_args()
    
    if args.subcommand=='vcf_map_assembly':
        assembly_files=args.assembly_mapping_files
        output_files=args.vcf_files
        print(assembly_files,output_files)
        vcf_converter_all_files(assembly_files, output_files)
    else:
        print("Wrong input. Check parameters")

if __name__ == "__main__":
        main()



