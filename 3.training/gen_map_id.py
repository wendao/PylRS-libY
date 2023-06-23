import sys
from Bio import SeqIO
from Bio.Seq import Seq

shift = 185
max_L = 269

#get mutations between two seqs
def get_muts( ref, seq, p0=0 ):
    muts = []
    for i, j in zip(ref, seq):
        p0 = p0 + 1
        if i != j:
            #print(i, p0, j)
            muts.append((i, p0, j))
    return muts

#mutate refseq to new seq
def put_muts( ref, muts, p0=0 ):
    seq = ref[:]
    p0 = p0 - 1
    for nat, pos, mut in muts:
        assert( seq[pos+p0] == nat )
        seq = seq[:pos+p0] + mut + seq[pos+p0+1:]
    return seq

#B1, FMGGF
fasta_seqs = SeqIO.parse(open('./B1.fasta'),'fasta')
for fas in fasta_seqs:
    B1 = fas.seq

AA = {
  'G' : "GLY",
  'A' : "ALA",
  'S' : "SER",
  'P' : "PRO",
  'V' : "VAL",
  'T' : "THR",
  'C' : "CYS",
  'L' : "LEU",
  'I' : "ILE",
  'N' : "ASN",
  'D' : "ASP",
  'Q' : "GLN",
  'K' : "LYS",
  'E' : "GLU",
  'M' : "MET",
  'H' : "HIS",
  'F' : "PHE",
  'R' : "ARG",
  'Y' : "TYR",
  'W' : "TRP",
}

#native seq
fasta_seqs = SeqIO.parse(open('MmPylRS.fasta'),'fasta')
for fas in fasta_seqs:
    WT = fas.seq

lines = open('X-mutations.txt', 'r').readlines()
for l in lines:
    es = l.split()
    muts = []
    label = es[0]
    if len(es) == 3:
      for mut in es[2].split('|'):
          muts.append((mut[0], int(mut[1:-1]), mut[-1]))

    mut_seq = put_muts( WT, muts, -shift )
    #from B1 to newseq
    muts_F = get_muts( B1, mut_seq, 0 )

    tag = "MUT"
    for mut in muts_F:
        tag += "_"+str(mut[1])+AA[mut[2]]

    print label, tag, mut_seq
