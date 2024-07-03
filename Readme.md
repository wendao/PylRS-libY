# Machine Learning Assisted Pyrrolysyl-tRNA Synthetase (PylRS) Design

## 1. Preparing sturcture templates

Relax the template pdb if you have one, follow the protocol from [Cage-Prox](https://github.com/wendao/Cage-Prox)

Otherwise you can predict the structure using [ColabFold](https://github.com/sokrypton/ColabFold)

## 2. Sequence embedding

Command line of ESM-1v

```bash
python /path/of/esm/variant-prediction/predict-multi.py \
    --model-location esm1v_t33_650M_UR90S_1 esm1v_t33_650M_UR90S_2 esm1v_t33_650M_UR90S_3 esm1v_t33_650M_UR90S_4 esm1v_t33_650M_UR90S_5 \
    --sequence SAPALTKSQTDRLEVLLNPKDEISLNSGKPFRELESELLSRRKKDLQQIYAEERENYLGKLEREITRFFVDRGFLEIKSPILIPLEYIERMGIDNDTELSKQIFRVDKNFCLRPMLAPNLYNYLRKLDRALPDPIKIFEIGPCYRKESDGKEHLEEFTMLNFCQMGSGCTRENLESIITDFLNHLGIDFKIVGDSCMVYGDTLDVMHGDLELSSAVVGPIPLDREWGIDKPWIGAGFGLERLLKVKHDFKNIKRAARSESYYNGISTNL \
    --dms-input mm_diskAB.csv \
    --mutation-col mutant \
    --dms-output mm_diskAB_1v_labeled.csv \
    --offset-idx 186 \
    --scoring-strategy wt-marginals
```

Command line of ESM-1b

```bash
python /path/of/esm/variant-prediction/predict-multi.py \
    --model-location esm_msa1b_t12_100M_UR50S \
    --sequence SAPALTKSQTDRLEVLLNPKDEISLNSGKPFRELESELLSRRKKDLQQIYAEERENYLGKLEREITRFFVDRGFLEIKSPILIPLEYIERMGIDNDTELSKQIFRVDKNFCLRPMLAPNLYNYLRKLDRALPDPIKIFEIGPCYRKESDGKEHLEEFTMLNFCQMGSGCTRENLESIITDFLNHLGIDFKIVGDSCMVYGDTLDVMHGDLELSSAVVGPIPLDREWGIDKPWIGAGFGLERLLKVKHDFKNIKRAARSESYYNGISTNL \
    --dms-input mm_diskAB.csv \
    --mutation-col mutant \
    --dms-output mm_diskAB_1b_labeled.csv \
    --offset-idx 186 \
    --scoring-strategy masked-marginals \
    --msa-path mm-hhb.a3m
```

Command line of eUnirep
```bash
#cd unirep/
python /path/of/jax-unirep/scripts/run_jax_evotuning.py \
    outputs/PylRS_train_set.fasta.txt \
    outputs/PylRS_out_domain_val_set.fasta.txt 256
```

## 3. Preparing input data

Predict:

Generate confs.sdf using RDKit and refine
```bash
python gen_rotamers.py UAA-info.csv
cd U[X]
  python ../refine_rotamers.py confs.sdf
cd ..

```

Generate rotlib
```bash
./run_all_protocol.sh UA UB [...]
```


```bash
#TZ with R and S type
python concat_data_for_prediction.py Z R S
#TCOY with ax and eq type
python concat_data_for_prediction.py X ax eq
```

## 4. Prediction

Follow the same data preparing protocol above.

Predict and rank for each single mutation, see notbook predict-ssm.ipynb.
