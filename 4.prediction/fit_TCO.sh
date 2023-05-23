echo load ../TCO-gaff-${1}.mol2 

for f in $(cat list)
do
    echo load raw/${f}.mol2
    #K
    #echo pair_fit TCO-gaff-${1} and name O13+C14+C21, ${f} and id 14+16+18
    #Y
    #echo pair_fit TCO-gaff-${1} and name O13+C14+C21, ${f} and id 15+16+18
    #C
    echo pair_fit TCO-gaff-${1} and name O13+C14+C21, ${f} and id 14+15+17
    echo save fit/${f}.pdb, TCO-gaff-${1}
    echo delete ${f}
done
