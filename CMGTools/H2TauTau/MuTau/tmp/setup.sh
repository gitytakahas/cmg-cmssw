#for pt in 21 24 27 30 33 36
for pt in 21
  do
  cd auxiliaries/shapes/CERN
  cp htt_mt.inputs-sm-8TeV_${pt}.root htt_mt.inputs-sm-8TeV.root 
  cd -
  sh do.sh # setup analysis environment
#  cd HiggsAnalysis/HiggsToTauTau/test;
#  python mlfit_and_copy.py $CMSSW_BASE/src/LIMITS/bbb/mt/125
  limit.py --significance-frequentist LIMITS/bbb/mt/125/
  cd -
#  cp $CMSSW_BASE/src/LIMITS/bbb/mt/125/out/mlfit.txt result/mlfit_mt_${pt}.txt
done

