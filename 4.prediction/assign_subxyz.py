import sys

#cmd: map.txt TCO.pdb ROT.mol2

lines = open(sys.argv[1], 'r').readlines()
map_pdb2mol = {}
for l in lines:
    es = l.split()
    map_pdb2mol[int(es[1])] = int(es[0])

lines = open(sys.argv[2], 'r').readlines()
xyz_db = {}
for l in lines:
    if l[:6] == "HETATM":
        ndx = int(l[6:12])
        if ndx in map_pdb2mol.values():
            x = float(l[30:38])
            y = float(l[38:46])
            z = float(l[46:54])
            xyz_db[ndx] = (x,y,z)

lines = open(sys.argv[3], 'r').readlines()
status = False
for l in lines:
    if l.strip() == "@<TRIPOS>ATOM":
        status = True
        print l.strip()
        continue
    if l.strip() == "@<TRIPOS>BOND":
        status = False
        print l.strip()
        continue
    if status:
        es = l.strip().split('\t')
        ndx = int(es[0])
        if ndx in map_pdb2mol.keys():
            x,y,z = xyz_db[map_pdb2mol[ndx]]
            str_out = es[0] + '\t'
            str_out = str_out + es[1] + '\t'
            str_out = str_out + str(x) + '\t'
            str_out = str_out + str(y) + '\t'
            str_out = str_out + str(z) + '\t'
            str_out = str_out + es[5] + '\t'
            str_out = str_out + es[6] + '\t'
            str_out = str_out + es[7] + '\t'
            str_out = str_out + es[8]
            print str_out
        else:
            print l.strip()
    else:
        print l.strip()
