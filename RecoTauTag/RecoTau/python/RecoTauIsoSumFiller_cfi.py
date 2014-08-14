import FWCore.ParameterSet.Config as cms

RecoTauIsoSumFiller = cms.EDProducer(
    "RecoTauIsoSumFiller",
    src = cms.InputTag("combinatoricRecoTaus"),
    pfIsolationValues = cms.PSet(
        pfSumChargedHadronPt = cms.InputTag('tauPFIsoValueCharged05'),
        pfSumPhotonEt = cms.InputTag('tauPFIsoValueGamma05'),
        pfSumNeutralHadronEt= cms.InputTag('tauPFIsoValueNeutral05'),
        pfSumPUPt = cms.InputTag('tauPFIsoValuePU08')
        )
)
