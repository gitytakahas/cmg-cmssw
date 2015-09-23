#cp htt_mt.inputs-sm-8TeV_20.root auxiliaries/shapes/CERN/htt_mt.inputs-sm-8TeV.root 
#cp htt_mt.inputs-sm-8TeV_scale.root auxiliaries/shapes/CERN/htt_mt.inputs-sm-8TeV.root
#cp htt_mt.inputs-sm-13TeV_10fb.root auxiliaries/shapes/CERN/htt_mt.inputs-sm-8TeV.root
cp htt_mt.inputs-sm-13TeV_50fb.root auxiliaries/shapes/CERN/htt_mt.inputs-sm-8TeV.root 
sh do.sh # setup analysis environment
blindData.py LIMITS/bbb/mt/125/  --X-allow-no-signal --inject-signal --X-no-check-norm
cd HiggsAnalysis/HiggsToTauTau/test;
python mlfit_and_copy.py $CMSSW_BASE/src/LIMITS/bbb/mt/125
cd -
echo "**** uncertainty on mu-value : mt-channel "
cp $CMSSW_BASE/src/LIMITS/bbb/mt/125/out/mlfit.txt result/mlfit_mt_20.txt
tail -n 1 result/mlfit_mt_20.txt
echo "**** significance test : mt-channel"
limit.py --significance-frequentist --expectedOnly LIMITS/bbb/mt/125/




