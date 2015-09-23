for pt in 24 27 30 33 36 39
#for pt in 30 36 42
#for pt in 33
#for pt in 24
  do
  cd auxiliaries/shapes/CERN
  cp htt_et.inputs-sm-8TeV_${pt}.new.root htt_et.inputs-sm-8TeV.root 
  cd -
  sh do_e.sh # setup analysis environment
  blindData.py LIMITS/bbb/et/125/  --X-allow-no-signal --inject-signal --X-no-check-norm
  cd HiggsAnalysis/HiggsToTauTau/test;
  python mlfit_and_copy.py $CMSSW_BASE/src/LIMITS/bbb/et/125
  cd -
  echo "**** uncertainty on mu-value : et-channel : pT = ", $pt, "----------------------"
  cp $CMSSW_BASE/src/LIMITS/bbb/et/125/out/mlfit.txt result/mlfit_et_${pt}.txt
  tail -n 1 result/mlfit_et_${pt}.txt
  echo "**** significance test : et-channel : pT = ", $pt, "----------------------"
  limit.py --significance-frequentist --expectedOnly LIMITS/bbb/et/125/
  cp $CMSSW_BASE/src/LIMITS/bbb/et/125/higgsCombineSIG-exp.ProfileLikelihood.mH125.root result/sig_et_${pt}.root
done
