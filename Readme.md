# Machine Learning Assisted Pyrrolysyl-tRNA Synthetase (PylRS) Design

This repository encompasses all the training code, model parameters, and the necessary code for inference. It provides a replicable process for predicting non-canonical amino acid TCOY on Google Colab. The provided example code allows users to attempt other non-canonical computations, but the required cartddg calculations must be completed in a local cluster with Rosetta installed.

## 1. Preparing sturcture templates

All calculations related to energy-based terms need to start from an optimized initial structure, which can be the wild-type (WT) structure or a known mutant that can recognize a similar substrate.

Relax (using Rosetta) the structure pdb if you have one, follow the protocol from [Cage-Prox](https://github.com/wendao/Cage-Prox), otherwise you can predict the structure using [ColabFold](https://github.com/sokrypton/ColabFold) beforehand.

## 2. Sequence embedding

Sequence-related features include the 1v and msa-1b scores calculated using the ESM model, where the MSA data used for msa-1b is obtained from deepMSA. Using the same MSA, we fine-tuned the UniRep model with [eUniRep](https://github.com/wendao/jax-unirep), making it more suitable for the characterization of PylRS, and selected the 256D model to encode protein sequences.

Note: UniRep model is fine-tuned specifically for PylRS, and the Autogluon model is designed for non-canonical amino acids derived from tyrosine. For more general applications, additional experimental data and model training are necessary.

### A. Command line for ESM-1v score

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

### B. Command line of ESM-msa-1b

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

### C. Command line of eUnirep
For the protein of interest, such as PylRS in this example, we use the multiple sequence alignment data obtained from DeepMSA to fine-tune the UniRep model. This only needs to be done once, but if you wish to apply this method to other proteins, you will need to fine-tune it specificlly.

```bash
#cd unirep/
python /path/of/jax-unirep/scripts/run_jax_evotuning.py \
    outputs/PylRS_train_set.fasta.txt \
    outputs/PylRS_out_domain_val_set.fasta.txt 256
```

## 3. Complex structure modeling and ΔΔG calculation

First, it is necessary to create a parameter file for the substrate molecule. Then, molecular docking is performed using Rosetta Docking protocol. Finally, the change in interaction energy between the mutant and the substrate is calculated using cartesian_ddg.

### A. Genration of substrate conformations
Generate confs.sdf using RDKit and refine
```bash
python gen_rotamers.py UAA-info.csv
cd U[X]
  python ../refine_rotamers.py confs.sdf
cd ..

```

### B. Generate rotlib and ligand params
```bash
./run_all_protocol.sh UA UB [...]
```

### C. Generate charge using ORCA and update params
As an option, [ORCA](https://www.faccts.de/orca/) can be used to calculate more accurate charge distributions. We use the [Multiwfn](http://sobereva.com/multiwfn/) for scripts generation and RESP charge calculation.

```bash
./run_QM_protocol.sh A B C D [...]
```

### D. Rosetta docking and cartesian_ddg calculation

Follow the same protocol in [Cage-Prox](https://github.com/wendao/Cage-Prox), Sec. 3 and 4.

## 4. Training

After obtaining the sequence embeddings and structural energy terms from the previous steps, we concatenate these two sets of data into a single one-dimensional vector with a length of 256 + 5 + 1 + 18 = 280. Each column is normalized saved. Subsequently, we invoke Autogluon to conduct the training process. 

We have provided scripts that can process data from scratch and a notebook that can reproduce the model training.

### A. Data preparation

We demonstrate in the *prepare_data_from_B1-training.ipynb* file how to concatenate the results of cartddg with the data of the PLM, and save it as a pickle.

### B. AutoGluon training

Load the  , and train
Load the training data(saved in 4.prediction/reference_data/train_evo256.pickle) and train with Autogluon. 

The final model is saved in 4.Prediction/AutogluonModels.

## 5. Prediction

To predict a new ncAA, follow the same data preparation protocol above.

Note: For TCOY, it is difficult to accurately predict the trans ring conformation. Therefore, we aligned the TCO conformations from the PDB structure of TCOK onto the generated rotamers in both ax and ep ways, and then re-optimized them using RDKit (fix_TCO.py and fit_TCO.sh).

```bash
#TCOY with ax and eq type
python concat_data_for_prediction.py X ax eq
```

Predict and rank for each single mutation, see notbook predict-ssm.ipynb.

We also provided notebook to reproduce the prediction of TCOY in Colab. <a href="https://colab.research.google.com/github/wendao/PylRS-libY/blob/master/4.prediction/reference_data/reproduce_pylrsY_prediction.ipynb">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a>

