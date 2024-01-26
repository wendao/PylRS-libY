

## Generate ligand params step by step

1. sampling conformations using RDKit
```bash
python ../3.training/gen_rotamers.py UAA_inp.txt
```

2. refine sdf (with TCO fix)
```bash
run_TCO_prefix.sh
```

3. generate rosetta params and rotlib
```bash
../3.training/run_rotlib_all.sh
```

4. fix charge with ORCA
```bash
../3.training/run_QM_protocol.sh
```
