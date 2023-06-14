#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
from pandas import DataFrame

import sys
name = sys.argv[1]
exts = sys.argv[2:]

#load energy data
all_data = pd.DataFrame()
for i in [ name+"-"+ext for ext in exts ]:
    print(i)
    df = pd.read_csv("ssm_U"+i+"_ddg_terms.txt", sep="\t", header=None)
    #delete all zero col
    df = df.loc[:,~(df==0).all(axis=0)]
    
    df['UAA'] = i
    df['label'] = False #for prediction, set to False
    all_data = pd.concat([all_data, df], axis=0, ignore_index=True)
all_data = all_data.rename(columns={0: "id"})


# In[3]:


#load ESM-1v, ESM-1b
df1v = pd.read_csv("../2.evotuning/mm_SSM_1v_labeled.csv")
df1b = pd.read_csv("../2.evotuning/mm_SSM_1b_labeled.csv")


# In[4]:


all_data = pd.merge(all_data, df1v.loc[:, ['id','esm1v_t33_650M_UR90S_1']], how='left', on='id')
all_data = pd.merge(all_data, df1v.loc[:, ['id','esm1v_t33_650M_UR90S_2']], how='left', on='id')
all_data = pd.merge(all_data, df1v.loc[:, ['id','esm1v_t33_650M_UR90S_3']], how='left', on='id')
all_data = pd.merge(all_data, df1v.loc[:, ['id','esm1v_t33_650M_UR90S_4']], how='left', on='id')
all_data = pd.merge(all_data, df1v.loc[:, ['id','esm1v_t33_650M_UR90S_5']], how='left', on='id')
all_data = pd.merge(all_data, df1b.loc[:, ['id','esm_msa1b_t12_100M_UR50S']], how='left', on='id')


# In[5]:


raw_data = all_data.copy()


# In[6]:


#extract X
col = raw_data.columns.values.tolist()
col.remove('UAA')
col.remove('label')
col.remove('id')


# In[7]:


X = np.array(raw_data[col])
y = np.array(raw_data['label'])
print(X.shape, np.sum(y))


# In[8]:


import pickle
import os
os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"   # see issue #152
os.environ["CUDA_VISIBLE_DEVICES"]="0"


# In[9]:


#load eUnirep 256 embedding
evo_tag = "256"
evo_num = int(evo_tag)
from jax_unirep.evotuning_models import mlstm256
from jax_unirep.utils import load_params
from jax_unirep import get_reps


# In[10]:


i2s = {}
lines = open("map_label_fname_ssm.txt", 'r')
for l in lines:
    es = l.strip().split()
    i2s[es[0]] = es[2]


# In[11]:


sequences = [i2s[t] for t in i2s.keys()]
s2t = {i2s[t]:t for t in i2s.keys()}


# In[12]:


params = load_params(folderpath='../2.evotuning/unirep/weights/'+evo_tag+'/', paper_weights=evo_num)[1]
h_avg, h_final, c_final= get_reps(sequences, params=params,mlstm_size=evo_num)


# In[13]:


df_evo = pd.DataFrame()
for i, t in enumerate(i2s.keys()):
    d = pd.Series([s2t[sequences[i]]]+[x for x in h_avg[i]])
    assert(t == s2t[sequences[i]])
    df_evo = pd.concat([df_evo, d.to_frame().T], axis=0, ignore_index=True)


# In[14]:


convert = {i:"e"+str(i) for i in range(1+evo_num)}
convert[0] = "id"
df_evo = df_evo.rename(columns=convert)


# In[15]:


raw_data = pd.merge(all_data, df_evo.loc[:, :], how='left', on='id')


# In[16]:


col = raw_data.columns.values.tolist()
#col.remove('tag')
col.remove('UAA')
col.remove('label')
col.remove('id')


# In[17]:


X = np.array(raw_data[col])
y = np.array(raw_data['label'])


# In[18]:


print(X.shape, np.sum(y))


# In[19]:


with open(name+"_ssm_evo"+evo_tag+".pickle", 'wb') as f:
    pickle.dump([X, y], f)


# In[ ]:




