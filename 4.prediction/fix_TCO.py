import rdkit
from rdkit import Chem
from rdkit.Chem import AllChem
import numpy

def CalcConfRMS(N, conf1, conf2):
    ssr = 0                                                                        
    for i in range(N):                                             
        d = conf1.GetAtomPosition(i).Distance(conf2.GetAtomPosition(i))              
        ssr += d * d                                                                 
    ssr /= N
    return numpy.sqrt(ssr)

rms_cut = 0.15
conformers = None
writer = Chem.SDWriter("fixed-confs.sdf")
file_lst = open("list", 'r').readlines()
for i,f in enumerate(file_lst):
    f = f.strip()
    suppl = Chem.SDMolSupplier(f+'.sdf', sanitize=True, removeHs=False, strictParsing=True)
    mol = suppl[0]
    ref_mol = Chem.MolFromMolBlock( Chem.MolToMolBlock(mol) )
    Chem.SanitizeMol(ref_mol)
    ref_mol = Chem.AddHs(ref_mol)
    ref_mol.AddConformer(mol.GetConformer(0)) #id and index are different

    #min
    try:
        ff = AllChem.UFFGetMoleculeForceField(mol)
        ff.Initialize()
        for atom in mol.GetAtoms():
            idx = atom.GetIdx()
            ff.UFFAddPositionConstraint(idx, maxDispl=0.1, forceConstant=1000)
        ff.Minimize(maxIts=200)
        rms = CalcConfRMS( mol.GetNumAtoms(), ref_mol.GetConformers()[1], mol.GetConformer(0) )
    except:
        print "Min failed, skip ..."
        continue
    if rms>0.15: continue
    #print "shift=", rms
    
    #embed
    #try:
    #    AllChem.ConstrainedEmbed(mol, tmpl, randomseed=111)
    #    ebrms = float(mol.GetProp('EmbedRMS'))
    #except:
    #    continue
    #if ebrms>0.2: continue
    
    #cluster
    if conformers is None:
        conformers = Chem.MolFromMolBlock( Chem.MolToMolBlock(mol) )
        Chem.SanitizeMol(conformers)
        conformers = Chem.AddHs(conformers)
        conformers.AddConformer(mol.GetConformer(0))
        writer.write(mol)
    else:
        confs = conformers.GetConformers()
        rmslst = [ CalcConfRMS(mol.GetNumAtoms(), conf, mol.GetConformer(0)) for conf in confs ]
        minrms = min(rmslst)
        if minrms > rms_cut:
            #save if not close any old rotamer
            conformers.AddConformer(mol.GetConformer(0))
            writer.write(mol)
            print i, 'RMS:', minrms
            last_iter = i
        else:
            if i-last_iter>100:
                print "Warning: early quit at iter=", i
                break
writer.close()

