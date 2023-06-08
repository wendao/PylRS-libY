basepath=$(dirname $0)
#echo $basepath
echo load ${1}.sdf
echo split_states ${1}
seq 1 $(${basepath}/get_Nconf.sh) | awk '{printf("save ROT_%04d.mol2, '${1}'_%04d\n", $1, $1)}'
echo quit
