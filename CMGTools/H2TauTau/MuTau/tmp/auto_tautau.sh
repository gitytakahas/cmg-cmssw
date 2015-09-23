for pt in 25 30 35 40 50 60
do
  echo ""
  echo "------------ processing pT = ${pt} -----------------"
  echo ""
  cp ~/work/TauTrigger_tautau/CMSSW_5_3_14/src/CMGTools/H2TauTau/TauTau/sample_${pt}/htt_tt.inputs-sm-8TeV.root auxiliaries/shapes/CERN/
  
  python HiggsAnalysis/HiggsToTauTau/scripts/doSM.py --drop-list auxiliaries/pruning/uncertainty-pruning-drop-130924-sm.txt --config HiggsAnalysis/HiggsToTauTau/limits.config --update-all 125
  blindData.py LIMITS/bbb/tt/125/  --X-allow-no-signal --inject-signal
  cd HiggsAnalysis/HiggsToTauTau/test;
  python mlfit_and_copy.py $CMSSW_BASE/src/LIMITS/bbb/tt/125
  cd -
  echo "**** uncertainty on mu-value ****"
  cp $CMSSW_BASE/src/LIMITS/bbb/tt/125/out/mlfit.txt result/mlfit_tt.txt
  tail -n 1 result/mlfit_tt.txt
  echo "**** significance test ****"
  limit.py --significance-frequentist --expectedOnly LIMITS/bbb/tt/125/
  cp $CMSSW_BASE/src/LIMITS/bbb/tt/125/higgsCombineSIG-exp.ProfileLikelihood.mH125.root result/sig_tt.root
  
  limit.py --asymptotic LIMITS/bbb/tt/125 --expectedOnly
done