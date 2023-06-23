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

#native seq
fasta_seqs = SeqIO.parse(open('../AF2/fasta/MmPylRS.fasta'),'fasta')
for fas in fasta_seqs:
    WT = fas.seq
#B1, FMGGF
fasta_seqs = SeqIO.parse(open('./B1.fasta'),'fasta')
for fas in fasta_seqs:
    B1 = fas.seq

lines = open('X-mutations.txt', 'r').readlines()
for l in lines:
    es = l.split()
    muts = []
    muts_R = []
    label = es[0]
    if len(es) == 3:
      for mut in es[2].split('|'):
          muts.append((mut[0], int(mut[1:-1]), mut[-1]))
    #print( label, muts )
    mut_seq = put_muts( WT, muts, -shift )

    #from newseq to B1
    muts_R = get_muts( mut_seq, B1, -1 )
    #from B1 to newseq
    muts_F = get_muts( B1, mut_seq, -1 )
    write_mutfile( "mut_fwd/"+label, muts_F )
    write_mutfile( "mut_rev/"+label, muts_R )
