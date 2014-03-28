import FWCore.ParameterSet.Config as cms

muEleSVFit = cms.EDProducer(
    "MuEleWithSVFitProducer",
    diTauSrc = cms.InputTag("cmgMuEleCorPreSel"),
#    metsigSrc = cms.InputTag("pfMetSignificance"),
    SVFitVersion =  cms.int32(2), # 1 for 2011 version , 2 for new 2012 (slow) version
    verbose = cms.untracked.bool( False )
    )
