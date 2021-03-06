import FWCore.ParameterSet.Config as cms

pfAllChargedHadrons = cms.EDFilter("PdgIdPFCandidateSelector",
    src = cms.InputTag("pfNoPileUpIso"),
    pdgId = cms.vint32(211,-211,321,-321,999211,2212,-2212)
)



