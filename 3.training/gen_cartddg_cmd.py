import sys, os
import shutil
from string import Template

templ = "/home/chuwang_pkuhpc/lustre1/rosetta/rosetta_src_2019.47.61047_bundle/main/source/bin/cartesian_ddg.mpi.linuxiccrelease -s opt.pdb -ddg::mut_file ../mut_ssm/${label}.mutfile -relax:min_type lbfgs_armijo_nonmonotone -ddg:iterations 3 -mute all -unmute apps.pilot.wendao.ddg -fa_max_dis 9.0 -ddg::dump_pdbs true -bbnbrs 1 -score:weights ref2015_cart -interface_ddg 1 -optimization:default_max_cycles 100 -crystal_refine -relax:cartesian -ddg::legacy -extra_res_fa LIG1.params -score:extra_improper_file LIG.tors"
s = Template(templ)

lines = open("muts_label.txt", 'r').readlines()
for l in lines:
  es = l.strip().split()
  label = es[0]

  #cmd
  d = { 'label': label }
  print(s.substitute(d))
