echo load ../refined-confs.sdf
echo split_states refined-confs
echo save lig.mol2, $(grep confs ../refined-confs.sdf | head -n1)
grep confs ../refined-confs.sdf | awk '{printf("save ROT_%04d.pdb, %s\n", NR, $1)}'
echo quit
