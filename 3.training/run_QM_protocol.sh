#for ORCA setup
export PATH=/home/wendao/install/orca_5_0_1_linux_x86-64_shared_openmpi411:$PATH
export LD_LIBRARY_PATH=/home/wendao/install/orca_5_0_1_linux_x86-64_shared_openmpi411:$LD_LIBRARY_PATH
export PATH=/opt/omp411/bin:$PATH
export LD_LIBRARY_PATH=/opt/omp411/lib:$LD_LIBRARY_PATH

#for Multiwfn setup
export KMP_STACKSIZE=200M
ulimit -s unlimited

#for i in A B C D E F G H #training
for i in X-ax X-eq Y-ax Y-eq Z-S Z-R S-ax S-eq
do
  echo $i
  cd U${i}

##############################################################################################1
#mkdir orca
cd orca
obabel ../rotlib/lig_bcc_gaff.mol2 -O lig.xyz

## OPT
cat ../../../3.training/orca-opt.templ > opt.inp
tail -n +3 lig.xyz >> opt.inp
echo ' *' >> opt.inp
/home/wendao/install/orca_5_0_1_linux_x86-64_shared_openmpi411/orca opt.inp > opt.out
orca_2mkl opt -molden

## GEN inp
~/source/Multiwfn_3.8_dev_bin_Linux/Multiwfn << __EOF__
opt.xyz
100
2
12
opt-gas.inp
5
2
12
opt-wat.inp
-1
water
5
0
0
q
__EOF__

## SP
../../../3.training/fix_orca_charge_line.sh opt-gas.inp
/home/wendao/install/orca_5_0_1_linux_x86-64_shared_openmpi411/orca opt-gas.inp > opt-gas.out
../../../3.training/fix_orca_charge_line.sh opt-wat.inp
/home/wendao/install/orca_5_0_1_linux_x86-64_shared_openmpi411/orca opt-wat.inp > opt-wat.out
orca_2mkl opt-gas -molden
orca_2mkl opt-wat -molden

## charge
~/source/Multiwfn_3.8_dev_bin_Linux/Multiwfn << __EOF__
opt-gas.molden.input
7
18
1
y
0
0
q
__EOF__

~/source/Multiwfn_3.8_dev_bin_Linux/Multiwfn << __EOF__
opt-wat.molden.input
7
18
1
y
0
0
q
__EOF__

# average charge
python ../../../3.training/map_resp_charge.py ../rotlib/LIG_0001.pdb opt-gas.molden.chg opt-wat.molden.chg ../rotlib/LIG.params > ../rotlib/LIG1.params

cd ..
##############################################################################################1

  cd ..
done

