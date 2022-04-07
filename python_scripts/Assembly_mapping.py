##THIS IS THE UPDATED VERSION OF METAIMP_ASSEMBLY_MAPPING ( Step-5 )
##Authors: Kalyan Sahu, Qiuming Yao
##Affiliation: Integrated Digital Omics Lab (IDOL), School of Computing, University of Nebraska-Lincoln


#imports
import Bio
import os
import argparse
import pandas as pd
from Bio import SeqIO

#create a function to call in 4 arguments

def assembly_mapping(instrain,eggnog,mergedfile,fin_assembly):
    
    #paths
    #instrain_path = os.path.join(instrain, 'instrain_SNVs.tsv')
    print(instrain)

    #eggnog_path = os.path.join(eggnog, 'eggnog_results.emapper.annotations')
    print(eggnog)

    #merged_file = os.path.join(mergedfile, 'mergedfile.fna')
    print(mergedfile)
    
    #this is where the final assembly result is stored
    fin_assembly_coding = os.path.join(fin_assembly,'Table_1_assembly_mapping_result_coding.csv')
    fin_assembly_noncoding = os.path.join(fin_assembly,'Table_2_assembly_mapping_result_noncoding.csv')
    #creating dataframes from paths

    instrain  = pd.read_csv(instrain, sep='\t')
    eggnog    = pd.read_csv(eggnog,sep ='\t', skiprows =  2, header =2,skipfooter= 3, engine='python')
    records   = SeqIO.parse(mergedfile, 'fasta')
    
    eggnog.rename(columns= {'#query': 'protein_id'}, inplace = True)
    
    #binning merged file manipulation 

    column_names = ["protein_id","start_pos","end_pos","sequence","complement",'pos_gap']
    mergedfile = pd.DataFrame(columns = column_names)
    #list for splitting mergedfile.fna
    #creating multiple lists to add the following information
    start_pos = list()
    end_pos = list()
    split = list()
    seq_ID = list()
    sequence = list()
    complement = list()
    
    
    for seq_record in records:
        
        split = seq_record.description.split(" # ")
        se = seq_record.seq
        sequence.append(se)
        seq_ID.append(split[0])
        start_pos.append(split[1])
        end_pos.append(split[2])
        complement.append(split[3])
        contig=split[0].rsplit("_",1)[0]
        contig_list.append(contig)
    #1=original/forward -1=reverse_complement   
    #add split records to mergedfile_dataframe

    mergedfile['start_pos'] = start_pos           
    mergedfile['end_pos'] = end_pos
    mergedfile['sequence'] = sequence
    mergedfile['protein_id'] = seq_ID
    mergedfile['complement'] = complement
    mergedfile['pos_gap'] = mergedfile['end_pos'].astype(int) - mergedfile['start_pos'].astype(int)
    mergedfile['scaffold'] = contig_list
    
    

    #merge between checkm data and eggnog- gives all proteins
    all_proteins = pd.merge (mergedfile, eggnog, on = 'protein_id', how = 'left')
    all_proteins_file = os.path.join(fin_assembly,'Table_3_assembly_complete_protein.csv')
    all_proteins.to_csv(all_proteins_file,index=None)
    #save all_proteins information

    #merge between all proteins and instrain

    final_assembly = pd.merge (instrain , all_proteins,  on = 'scaffold', how = 'left')
    

    #declare two new dfs to save coding non-coding mutations      
    final_assembly_noncoding_mutations=pd.DataFrame()
    final_assembly_coding_mutations=pd.DataFrame()
    
    final_assembly = final_assembly.dropna(subset=['start_pos', 'end_pos'])
    
    coding_region=list()
    
    
    
    for i in final_assembly.index:
        this_record = final_assembly.loc[i]
        position = int(this_record['position'])
        startpos = int(this_record['start_pos'])
        endpos = int(this_record['end_pos'])
        #position from instrain is zero-based, but startpos and endpos from contig are one-based

        if ((position+1)>=startpos) & ((position+1)<=endpos):
            coding_region.append(1)

        else:
            coding_region.append(0)


    
    final_assembly['coding_region']=coding_region

   
    final_assembly_noncoding_mutations=final_assembly.loc[final_assembly['coding_region']==0]
    final_assembly_coding_mutations=final_assembly.loc[final_assembly['coding_region']==1]  
    
    final_assembly_noncoding_mutations.rename(columns = {'start_pos':'start_pos(1-based)','end_pos':'end_pos(1-based)','position':'position(0-based)'}, inplace = True)
    final_assembly_coding_mutations.rename(columns = {'start_pos':'start_pos(1-based)','end_pos':'end_pos(1-based)','position':'position(0-based)'}, inplace = True)
    
    noncoding_col=19
    final_assembly_noncoding_mutations=final_assembly_noncoding_mutations.iloc[: , :noncoding_col]
    final_assembly_noncoding_mutations=final_assembly_noncoding_mutations.drop_duplicates()


    metaimp_id_coding_list = list()
    for i in final_assembly_coding_mutations.index:
        metaimp_id="MetaIMP_"+str(i+1)
        metaimp_id_coding_list.append(metaimp_id)
    final_assembly_coding_mutations['MetaIMP_ID']=metaimp_id_coding_list

    metaimp_id_noncoding_list=list()
    for i in final_assembly_noncoding_mutations.index:
        metaimp_id="MetaIMP_"+str(i+1)
        metaimp_id_noncoding_list.append(metaimp_id)
    final_assembly_noncoding_mutations['MetaIMP_ID']=metaimp_id_noncoding_list


    final_assembly_noncoding_mutations.to_csv(fin_assembly_noncoding,index=None)
    final_assembly_coding_mutations.to_csv(fin_assembly_coding,index=None)
    
    
