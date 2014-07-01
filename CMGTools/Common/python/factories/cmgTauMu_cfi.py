import FWCore.ParameterSet.Config as cms
from CMGTools.Common.factories.cmgDiObject_cfi import diObjectFactory

tauMuFactory = diObjectFactory.clone(
       leg1Collection = cms.InputTag('slimmedTaus'),
       leg2Collection = cms.InputTag('slimmedMuons'),
       metCollection = cms.InputTag('slimmedMETs')       
)

cmgTauMu = cms.EDFilter(
    "TauMuPOProducer",
    cfg = tauMuFactory.clone(),
    cuts = cms.PSet(),
    )
