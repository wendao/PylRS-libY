echo load ../refined-confs.sdf
echo split_states refined-confs
echo save lig.mol2, refined-confs_0001
seq 1 $(grep RDKit ../refined-confs.sdf | wc -l) | awk '{printf("save ROT_%04d.pdb, refined-confs_%04d\n", $1, $1)}'
echo quit
