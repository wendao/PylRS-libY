import sys, os, csv
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Draw
import rdkit.Chem.rdFMCS as MCS

import py3Dmol
from ipywidgets import interact, interactive, fixed

def drawit(m,p,confId=-1):
        mb = Chem.MolToMolBlock(m,confId=confId)
        p.removeAllModels()
        p.addModel(mb,'sdf')
        p.setStyle({'stick':{}})
        p.setBackgroundColor('0xeeeeee')
        p.zoomTo()
        return p.show()

#load UAA smile strings
smi_db = {}
lines = open(sys.argv[1], 'r').readlines()
for l in lines[:]:
    es = l.split(' ')
    ndx = es[0][:-1]
    smi = es[1].strip()
    #print ndx, smi
    smi_db[ndx] = smi
smi_db

#define reaction
rxn_smarts = "[C:1](=[O:2])[OH:3].[OH:4][PH0:5][OH:6]>>[C:1](=[O:2])[OH0:4][P:5][O-:6]"
rxn = AllChem.ReactionFromSmarts(rxn_smarts)

#load AMP template
suppl = Chem.SDMolSupplier("../1.strcutures/AMP.sdf")
for mol in suppl:
    AMP_tmpl = mol
suppl = Chem.SDMolSupplier("../1.strcutures/stub-Y.sdf")
for mol in suppl:
    stubY = mol
suppl = Chem.SDMolSupplier("../1.strcutures/stub-K.sdf")
for mol in suppl:
    stubK = mol

#pv = py3Dmol.view(width=400,height=400)
#interact(drawit, m=fixed(stubK),p=fixed(pv),confId=(0,AMP_tmpl.GetNumConformers()-1));
#
#pv = py3Dmol.view(width=400,height=400)
#interact(drawit, m=fixed(stubY),p=fixed(pv),confId=(0,AMP_tmpl.GetNumConformers()-1));

import numpy
def CalcConfRMS(N, conf1, conf2):
    ssr = 0                                                                        
    for i in range(N):                                             
        d = conf1.GetAtomPosition(i).Distance(conf2.GetAtomPosition(i))              
        ssr += d * d                                                                 
    ssr /= N
    return numpy.sqrt(ssr)

def GenMutiConfMol(mol, tmpl, num_iter, rms_cut, w):
    #constrained and align
    res = MCS.FindMCS([mol, tmpl], threshold=0.9, completeRingsOnly=True)
    p = Chem.MolFromSmarts(res.smartsString)
    core = AllChem.DeleteSubstructs(AllChem.ReplaceSidechains(tmpl,p), Chem.MolFromSmiles('*'))
    core.UpdatePropertyCache()
    print(Chem.MolToSmiles(core))
    #generate confs
    conformers = None
    last_iter = 0
    for i in range(num_iter):
        AllChem.ConstrainedEmbed(mol, core, randomseed=i+111)
        ebrms = float(mol.GetProp('EmbedRMS'))
        if ebrms<0.10:
            #check 
            if conformers == None:
                #save the first one
                conformers = Chem.MolFromMolBlock( Chem.MolToMolBlock(mol) )
                Chem.SanitizeMol(conformers)
                conformers = Chem.AddHs(conformers)
                conformers.AddConformer(mol.GetConformer(0))
                w.write(mol)
            else:
                confs = conformers.GetConformers()
                rmslst = [ CalcConfRMS(mol.GetNumAtoms(), conf, mol.GetConformer(0)) for conf in confs ]
                minrms = min(rmslst)
                if minrms > rms_cut:
                    #save if not close any old rotamer
                    conformers.AddConformer(mol.GetConformer(0))
                    w.write(mol)
                    print(i, 'RMS:', minrms)
                    last_iter = i
                else:
                    if i-last_iter>100:
                        print("Warning: early quit at iter=", i)
                        break
    return conformers

for ndx in smi_db.keys():
    k = ndx
    t = ndx[2]
    smi = smi_db[k]
    #init
    d = "U"+str(k)
    if not os.path.isdir(d):
        os.mkdir(d)
    #create
    print(k, smi)
    UAA = AllChem.MolFromSmiles(smi) #Chem.MolToSmiles(mol, isomericSmiles=True)
    #react
    products = rxn.RunReactants((UAA, AMP_tmpl))
    print(len(products))
    writer = Chem.SDWriter(d+"/confs.sdf")
    for prod in products[1:]:
        #fix prod
        product = prod[0]
        Chem.SanitizeMol(product)
        #product = Chem.RemoveHs(product)
        product = Chem.AddHs(product)
        #use templete
        stub = stubY
        GenMutiConfMol(product, stub, 5000, 0.6, writer)
    writer.close()

