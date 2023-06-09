# Machine Learning Assisted Pyrrolysyl-tRNA Synthetase (PylRS) Design

## 1. Preparing sturcture templates

## 2. Sequence embedding

Command line of ESM-1v

```python
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

```python
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

## 3. Preparing input data and training set

