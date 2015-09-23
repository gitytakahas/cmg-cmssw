for pt in 21 24 27 30 33 36
#for pt in 21
#for pt in 27 33
#for pt in 27
#for pt in 21
#for pt in 36
#for pt in 21
  do
  cd auxiliaries/shapes/CERN
  cp htt_mt.inputs-sm-8TeV_${pt}.new.root htt_mt.inputs-sm-8TeV.root 
  cd -
  sh do.sh # setup analysis environment
  blindData.py LIMITS/bbb/mt/125/  --X-allow-no-signal --inject-signal --X-no-check-norm
  cd HiggsAnalysis/HiggsToTauTau/test;
  python mlfit_and_copy.py $CMSSW_BASE/src/LIMITS/bbb/mt/125
  cd -
  echo "**** uncertainty on mu-value : mt-channel : pT = ", $pt, "----------------------"
  cp $CMSSW_BASE/src/LIMITS/bbb/mt/125/out/mlfit.txt result/mlfit_mt_${pt}.txt
  tail -n 1 result/mlfit_mt_${pt}.txt
  echo "**** significance test : mt-channel : pT = ", $pt, "----------------------"
  limit.py --significance-frequentist --expectedOnly LIMITS/bbb/mt/125/
  cp $CMSSW_BASE/src/LIMITS/bbb/mt/125/higgsCombineSIG-exp.ProfileLikelihood.mH125.root result/sig_${pt}.root
done


