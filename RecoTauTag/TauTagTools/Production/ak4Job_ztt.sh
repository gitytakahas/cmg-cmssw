cd ${dir}
currDir=`pwd`
echo 'Now working in '${currDir}
eval `scramv1 runtime -sh`
cmsRun SingleTaupt_50_cfi_GEN_SIM_DIGI_L1_DIGI2RAW_RAW2DIGI_L1Reco_RECO.py maxEvents=${1} seed=${2}