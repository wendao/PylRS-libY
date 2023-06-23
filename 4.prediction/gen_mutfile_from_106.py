import sys
import itertools
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

#save mutfile
def write_mutfile( fn, muts ):
    fp = open( fn+".mutfile", 'w' )
    N = len(muts)
    fp.write( "total %d\n%d\n" % (N,N) )
    for nat, pos, mut in muts:
        if pos>-1 and pos<max_L:
            fp.write( "%s %d %s\n" % (nat, pos, mut) )
        else:
            print("Warning!")
    fp.close()

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

NAT = { #106
 302 : "A",
 305 : "L",
 306 : "Y",
 309 : "A",
 346 : "N",
 348 : "V",
 384 : "F",
 401 : "V",
 417 : "W",
}

#106, LANVF
fasta_seqs = SeqIO.parse(open('../1.strcutures/106.fasta'),'fasta')
for fas in fasta_seqs:
  B1 = fas.seq

for pos in NAT.keys():
  n = NAT[pos]
  for a in AA.keys():
    if n == a: continue	
    print( n, pos, a )
    label = str(pos)+a
    write_mutfile( "mut_ssm/"+label, [(n, pos-shift, a)] )

