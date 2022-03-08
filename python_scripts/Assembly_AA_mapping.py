"""
This program maps mutations in nucleotide sequence to mutations in corresponding amino acid sequence

#ASSEMBLY-PROCESS
##############################################################################
"""

#imports
import pandas as pd
import math
import Bio
import skbio
import os
import argparse

from Bio import SeqIO
from Bio.SeqIO import parse
from skbio import DNA


#functions for calculation
def complement(base):
	""" Complement nucleotide """
	d = {'A':'T', 'T':'A', 'G':'C', 'C':'G'}
	if base in d: return d[base]
	else: return base

def rev_comp(seq):
	""" Reverse complement sequence """
	return(''.join([complement(base) for base in list(seq[::-1])]))

def translate(codon):
	""" Translate individual codon """
	codontable = {
	'ATA':'I', 'ATC':'I', 'ATT':'I', 'ATG':'M',
	'ACA':'T', 'ACC':'T', 'ACG':'T', 'ACT':'T',
	'AAC':'N', 'AAT':'N', 'AAA':'K', 'AAG':'K',
	'AGC':'S', 'AGT':'S', 'AGA':'R', 'AGG':'R',
	'CTA':'L', 'CTC':'L', 'CTG':'L', 'CTT':'L',
	'CCA':'P', 'CCC':'P', 'CCG':'P', 'CCT':'P',
	'CAC':'H', 'CAT':'H', 'CAA':'Q', 'CAG':'Q',
	'CGA':'R', 'CGC':'R', 'CGG':'R', 'CGT':'R',
	'GTA':'V', 'GTC':'V', 'GTG':'V', 'GTT':'V',
	'GCA':'A', 'GCC':'A', 'GCG':'A', 'GCT':'A',
	'GAC':'D', 'GAT':'D', 'GAA':'E', 'GAG':'E',
	'GGA':'G', 'GGC':'G', 'GGG':'G', 'GGT':'G',
	'TCA':'S', 'TCC':'S', 'TCG':'S', 'TCT':'S',
	'TTC':'F', 'TTT':'F', 'TTA':'L', 'TTG':'L',
	'TAC':'Y', 'TAT':'Y', 'TAA':'*', 'TAG':'*',
	'TGC':'C', 'TGT':'C', 'TGA':'*', 'TGG':'W',
	}
	return codontable[str(codon)]


def translate_gene(gene_seq):
    protein_seq=""
    number_of_condons=math.floor(len(gene_seq)/3)
    for i in range(0,number_of_condons):
        condon_seq=gene_seq[3*i:3*i+3]
        aa = translate(condon_seq)
        protein_seq=protein_seq+aa
    return protein_seq

#calcuate mutation position in amino acid
def calculate_mutation_aa(ref_na, alt_na, mutation_na_pos, gene_na):
    #in this code, all positions are one-based
    #mutation_na_pos=5
    #ref_na='A'
    #alt_na='G'
    ref_aa=''
    alt_aa=''
     
    

    codon_num=math.ceil(mutation_na_pos/3)
    na_start=3*codon_num-2
    na_end=na_start+2
    ref_codon = gene_na[na_start-1:na_end]

    if gene_na[mutation_na_pos-1]==ref_na:
        new_gene=gene_na[0:mutation_na_pos-1]+alt_na+gene_na[mutation_na_pos:]
        alt_codon = new_gene[na_start-1:na_end]
        ref_aa=translate(ref_codon)
        alt_aa=translate(alt_codon)
    return ref_aa, alt_aa,codon_num



