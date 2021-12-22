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

    fin_assembly = os.path.join(fin_assembly,'assembly_mapping_result.csv')


    #creating dataframes from paths

    df_instrain  = pd.read_csv(instrain_path, sep='\t')
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

    df_inner = pd.merge(df1_eggnog, df2_instrain, left_on = 'location', right_on = 'scaffold', how = 'inner')


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
        if (position>=startpos) & (position<=endpos):
            check_list.append(1)
        else:
            check_list.append(0)
    
    df_final_assembly['in_protein_range']=check_list

    inst_egg_mapping = df_final_assembly.loc[df_final_assembly['in_protein_range']==1]
    
    #saving output
    inst_egg_mapping.to_csv(fin_assembly)

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
