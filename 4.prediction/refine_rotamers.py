import rdkit
from rdkit import Chem
from rdkit.Chem import AllChem
import sys

suppl = Chem.SDMolSupplier(sys.argv[1], sanitize=True, removeHs=False, strictParsing=True)

raw_sc = []
min_sc = []
confs = []
for mol in suppl:
    ff0 = AllChem.UFFGetMoleculeForceField(mol)
    ff0.Initialize()
    ff1 = AllChem.UFFGetMoleculeForceField(mol)
    ff1.Initialize()
    
    raw_sc.append(ff0.CalcEnergy())
    
    for atom in mol.GetAtoms():
        idx = atom.GetIdx()
        ff1.UFFAddPositionConstraint(idx, maxDispl=0.1, forceConstant=100)
    ff1.Minimize(maxIts=200)
    min_sc.append(ff0.CalcEnergy())

    confs.append(mol)

import numpy as np
up = np.std(min_sc)
if up > 20.0: up = 20.0
ener_cut = np.median(min_sc) + up

writer = Chem.SDWriter("refined-confs.sdf")
for sc, mol in zip(min_sc, confs):
    if sc < ener_cut:
        writer.write(mol)
writer.close()