def amino_acid_mapping(assembly_final_result, vcf, contigs,aa_final_output):
    #get assembly_mapping_final_results
    assembly_mapping_result_file=pd.read_csv(assembly_final_result)
    assembly_cleaner_df=assembly_mapping_result_file[['Description','scaffold','position(0-based)','position_coverage','ID','start_pos(1-based)','end_pos(1-based)','complement','pos_gap','eggNOG_OGs','GOs','EC','MetaIMP_ID']]
    assembly_cleaner_df.rename(columns = {'scaffold':'SCAFFOLD'}, inplace = True)
    
    vcf_file=pd.read_csv(vcf, sep ='\t', header=15)#,comment="##")
    vcf_file.rename(columns = {'#CHROM':'SCAFFOLD'}, inplace = True)
    vcf_file=vcf_file.drop(['ID', 'QUAL', 'FILTER', 'INFO'], axis = 1)
    
    
    with open(contigs) as fasta_file:
        # Will close handle cleanly
        identifiers = []
        lengths = []
        sequence = []
    
        for seq_record in SeqIO.parse(fasta_file, 'fasta'):# (generator)
            identifiers.append(seq_record.id)
            lengths.append(len(seq_record.seq))
            sequence.append(str(seq_record.seq))

    #create columns to save id and sequenece in data frame
    column_names = ["ID","sequence"]
    #create contig dataframe
    df_contig = pd.DataFrame(columns = column_names)
    #parse sequence and it's id into list

    df_contig.sequence = sequence
    df_contig.ID = identifiers
    df_contig.rename(columns = {'ID':'SCAFFOLD'}, inplace = True)
    
    #amino_acid dataframe
    aa_df=pd.merge(pd.merge(df_contig,vcf_file,on='SCAFFOLD'),assembly_cleaner_df,on=('MetaIMP_ID','SCAFFOLD'))
    
    alt_na_list=list()
    ref_na_list=list()
    alt_aa_list = list()
    ref_aa_list = list()
    gene_sequence_list=list()
    protein_sequence_list=list()
    go_list=list()
    ec_list=list()
    description_list=list()
    eggnog_og_list=list()
    mutation_na_pos_list=list()
    mutation_aa_pos_list=list()


    for i in aa_df.index:
        contig_seq=aa_df.loc[i]['sequence']
        start_pos=int(aa_df.loc[i]['start_pos(1-based)'])
        end_pos=int(aa_df.loc[i]['end_pos(1-based)'])
        gene_na = contig_seq[start_pos-1:end_pos]
        go=aa_df.loc[i]['GOs']
        ec=aa_df.loc[i]['EC']
        description=aa_df.loc[i]['Description']
        eggnog_og=aa_df.loc[i]['eggNOG_OGs']
        mutation_na_pos=int(aa_df.loc[i]['POS'])
        ref_na_letter=aa_df.loc[i]['REF']
        alt_na_letter=aa_df.loc[i]['ALT']

        if aa_df.loc[i]['complement']==1:
            #instrain mutation position is based on zero coordinate
            mutation_pos=(mutation_na_pos+1)-start_pos+1
            #relative start position
            ref_aa,alt_aa,aa_pos=calculate_mutation_aa(ref_na_letter, alt_na_letter, mutation_pos, gene_na)
            alt_aa_list.append(alt_aa)
            ref_aa_list.append(ref_aa)
            gene_sequence_list.append(gene_na)
            protein_seq=translate_gene(gene_na)
            protein_sequence_list.append(protein_seq)
            go_list.append(go)
            ec_list.append(ec)
            description_list.append(description)
            eggnog_og_list.append(eggnog_og)
            mutation_na_pos_list.append(mutation_pos)
            mutation_aa_pos_list.append(aa_pos)
            alt_na_list.append(alt_na_letter)
            ref_na_list.append(ref_na_letter)

        elif aa_df.loc[i]['complement']==-1:
            gene_na_rev=rev_comp(gene_na)
            mutation_pos=end_pos-(mutation_na_pos+1)+1
            ref_na_letter_rev=rev_comp(ref_na_letter)
            alt_na_letter_rev=rev_comp(alt_na_letter)
            ref_aa,alt_aa,aa_pos=calculate_mutation_aa(ref_na_letter_rev, alt_na_letter_rev, mutation_pos, gene_na_rev)
            alt_aa_list.append(alt_aa)
            ref_aa_list.append(ref_aa)
            gene_sequence_list.append(gene_na_rev)
            protein_seq=translate_gene(gene_na_rev)
            protein_sequence_list.append(protein_seq)
            go_list.append(go)
            ec_list.append(ec)
            description_list.append(description)
            eggnog_og_list.append(eggnog_og)
            mutation_na_pos_list.append(mutation_pos)
            mutation_aa_pos_list.append(aa_pos)
            alt_na_list.append(alt_na_letter_rev)
            ref_na_list.append(ref_na_letter_rev)

    aa_df['eggNOG_OGs']=eggnog_og_list
    aa_df['Description']=description_list
    aa_df['GO']=go_list
    aa_df['EC']=ec_list
    aa_df['Protein_Seq']=protein_sequence_list
    aa_df['Gene Seq']=gene_sequence_list
    aa_df['ALT_AA']=alt_aa_list
    aa_df['REF_AA']=ref_aa_list
    aa_df['ALT_NA']=alt_na_list
    aa_df['REF_NA']=ref_na_list
    aa_df['NA_Mutatation_Pos']=mutation_na_pos_list
    aa_df['AA_Mutation_Pos']=mutation_aa_pos_list

    #drop contig column
    aa_df=aa_df.drop(['sequence'], axis=1)

    final_assembly_AA = os.path.join(aa_final_output,'assembly_AA_mapping_result.csv')
    aa_df.to_csv(final_assembly_AA,index=None)

    
    
    
    
    
            
 
def main():
    
    parser = argparse.ArgumentParser(prog='step5_assembly_based',description='this method executes the assembly based amino acid mapping')
    subparser = parser.add_subparsers(dest='subcommand',help ='following files are the input:1)aaembly_mapping_final_result 2) vcf file 3) contigs.fasta')
    
    amino_acid_parser=subparser.add_parser("aa_map",help="This function is to map amino acids with mutations")
   
    amino_acid_parser.add_argument("-a", dest="assembly_mapping_file", type=str, help="assembly file eg./path/to/assembly_mapping_result.csv as input")
    amino_acid_parser.add_argument("-v", dest="vcf_file", type=str, help="vcf file eg. /path/to/assembly_mapping_result.vcf as input")
    amino_acid_parser.add_argument("-c", dest="contigs_file", type=str, 
                                         help="merged file obtained from checkm as input eg. /path/to/contigs.fasta")
    amino_acid_parser.add_argument("-o", dest="output_file_path", type=str, help="output file path")
    
    args = parser.parse_args()
    
    if args.subcommand=='aa_map':
        aa_map_file = args.assembly_mapping_file
        vcf_file = args.vcf_file
        contigs_file = args.contigs_file
        assembly_aa_file= args.output_file_path
        print(aa_map_file,vcf_file,contigs_file,assembly_aa_file)
        amino_acid_mapping(aa_map_file, vcf_file, contigs_file, assembly_aa_file)
    else:
        print("Wrong input. Check parameters")

if __name__ == "__main__":
    main()