def main():
    
    parser = argparse.ArgumentParser(prog='META_IMP_assembly_based',description='this method executes the assembly based mapping')
    subparser = parser.add_subparsers(dest='subcommand',help ='enter the eggnog and instrain file names')
       
    
    assembly_mapping_parser = subparser.add_parser("a_map",help="This function is to map snps with annotations")
    assembly_mapping_parser.add_argument("-i", dest="instrain_file", type=str, help="instrain file eg./path/to/instrain_SNVs.tsv as input")
    assembly_mapping_parser.add_argument("-e", dest="eggnog_file", type=str, help="eggnog file eg. /path/to/eggnog_results.emapper.annotations as input")
    assembly_mapping_parser.add_argument("-m", dest="mergedfile_file", type=str, 
                                         help="merged file obtained from checkm as input eg. /path/to/mergedfile.fna")
    assembly_mapping_parser.add_argument("-o", dest="output_file_path", type=str, help="output file path")
    
    
    
          #command_line = "a_map -i /somepath -e /somepath -m /somepath -o /somepath".split()
          #print(command_line)
          #args= parser.parse_args(command_line)
    
    args = parser.parse_args()


    if args.subcommand=='a_map':
        instrain = args.instrain_file
        eggnog = args.eggnog_file
        mergedfile = args.mergedfile_file
        fin_assembly = args.output_file_path
        print(instrain,eggnog,mergedfile,fin_assembly)
        assembly_mapping(instrain,eggnog,mergedfile,fin_assembly)
    else:
        print("Wrong input. Check parameters")

if __name__ == "__main__":
    main()

