# setup environment !
#export SCRAM_ARCH=slc5_amd64_gcc472
#cmsrel CMSSW_6_1_1
#cd CMSSW_6_1_1/src/
#cmsenv
#git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
#git clone https://github.com/cms-analysis/HiggsAnalysis-HiggsToTauTau.git HiggsAnalysis/HiggsToTauTau
#git clone https://github.com/roger-wolf/HiggsAnalysis-HiggsToTauTau-auxiliaries.git auxiliaries
# scram b -j4

# setup limit structure:
python HiggsAnalysis/HiggsToTauTau/scripts/doSM.py --drop-list auxiliaries/pruning/uncertainty-pruning-drop-130924-sm.txt --config HiggsAnalysis/HiggsToTauTau/limits_m.config --update-all 125

#for chn in et mt
#for chn in mt
#  do
#  submit.py --max-likelihood LIMITS/hww-bg/${chn}/125
#  submit.py --max-likelihood LIMITS/bbb/${chn}/125
#done


#sed -i "1s,.*,#include \"$CMSSW_BASE/src/HiggsAnalysis/HiggsToTauTau/interface/HttStyles.h\"," HiggsAnalysis/HiggsToTauTau/src/HttStyles.cc
#cd HiggsAnalysis/HiggsToTauTau/test

#for chn in et
#do
#  python mlfit_and_copy.py -s $CMSSW_BASE/src/LIMITS/bbb/$chn/125
##  python produce_macros.py -c ../data/limits.config-sm-${chn}-only --hww-background --add-0jet-signal --shapes 0
##  python produce_macros.py -c ../data/limits.config-sm-${chn}-only --add-0jet-signal --shapes 0
##  python produce_macros.py -c ../data/limits.config-sm-${chn}-only --shapes 0 --omit 1
#  python produce_macros.py -c ../data/limits.config-sm-${chn}-only --shapes 1 --omit 1
#  python run_macros.py -c ../data/limits.config-sm-${chn}-only
#done
#
#cd -
