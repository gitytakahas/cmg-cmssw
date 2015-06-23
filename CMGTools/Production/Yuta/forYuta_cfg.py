import FWCore.ParameterSet.Config as cms

process = cms.Process("forYuta")

# import of standard configurations for RECOnstruction
# of electrons, muons and tau-jets with non-standard isolation cones
process.load('Configuration/StandardSequences/Services_cff')
process.load('FWCore/MessageService/MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
process.load('Configuration.Geometry.GeometryExtended2017Reco_cff') 
process.load('Configuration.Geometry.GeometryExtended2017_cff')
process.load('Configuration/StandardSequences/MagneticField_cff')
process.load('Configuration/StandardSequences/FrontierConditions_GlobalTag_cff')
process.GlobalTag.globaltag = cms.string('PHYS14_25_V2::All')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(5)
)

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring( 
#        'root://xrootd.unl.edu//store/mc/Phys14DR/QCD_Pt-15to3000_Tune4C_Flat_13TeV_pythia8/AODSIM/PU20bx25_trkalmb_PHYS14_25_V1-v1/00000/125A6B71-C56A-E411-9D2B-0025907609BE.root'
        'root://xrootd.unl.edu//store/mc/Phys14DR/VBF_HToTauTau_M-125_13TeV-powheg-pythia6/AODSIM/PU20bx25_tsg_PHYS14_25_V1-v2/00000/0ACE16B2-5677-E411-87FF-7845C4FC3A40.root'
        ),
#    eventsToProcess = cms.untracked.VEventRange(
#        '1:72:7152',
#        '1:493:49214',
#        '1:230:22944',
#        '1:418:41750',
#        ),
)

process.rerunTauSequence = cms.Sequence()

#--------------------------------------------------------------------------------
# rerun tau reconstruction with latest tags

process.load("RecoTauTag/Configuration/RecoPFTauTag_cff")
process.load("JetMETCorrections/Configuration/DefaultJEC_cff")
process.load("RecoTauTag.Configuration.HPSPFTaus_cff")

process.hpsPFTauMVAIsolation2Seq += process.hpsPFTauMVA3IsolationNeutralIsoPtSumWeight
process.rerunTauSequence += process.PFTau
process.rerunTauSequence += process.ak4PFJetsL1FastL2L3


#--------------------------------------------------------------------------------

process.p = cms.Path(process.rerunTauSequence)

process.skimOutputModule = cms.OutputModule("PoolOutputModule",
    outputCommands = cms.untracked.vstring(
        'keep *_*_*_*'
    ),
    fileName = cms.untracked.string(
#        'forYuta_AOD.root'
        'aod.root'
    )
)

#process.skimOutputModule.outputCommands.append('keep *_*_*_*')

#process.skimOutputModule.outputCommands.append('drop *_ak8*_*_*')
#process.skimOutputModule.outputCommands.append('drop *_*_rho_*')
#process.skimOutputModule.outputCommands.append('drop *_*_sigma_*')
#process.skimOutputModule.outputCommands.append('drop *Track*_*_*_*')
#process.skimOutputModule.outputCommands.append('drop *_kt4*_*_*')
#process.skimOutputModule.outputCommands.append('drop *_kt6*_*_*')
#process.skimOutputModule.outputCommands.append('drop *_muons_*_*')







process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True)
)

process.o = cms.EndPath(process.skimOutputModule)



