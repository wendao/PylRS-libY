for i in S-ax S-eq Z-S Z-R
do
echo ${i}

#ddg results
cd U${i}
cd ddg/muts
ls *ddg > list
python ../../../../3.training/parse_newdata_ddg.py > results.txt
python ../../../../3.training/parse_newdata_ddg_terms.py > results-terms.txt
cp results.txt ../../../ddg_muts/U${i}_ddg.txt
cp results-terms.txt ../../../ddg_muts/U${i}_ddg_terms.txt
cd ../..
cd ddg/ssm
ls *ddg > list
python ../../../../3.training/parse_newdata_ddg.py > results.txt
python ../../../../3.training/parse_newdata_ddg_terms.py > results-terms.txt
cp results.txt ../../../ddg_ssm/U${i}_ddg.txt
cp results-terms.txt ../../../ddg_ssm/U${i}_ddg_terms.txt
cd ../..
cd ..

#norm
tail -n +2 ddg_muts/U${i}_ddg_terms.txt > tmp_U${i}.dat
tail -n +2 ddg_ssm/U${i}_ddg_terms.txt > ssm_U${i}.dat
python ../3.training/normalization_zscore.py tmp_U${i}.dat ssm_U${i}.dat > ssm_U${i}_ddg_terms.txt
done

