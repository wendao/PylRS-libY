import sys
import numpy as np
from collections import defaultdict

max_zscore = 5

#stat
data = defaultdict(lambda: defaultdict(float))
lines = open(sys.argv[1], 'r').readlines()
for l in lines:
    es = l.strip().split()
    for i, e in enumerate(es[1:]):
        data[i][es[0]]=float(e)

#calc
mu = defaultdict(float)
sigma = defaultdict(float)
for k in data.keys():
    x_raw = np.array(data[k].values())
    tmp_mu = np.mean(x_raw)
    x0 = x_raw - tmp_mu
    tmp_sigma = np.std(x0)
    if tmp_sigma < 1e-6:
        #print "skip", k
        continue
    mu[k] = tmp_mu
    sigma[k] = tmp_sigma
    #print "DB:", k, mu[k], sigma[k]

#norm
lines = open(sys.argv[2], 'r').readlines()
for l in lines:
    es = l.strip().split()
    out_str = es[0]
    for k, e in enumerate(es[1:]):
        if k not in mu.keys(): continue
        z = (float(e)-mu[k])/sigma[k]
        if z > max_zscore: z = max_zscore
        elif z < -max_zscore: z = -max_zscore
        out_str += "\t%4.2f" % z
    print out_str
