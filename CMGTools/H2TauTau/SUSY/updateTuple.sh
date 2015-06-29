# update each ntuple by adding QCD fake weight and the MVA for ttbar rejection

basedir="/afs/cern.ch/user/y/ytakahas/work/H_CP_study/CMSSW_5_3_14/src/CMGTools/H2TauTau/SUSY/sample_201507/"

for file in TTJetsFullLept TTJetsSemiLept WJets data_Run2012A data_Run2012B data_Run2012C data_Run2012D DYJets
  do

  ifile="${basedir}/${file}/H2TauTauTreeProducerTauMu/H2TauTauTreeProducerTauMu_tree.root";
  ofile="${basedir}/${file}/H2TauTauTreeProducerTauMu/H2TauTauTreeProducerTauMu_tree_mod.root";

  cd EmuMVA;
  root -l -q -b 'addvariable.C("'${ifile}'", "'${ofile}'", "'${file}'")'
  cd -;

done
