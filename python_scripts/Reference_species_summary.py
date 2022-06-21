##THIS IS THE UPDATED VERSION OF METAIMP_ASSEMBLY_MAPPING ( Step-5 )
##Authors: Kalyan Sahu, Qiuming Yao
##Affiliation: Integrated Digital Omics Lab (IDOL), School of Computing, University of Nebraska-Lincoln


#imports
import Bio
import os
import argparse
import pandas as pd
from Bio import SeqIO


#function for looping



#function for one folder


def species_profile_for_all_files(midas_species_table_path,ref_snp_annotations_folder_path):
    #print("MIDAS SPECIES TEXT FILE PATH IS THIS ::: $$$ \n")
    #print(midas_species_table_path,"\n")
    #get species_profile filename from MIDAS. this is constant
    #midas_species_profile_file=os.path.join(midas_species_table_path,"species_profile.txt")
    #print("MIDAS SPECIES FILE PATH IS :: $$$$$$ \n")
    #print(midas_species_profile_file, "\n")
    
    print("REF_SNP_ANNOTATION_FOLDER IS:::: \n")
    print( ref_snp_annotations_folder_path+" \n ")
    print("^^^^ that is reference snp folder- step 5 output folder \n")

    midas_species_profile=pd.read_csv(midas_species_table_path,sep="\t")

    midas_species_profile.rename(columns = {'species_id': 'species'}, inplace = True)

    id_list=list()
    mutation_count_list=list()

    for i in midas_species_profile.index:
        midas_species =midas_species_profile.loc[i]['species']
        midas_species_id_split=midas_species.rsplit('_')
        id_list.append(midas_species_id_split[-1])  

        #Update 06202022-K.Sahu
        #filename=midas_species+'_patric_midassnps.csv'
        filename=os.path.join(midas_species,"Table_1_coding.csv")

        #Update 06202022-K.Sahu
        #midas_filename=os.path.join(ref_snp_annotations_folder_path,midas_species,filename)
        midas_filename=os.path.join(ref_snp_annotations_folder_path,filename)
        
        #print("step 5 result full path filename::$$$ \n")
        #print("$$$$$$$$$$$$$$$$ \n")
        #print(midas_filename)
    
        if os.path.exists(midas_filename):
            midas_filename_df=pd.read_csv(midas_filename,sep='\t',header=0)
            the_shape=midas_filename_df.shape[0]
            print("THIS FILE IS NON-EMPTY. WE MUST FIND THE SHAPE OF THIS FILE!!!! \n")
            print("THE SHAPE IS",the_shape,"\n")
            mutation_count_list.append(the_shape)
        else:
            mutation_count_list.append(0)



    midas_species_profile['species_id']=id_list
    midas_species_profile['mutation_count']=mutation_count_list
    
    total_species_info=os.path.join(ref_snp_annotations_folder_path,"Table_6_total_mutation.csv")
    midas_species_profile.to_csv(total_species_info, sep=",",index=None)

    #path=ref_snp_annotations_folder_path

    #step_5_results_folder_list=next(os.walk(path))[1]

    

    #step_5_results_folder=os.path.join(ref_snp_annotations_folder_path,species)


 #   for species in step_5_results_folder_list:
 #       step_5_results_folder=os.path.join(ref_snp_annotations_folder_path,species)
 #       
 #       print("step 5 results folder is this \n")
 #       print("$$$$$$$$$$$")
 #       print(step_5_results_folder)
 #       print("$$$$$$$$$")
 #
 #       print("midas_species_profilefile is this :::: \n")
 #       print("$$$$$$$$$$$")
 #       print(midas_species_profile_file)
 #       print("$$$$$$$$$")

 #      species_profile_for_one_file(midas_species_profile_file, step_5_results_folder)
        
        
    #loop through ref_snp mapping output folder.
    #get directory for each species
    #use that to calculate final total species mutations and corresponding details
    
    

#midas_species_profile file is generated by MIDAS tool
##step_5_results_folder is generated for each species by meta_IMP

'''
#def species_profile_for_one_file(midas_species, step_5_results_folder):
    midas_species_profile=pd.read_csv(midas_species,sep="\t")
    
    midas_species_profile.rename(columns = {'species_id': 'species'}, inplace = True)
    
    id_list=list()
    mutation_count_list=list()
    
    for i in midas_species_profile.index:
        midas_species =midas_species_profile.loc[i]['species']
        midas_species_id_split=midas_species.rsplit('_')
        id_list.append(midas_species_id_split[-1])
        
        filename=midas_species+'_patric_midassnps.csv'    
        midas_filename=os.path.join(step_5_results_folder,filename)
        #print("MIDAS FILENAME IS :::: \n")
        #print(midas_filename)


        if os.path.exists(midas_filename):
            midas_filename_df=pd.read_csv(midas_filename,sep='\t',header=0)
            the_shape=midas_filename_df.shape[0]
        #print(the_shape)
            mutation_count_list.append(the_shape)
        else:
            mutation_count_list.append(0)
            
            

    midas_species_profile['species_id']=id_list
    midas_species_profile['mutation_count']=mutation_count_list
    
    total_species_table_abs_filename=os.path.join(step_5_results_folder,"total_species_information.csv")
    midas_species_profile.to_csv(total_species_table_abs_filename, sep=",",index=None)
    
''' 
    #here we finally print out the total species leve information generated by MIDAS AND metaIMP
    

#main function with argpase

def main():
    parser = argparse.ArgumentParser(prog='total_species_evalutation', description='here we are counting mutations per species')
    subparser = parser.add_subparsers(dest='subcommand',help='select from subcommands: species_mut_count')
    
    add_parser = subparser.add_parser("species_mut_count",help="This function is count mutation per species")
    add_parser.add_argument("-m", dest="midas_species_file", type=str, help="species file from midas as input")
    add_parser.add_argument("-n", dest="metaimp_reference_mapping_results_main_folder", type=str, help="this is the main folder where all results for step 5 is saved organzied by species")
    
    
    args = parser.parse_args()
    
    if args.subcommand=='species_mut_count':
        midas_species_folder_path=args.midas_species_file
        step_5_mapping_result=args.metaimp_reference_mapping_results_main_folder
        
        print("MIDAS SPECIES PROFILE AND STeP 5 mapping reuslt are :: \n")
        print(midas_species_folder_path, step_5_mapping_result)
        
        species_profile_for_all_files(midas_species_folder_path, step_5_mapping_result)
    else:
        print("Wrong input. Check parameters")
        

if __name__ == "__main__":
    main()
