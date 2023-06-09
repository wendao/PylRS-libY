for i in UY US #UX:Y, UY/US:C
do
  for j in ax eq
  do
    cd ${i}-${j}
      #generate script
      ../../3.training/gen_pml.sh confs > gen_rotamers.pml
      pymol gen_rotamers.pml 
      #move mol2
      mkdir raw
      mv ROT*mol2 raw/
      cd raw
        ls *mol2 | sed 's/.mol2//' > ../list
      cd ..
    cd ..

    #fit K/Y/C
    cd ${i}-ax
      mkdir fit
      ../fit_TCO.sh ax > aln-ax.pml
      pymol aln-ax.pml
      ../replace_TCO.sh > convert.pml
      pymol convert.pml
      python ../fix_TCO.py
      mv fixed-confs.sdf fixed-ax.sdf
      ../fit_TCO.sh eq > aln-eq.pml
      pymol aln-eq.pml
      ../replace_TCO.sh > convert.pml
      pymol convert.pml
      python ../fix_TCO.py
      mv fixed-confs.sdf fixed-eq.sdf
    cd ..
    cd ${i}-eq
      ../fit_TCO.sh ax > aln-ax.pml
      pymol aln-ax.pml
      ../replace_TCO.sh > convert.pml
      pymol convert.pml
      python ../fix_TCO.py
      mv fixed-confs.sdf fixed-ax.sdf
      ../fit_TCO.sh eq > aln-eq.pml
      pymol aln-eq.pml
      ../replace_TCO.sh > convert.pml
      pymol convert.pml
      python ../fix_TCO.py
      mv fixed-confs.sdf fixed-eq.sdf
    cd ..
    ##refine
    cd ${i}-ax
      python ../refine_rotamers.py fixed-ax.sdf ../${i}-eq/fixed-ax.sdf
    cd ..
    cd ${i}-eq
      python ../refine_rotamers.py fixed-eq.sdf ../${i}-ax/fixed-eq.sdf
    cd ..
  done
done

