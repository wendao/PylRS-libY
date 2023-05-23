for f in $(cat list)
do
    #K
    #python ../assign_subxyz.py ../map_tco_K_mol2.txt fit/${f}.pdb raw/${f}.mol2 > ${f}.mol2
    #Y
    #python ../assign_subxyz.py ../map_tco_Y_mol2.txt fit/${f}.pdb raw/${f}.mol2 > ${f}.mol2
    #C
    python ../assign_subxyz.py ../map_tco_C_mol2.txt fit/${f}.pdb raw/${f}.mol2 > ${f}.mol2

    #save to a pml file
    echo load ${f}.mol2
    echo save ${f}.sdf
    echo delete ${f}
done