'''
import Bio
import os
import argparse

from Bio import SeqIO

import pandas as pd      


#create a function to call in 4 arguments

def assembly_mapping(instrain,eggnog,mergedfile,fin_assembly):
    #defining paths to instrain,eggnog and mergedfile.fna

    #paths
    #instrain_path = os.path.join(instrain, 'instrain_SNVs.tsv')
    print(instrain)

    #eggnog_path = os.path.join(eggnog, 'eggnog_results.emapper.annotations')
    print(eggnog)

    #merged_file = os.path.join(mergedfile, 'mergedfile.fna')
    print(mergedfile)
    
    #this is where the final assembly result is stored
    fin_assembly = os.path.join(fin_assembly,'assembly_mapping_result.csv')


    #creating dataframes from paths

    df_instrain  = pd.read_csv(instrain, sep='\t')
    df_eggnog    = pd.read_csv(eggnog,sep ='\t', skiprows =  2, header =2)
    records      = SeqIO.parse(mergedfile, 'fasta')


    #number of rows to drop from eggnog file

    n = 3

    # dropping last n rows using drop

    df_eggnog.drop(df_eggnog.tail(n).index, inplace = True)

    #saving position and node info of protein

    pos = '_'

    df_eggnog[["location","protein_id"]] = df_eggnog["#query"].str.rsplit(pos, 1, expand = True)

    #merged eggnog and instrain dataframes - inner merge

    df_inner = pd.merge(df_eggnog, df_instrain, left_on = 'location', right_on = 'scaffold', how = 'inner')


    #manipulation of mergedfile
    #binning merged file manipulation

    column_names = ["ID","start_pos","end_pos","sequence","complement",'seq_len','pos_gap']

    df_mergedfile = pd.DataFrame(columns = column_names)

    #creating multiple lists to add the following information
    start_pos = list()
    end_pos = list()
    split = list()
    seq_ID = list()
    sequence = list()
    complement = list()

    #splitting records obtained from mergedfile.fna and appending it to the lists defined above

    for seq_record in records:
        #print(seq_record)
        split = seq_record.description.split(" # ")
        se = seq_record.seq
        sequence.append(se)
        #print(se)
        seq_ID.append(split[0])
        start_pos.append(split[1])
        end_pos.append(split[2])
        complement.append(split[3])
        #1=original/forward -1=reverse_complement
    #add split records to mergedfile_dataframe
    
    df_mergedfile.start_pos = start_pos
    df_mergedfile.end_pos = end_pos
    df_mergedfile.sequence = sequence
    df_mergedfile.ID = seq_ID
    df_mergedfile.complement = complement
    #df.seq_len = df.sequence.str.len()
    df_mergedfile.pos_gap = df_mergedfile.end_pos.astype(int) - df_mergedfile.start_pos.astype(int)
    df_mergedfile[["location","protein_id"]] = df_mergedfile["ID"].str.rsplit(pos, 1, expand = True)

    #inner merge again to create a final assembly dataframe

    df_final_assembly = pd.merge(df_inner,df_mergedfile, left_on = '#query', right_on ='ID', how = 'inner')

    #creating final checklist. this ensures that the mutation position achieved lies between the start and end position

    check_list=[]
    for i in df_final_assembly.index:
        this_record=df_final_assembly.loc[i]
        position = int(this_record['position'])
        startpos = int(this_record['start_pos'])
        endpos = int(this_record['end_pos'])
        #position from instrain is zero-based, but startpos and endpos from contig are one-based
        if ((position+1)>=startpos) & ((position+1)<=endpos):
            check_list.append(1)
        else:
            check_list.append(0)
    
    df_final_assembly['in_protein_range']=check_list
    
    metaimp_id_list = list()
    for i in df_final_assembly.index:
        metaimp_id="MetaIMP_"+str(i+1)
        metaimp_id_list.append(metaimp_id)
    df_final_assembly['MetaIMP_ID']=metaimp_id_list
    df_final_assembly.rename(columns = {'start_pos':'start_pos(1-based)','end_pos':'end_pos(1-based)','position':'position(0-based)'}, inplace = True)

    inst_egg_mapping_coding = df_final_assembly.loc[df_final_assembly['in_protein_range']==1]
    inst_egg_mapping_non_coding = df_final_assembly.loc[df_final_assembly['in_protein_range']==0]

    #metaimp_id_list = list()
    #for i in df_final_assembly.index:
    #    metaimp_id="MetaIMP_"+str(i+1)
    #    metaimp_id_list.append(metaimp_id)
    #df_final_assembly['MetaIMP_ID']=metaimp_id_list
    
    #df_final_assembly.rename(columns = {'start_pos':'start_pos(1-based)','end_pos':'end_pos(1-based)','position':'position(0-based)'}, inplace = True)

    #saving output
    inst_egg_mapping_coding.to_csv(fin_assembly,index=None)
    inst_egg_mapping_non_coding.to_csv(fin_assembly,index=None)
    
   

def main():
    
    parser = argparse.ArgumentParser(prog='step5_assembly_based',description='this method executes the assembly based mapping')
    subparser = parser.add_subparsers(dest='subcommand',help ='enter the eggnog and instrain file names')
       
    
    assembly_mapping_parser = subparser.add_parser("a_map",help="This function is to map snps with annotations")
    assembly_mapping_parser.add_argument("-i", dest="instrain_file", type=str, help="instrain file eg./path/to/instrain_SNVs.tsv as input")
    assembly_mapping_parser.add_argument("-e", dest="eggnog_file", type=str, help="eggnog file eg. /path/to/eggnog_results.emapper.annotations as input")
    assembly_mapping_parser.add_argument("-m", dest="mergedfile_file", type=str, 
                                         help="merged file obtained from checkm as input eg. /path/to/mergedfile.fna")
    assembly_mapping_parser.add_argument("-o", dest="output_file_path", type=str, help="output file path")
    
    
    
          #command_line = "a_map -i /somepath -e /somepath -m /somepath -o /somepath".split()
          #print(command_line)
          #args= parser.parse_args(command_line)
    
    args = parser.parse_args()


    if args.subcommand=='a_map':
        instrain = args.instrain_file
        eggnog = args.eggnog_file
        mergedfile = args.mergedfile_file
        fin_assembly = args.output_file_path
        print(instrain,eggnog,mergedfile,fin_assembly)
        assembly_mapping(instrain,eggnog,mergedfile,fin_assembly)
    else:
        print("Wrong input. Check parameters")

if __name__ == "__main__":
    main()
'''
