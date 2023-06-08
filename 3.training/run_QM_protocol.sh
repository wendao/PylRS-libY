#for ORCA setup
export PATH=/home/wendao/install/orca_5_0_1_linux_x86-64_shared_openmpi411:$PATH
export LD_LIBRARY_PATH=/home/wendao/install/orca_5_0_1_linux_x86-64_shared_openmpi411:$LD_LIBRARY_PATH
export PATH=/opt/omp411/bin:$PATH
export LD_LIBRARY_PATH=/opt/omp411/lib:$LD_LIBRARY_PATH

#for Multiwfn setup
export KMP_STACKSIZE=200M
ulimit -s unlimited

for i in X-eq Y-ax Y-eq Z-S Z-R S-ax S-eq #X-ax 
do
  echo $i
  cd U${i}

##############################################################################################1
mkdir orca
cd orca
obabel ../rotlib/lig_bcc_gaff.mol2 -O lig.xyz

## OPT
cat ../../../3.training/orca-opt.templ > opt.inp
tail -n +3 lig.xyz >> opt.inp
echo ' *' >> opt.inp
/home/wendao/install/orca_5_0_1_linux_x86-64_shared_openmpi411/orca opt.inp > opt.out
#orca_2mkl opt -molden

cd ..
##############################################################################################1

  cd ..
done
