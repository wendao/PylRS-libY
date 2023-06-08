for d in $*
do
    cd $d
    mkdir rotlib
    cd rotlib
      #for normal
      ../../../3.training/gen_pml_rot.sh > gen_rotamers.pml

      pymol gen_rotamers.pml
      acpype.py -i lig.mol2 -n -1

      cp lig.acpype/lig_bcc_gaff.mol2 .
      ../../../3.training/convert_qm2mol2.sh lig_bcc_gaff.mol2

      root=$(grep 'N.2' lig_bcc_gaff.mol2 | awk '{print $1}')
      /home/wendao/bakerlab/Rosetta/main/source/scripts/python/public/molfile_to_params.py lig_bcc_gaff.mol2 -n LIG --root_atom=$root --extra_torsion_output --clobber

      python ../../../3.training/gen_rot_lib.py LIG_0001.pdb ROT_0*pdb > rotlib.pdb
      cp LIG.params LIG0.params
      echo "PDB_ROTAMERS rotlib.pdb" >> LIG.params
    cd ..
    cd ..
done

