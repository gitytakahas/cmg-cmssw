# 
# before starting, you need to do 
# 
# 1. put latet file 
#   cd setups/example/th
#   python rename.py -> produce htt_th.inputs-sm-8TeV.root
# 
# 2. run this script



#mkdir -p setups aux
#cp -r HiggsAnalysis/HiggsToTauTau/setup setups/example
#mkdir -p aux/example/sm
setup-datacards.py -p 8TeV -c th -i setups/example -o aux/example -a sm 125
#mkdir -p LIMITS
#mkdir -p LIMITS/example
setup-htt.py -p 8TeV -i aux/example/ -o LIMITS/example/sm -c 'th' 125

cp aux/example/sm/htt_th/htt_th.inputs-sm-8TeV.root LIMITS/example/sm/th/common/htt_th.input_8TeV.root
#limit.py --expectedOnly --significance-frequentist LIMITS/example/sm/th/125 
limit.py --asymptotic LIMITS/example/sm/th/125/