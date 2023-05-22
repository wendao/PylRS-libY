import sys
import numpy as np
from collections import defaultdict

"""
Options: 0001.pdb gas.chg wat.chg params
inp and pdb: map atom order
"""

atom_db = {}
ndx = 0
lines = open(sys.argv[1], 'r').readlines()
for l in lines:
    if l[:6]=="HETATM":
        ndx = ndx + 1
        atom = l[12:16].strip()
        atom_db[atom] = ndx
#print atom_db

charge_db = defaultdict(list)
#charge A
lines = open(sys.argv[2], 'r').readlines()
ndx = 0
for l in lines:
    es = l.split()
    ndx = ndx + 1
    charge = float(es[-1])
    charge_db[ndx].append(charge)
#charge B
lines = open(sys.argv[3], 'r').readlines()
ndx = 0
for l in lines:
    es = l.split()
    ndx = ndx + 1
    charge = float(es[-1])
    charge_db[ndx].append(charge)
#print charge_db

#params
lines = open(sys.argv[4], 'r').readlines()
ndx = 0
for l in lines:
    l = l.strip()
    if l[:4] == "ATOM":
        ndx = ndx + 1
        es = l.split()
        name = es[1]
        type = es[2]
        label = es[3]
        charge = float(es[4])
        iatom = atom_db[name]
        print "ATOM  %s  %s  %s  %6.2f" % (name, type, label, np.mean(charge_db[iatom]))
    else:
        print l
