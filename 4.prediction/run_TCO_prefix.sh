for i in UX-ax UX-eq UY-ax UY-eq US-ax US-eq
do
  cd $i
    ##generate script
    #../../3.training/gen_pml.sh confs > gen_rotamers.pml
    #pymol gen_rotamers.pml 
    ##move mol2
    #mkdir raw
    #mv ROT*mol2 raw/
    #cd raw
    #  ls *mol2 | sed 's/.mol2//' > ../list
    #cd ..

    ##fit K/Y/C

  cd ..
done
