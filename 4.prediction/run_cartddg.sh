for d in X-ax X-eq Y-ax Y-eq S-ax S-eq Z-S Z-R
do
cd U$d
mkdir dock
cd dock
##init
cat ../../../1.strcutures/B1-af2.pdb ../rotlib/LIG_0001.pdb | grep -v END > complex.pdb

##params
cp ../rotlib/rotlib.pdb .
cp ../rotlib/LIG1.params .
cp ../rotlib/LIG.tors .
cd ..

#cartddg from hpc cluster and collect *.ddg
mkdir ddg
mkdir ddg/muts
mkdir ddg/ssm

cd ..
done
