import sys, os
import numpy as np

tmpl = sys.argv[1]
rots = sys.argv[2:]

tmp_lines = open(tmpl, 'r').readlines()
map_tmpl_xyz = {}
for n, l in enumerate(tmp_lines):
    if l[:6] != "HETATM": continue
    L1 = l[:13]
    NA = l[13:16]
    L2 = l[16:30]
    XL = l[30:38]
    YL = l[38:46]
    ZL = l[46:54]
    L3 = l[54:-1]
    #print "|"+L1+"|"+NA+"|"+L2+"|"+XL+"|"+YL+"|"+ZL+"|"+L3+"|"
    map_tmpl_xyz[n] = np.array([float(XL), float(YL), float(ZL)])

#compare with the first one, should be the same
map_tmplid2confid = {}
lines = open(rots[0], 'r').readlines()
for n, l in enumerate(lines):
    if l[:6] != "HETATM": continue
    L1 = l[:13]
    NA = l[13:16]
    L2 = l[16:30]
    XL = l[30:38]
    YL = l[38:46]
    ZL = l[46:54]
    L3 = l[54:-1]
    xyz = np.array([float(XL), float(YL), float(ZL)])
    for ni in map_tmpl_xyz.keys():
        txyz = map_tmpl_xyz[ni]
        dr = txyz - xyz
        dd = np.dot(dr, dr)
        if dd<0.01:
            map_tmplid2confid[ni] = n
#print map_tmplid2confid

for nr, rot in enumerate(rots):
    lines = open(rot, 'r')
    map_conf_xyz = {}
    for n, l in enumerate(lines):
        if l[:6] != "HETATM": continue
        L1 = l[:13]
        NA = l[13:16]
        L2 = l[16:30]
        XL = l[30:38]
        YL = l[38:46]
        ZL = l[46:54]
        L3 = l[54:-1]
        xyz = np.array([float(XL), float(YL), float(ZL)])
        map_conf_xyz[n] = xyz
    print "MODEL%9d" % (nr+1)
    for n, l in enumerate(tmp_lines):
        if l[:6] != "HETATM": continue
        L1 = l[:13]
        NA = l[13:16]
        L2 = l[16:30]
        L3 = l[54:-1]
        xyz = map_conf_xyz[map_tmplid2confid[n]]
        xyz_str = "%8.3f%8.3f%8.3f" % (xyz[0], xyz[1], xyz[2])
        pdb_str = L1+NA+L2+xyz_str+L3
        print pdb_str
    print "ENDMDL"
