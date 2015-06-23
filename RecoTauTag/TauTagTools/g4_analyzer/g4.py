import FWCore.ParameterSet.Config as cms
from FWCore.ParameterSet.VarParsing import VarParsing

options = VarParsing ('analysis')

options.register ('skipEvents',
                  0,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "events to skip")

options.parseArguments()

procName="DMtest"

eMax = 100
if options.maxEvents:
    eMax = options.maxEvents


sEvents=0
if options.skipEvents:
    sEvents=options.skipEvents

discriminatorNew="hpsPFTauDiscriminationByDecayModeFindingNewDMs"
discriminatorOld="hpsPFTauDiscriminationByDecayModeFindingOldDMs"
discriminator="hpsPFTauDiscriminationByDecayModeFinding"

decayMode = 0

DMname=""
if decayMode == 0:
    DMname="DMall"
elif decayMode == 1:
    DMname="DM1p"
elif decayMode == 2:
    DMname="DM1pX"
elif decayMode == 3:
    DMname="DM3p"

#process definition'
procName=procName+DMname
process = cms.Process(procName)

## MessageLogger
process.load("FWCore.MessageLogger.MessageLogger_cfi")


## Options and Output Report
process.options = cms.untracked.PSet( 
    SkipEvent = cms.untracked.vstring('ProductNotFound'),
    wantSummary = cms.untracked.bool(False) 
    )


## Source
process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring(
        '/store/cmst3/user/ytakahas/CMG/QCD_Pt-15to3000_Tune4C_Flat_13TeV_pythia8/Phys14DR-PU20bx25_trkalmb_PHYS14_25_V1-v1/AODSIM/Dynamic95_20150505/aod_1.root'
#        '/store/cmst3/user/ytakahas/CMG/VBF_HToTauTau_M-125_13TeV-powheg-pythia6/Phys14DR-PU20bx25_tsg_PHYS14_25_V1-v2/AODSIM/Dynamic95_20150520/aod_1.root'
#        '/store/cmst3/user/ytakahas/CMG/VBF_HToTauTau_M-125_13TeV-powheg-pythia6/Phys14DR-PU20bx25_tsg_PHYS14_25_V1-v2/AODSIM/Dynamic95_20150505/aod_1.root'
        ),
                            skipEvents = cms.untracked.uint32(sEvents),
                            duplicateCheckMode = cms.untracked.string('noDuplicateCheck'),
)

## Maximal Number of Events
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(eMax) )
#process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(1))

#### included from standard pat template
## Geometry and Detector Conditions (needed for a few patTuple production steps)
process.load("Configuration.Geometry.GeometryIdeal_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
from Configuration.AlCa.autoCond import autoCond
process.GlobalTag.globaltag = cms.string( autoCond[ 'startup' ] )
process.load("Configuration.StandardSequences.MagneticField_cff")



process.options.allowUnscheduled = cms.untracked.bool(False)

process.load("RecoTauTag.Configuration.RecoPFTauTag_cff")
process.load("PhysicsTools.JetMCAlgos.TauGenJets_cfi")
process.load("RecoJets.JetProducers.ak5GenJets_cfi")
process.load("RecoJets.Configuration.GenJetParticles_cff")

#process.load("PhysicsTools.PatAlgos.producersLayer1.patCandidates_cff")
#from PhysicsTools.PatAlgos.tools.tauTools import *
#switchToPFTauHPS(process)

#process.load("TrackingTools/TransientTrack/TransientTrackBuilder_cfi")
from TrackingTools.TransientTrack.TransientTrackBuilder_cfi import TransientTrackBuilderESProducer
process.load("TrackingTools/TransientTrack/TransientTrackBuilder_cfi")

from RecoTauTag.RecoTau.PFRecoTauQualityCuts_cfi import PFTauQualityCuts

process.tauAnalyzer = cms.EDAnalyzer("GeantAnalyzer",
                                     src = cms.InputTag("hpsPFTauProducer","","RECO"),
                                     )

process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")
process.printTree = cms.EDAnalyzer("ParticleListDrawer",
                                    src = cms.InputTag("genParticles"),
                                   maxEventsToPrint  = cms.untracked.int32(100000)
)


## let it run
process.load("CommonTools.ParticleFlow.pfParticleSelection_cff")
process.load("RecoParticleFlow.PFProducer.pfLinker_cff")

process.pfPileUp.PFCandidates = 'particleFlowPtrs'
process.pfNoPileUp.bottomCollection = 'particleFlowPtrs'
process.pfPileUpIso.PFCandidates = 'particleFlowPtrs'
process.pfNoPileUpIso.bottomCollection='particleFlowPtrs'
process.pfPileUpJME.PFCandidates = 'particleFlowPtrs'
process.pfNoPileUpJME.bottomCollection='particleFlowPtrs'


process.p = cms.Path(
    process.printTree*
    process.tauGenJets*
#    process.particleFlowPtrs*
#    process.pfParticleSelectionSequence*
#    process.PFTau*
    process.tauAnalyzer
#        process.tauDifferenceAnalyzer
#        process.patDefaultSequence
            )


#process.TFileService = cms.Service("TFileService", fileName = cms.string("dummy.root"))

## Output Module Configuration (expects a path 'p')
from PhysicsTools.PatAlgos.patEventContent_cff import patEventContentNoCleaning
process.out = cms.OutputModule("PoolOutputModule",
                               fileName = cms.untracked.string('patTuple.root'),
                               ## save only events passing the full path
                               #SelectEvents = cms.untracked.PSet( SelectEvents = cms.vstring('p') ),
                               ## save PAT output; you need a '*' to unpack the list of commands
                               ## 'patEventContent'
                               outputCommands = cms.untracked.vstring('drop *', *patEventContentNoCleaning )
                               )

#process.outpath = cms.EndPath(process.out)

process.options.wantSummary = False
