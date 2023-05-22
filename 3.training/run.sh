for i in A B C D E F G H
do
echo $i
cd U${i}

## OPT
mv ../opt${i}.inp .
orca opt${i}.inp > opt.out
orca_2mkl opt${i} -molden

# gen input
# charge 0 2 -> -1 1
~/source/Multiwfn_3.8_dev_bin_Linux/Multiwfn << __EOF__
opt${i}.xyz
100
2
12
opt${i}-gas.inp
5
2
12
opt${i}-wat.inp
-1
water
5
0
0
q
__EOF__

# SP
orca opt${i}-gas.inp > opt-gas.out
orca opt${i}-wat.inp > opt-wat.out
orca_2mkl opt${i}-gas -molden
orca_2mkl opt${i}-wat -molden

# charge
~/source/Multiwfn_3.8_dev_bin_Linux/Multiwfn << __EOF__
opt${i}-gas.molden.input
7
18
1
y
0
0
q
__EOF__

~/source/Multiwfn_3.8_dev_bin_Linux/Multiwfn << __EOF__
opt${i}-wat.molden.input
7
18
1
y
0
0
q
__EOF__

## average charge
python ../map_resp_charge.py LIG_0001.pdb opt${i}-gas.molden.chg opt${i}-wat.molden.chg LIG.params > LIG1.params
cd ..
done

