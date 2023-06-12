import numpy as np

def get_terms( elems ):
    tot = float(elems[0])
    terms = {}
    terms["TOT"] = tot
    name = "DUMY"
    for el in elems[1:]:
        if name == "DUMY":
            name = el
        else:
            ener = float(el)
            terms[name] = ener
            name = "DUMY"
    return terms

mutations = []
with open( "list", 'r' ) as flist:
    for line in flist.readlines():
        fn = line.strip()
        mutations.append(fn)

database = {}
for mut in mutations:
    mutation = mut[0:-4]
    #save the lowest term dict
    data = {}
    data["WT"] = {}       #mono WT
    data["MUT"] = {}      #mono MUT
    data["WT_OPT"] = {}   #mono WT
    data["MUT_OPT"] = {}  #mono MUT
    data["B_WT"] = {}     #bind WT
    data["B_MUT"] = {}    #bind MUT
    database[mutation] = data
    with open( mut, 'r' ) as fp:
        for line in fp.readlines():
            elems = line.split()
            if (elems[0]=="COMPLEX:"):
                if (elems[2]=="WT:"):
                    if len(database[mutation]["B_WT"].keys()) == 0:
                        database[mutation]["B_WT"] = get_terms( elems[3:] )
                    else:
                        min_E = database[mutation]["B_WT"]["TOT"]
                        terms = get_terms( elems[3:] )
                        if terms["TOT"] < min_E:
                            database[mutation]["B_WT"] = terms
                elif (elems[2][0:3]=="MUT"):
                    #database[mutation]["B_MUT"].append(float(elems[3]))
                    if len(database[mutation]["B_MUT"].keys()) == 0:
                        database[mutation]["B_MUT"] = get_terms( elems[3:] )
                    else:
                        min_E = database[mutation]["B_MUT"]["TOT"]
                        terms = get_terms( elems[3:] )
                        if terms["TOT"] < min_E:
                            database[mutation]["B_MUT"] = terms
            if (elems[0]=="OPT_APART:"):
                if (elems[2]=="WT:"):
                    #database[mutation]["WT_OPT"].append(float(elems[3]))
                    if len(database[mutation]["WT_OPT"].keys()) == 0:
                        database[mutation]["WT_OPT"] = get_terms( elems[3:] )
                    else:
                        min_E = database[mutation]["WT_OPT"]["TOT"]
                        terms = get_terms( elems[3:] )
                        if terms["TOT"] < min_E:
                            database[mutation]["WT_OPT"] = terms
                elif (elems[2][0:3]=="MUT"):
                    #database[mutation]["MUT_OPT"].append(float(elems[3]))
                    if len(database[mutation]["MUT_OPT"].keys()) == 0:
                        database[mutation]["MUT_OPT"] = get_terms( elems[3:] )
                    else:
                        min_E = database[mutation]["MUT_OPT"]["TOT"]
                        terms = get_terms( elems[3:] )
                        if terms["TOT"] < min_E:
                            database[mutation]["MUT_OPT"] = terms
            if (elems[0]=="APART:"):
                if (elems[2]=="WT:"):
                    #database[mutation]["WT"].append(float(elems[3]))
                    if len(database[mutation]["WT"].keys()) == 0:
                        database[mutation]["WT"] = get_terms( elems[3:] )
                    else:
                        min_E = database[mutation]["WT"]["TOT"]
                        terms = get_terms( elems[3:] )
                        if terms["TOT"] < min_E:
                            database[mutation]["WT"] = terms
                elif (elems[2][0:3]=="MUT"):
                    #database[mutation]["MUT"].append(float(elems[3]))
                    if len(database[mutation]["MUT"].keys()) == 0:
                        database[mutation]["MUT"] = get_terms( elems[3:] )
                    else:
                        min_E = database[mutation]["MUT"]["TOT"]
                        terms = get_terms( elems[3:] )
                        if terms["TOT"] < min_E:
                            database[mutation]["MUT"] = terms

out_str = "MUT"
for k in data["WT"].keys():
    out_str += "\t" + k
print out_str

for mutation in database.keys():
    data = database[mutation]
    results = {}
    if len(data["MUT"].keys())>0:
      for k in data["WT"].keys():
          Efmut = data["MUT"][k]
          Eomut = data["MUT_OPT"][k]
          Ebmut = data["B_MUT"][k]
          results[k] = Ebmut-Efmut
      out_str = ""
      for k in results.keys():
          out_str += "\t%6.4f" % results[k]
      print mutation + out_str
    else:
      for k in data["WT"].keys():
          Efwt = data["WT"][k]
          Eowt = data["WT_OPT"][k]
          Ebwt = data["B_WT"][k]
          results[k] = Ebwt-Efwt
      out_str = ""
      for k in results.keys():
          out_str += "\t%6.4f" % results[k]
      print mutation + out_str


