# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: SingleTaupt_50_cfi --conditions PHYS14_25_V1 -n 800 --eventcontent AODSIM --datatier AODSIM -s GEN,SIM,DIGI,L1,DIGI2RAW,RAW2DIGI,L1Reco,RECO --customise SLHCUpgradeSimulations/Configuration/postLS1Customs.customisePostLS1 --magField 38T_PostLS1 --fileout file:step.root --no_exec
import FWCore.ParameterSet.Config as cms
from FWCore.ParameterSet.VarParsing import VarParsing


def addWeightedIsolation(process):
    process.load("RecoTauTag.Configuration.HPSPFTaus_cff")
    process.hpsPFTauMVAIsolation2Seq+=process.hpsPFTauMVA3IsolationNeutralIsoPtSumWeight
    return process

options = VarParsing ('analysis')

options.register ('seed',
                  0,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "random seed")

options.parseArguments()

print 'random seed ', options.seed
print 'max events ', options.maxEvents

eMax = 100
if options.maxEvents:
    eMax = options.maxEvents


process = cms.Process('RECO')

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.Geometry.GeometrySimDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_PostLS1_cff')
process.load('Configuration.StandardSequences.Generator_cff')
process.load('IOMC.EventVertexGenerators.VtxSmearedRealistic8TeVCollision_cfi')
process.load('GeneratorInterface.Core.genFilterSummary_cff')
process.load('Configuration.StandardSequences.SimIdeal_cff')
process.load('Configuration.StandardSequences.Digi_cff')
process.load('Configuration.StandardSequences.SimL1Emulator_cff')
process.load('Configuration.StandardSequences.DigiToRaw_cff')
process.load('Configuration.StandardSequences.RawToDigi_cff')
process.load('Configuration.StandardSequences.L1Reco_cff')
process.load('Configuration.StandardSequences.Reconstruction_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(eMax)
)


#import pdb; pdb.set_trace()
#print process.RandomNumberGeneratorService.generator
process.RandomNumberGeneratorService.generator.initialSeed = cms.untracked.uint32(options.seed)

#process.add_( cms.Service("RandomNumberGeneratorService",
#			  #this sets the random number seed used by Pythia
#			  sourceSeed = cms.untracked.uint32(123456789)
#			  )
#	      )

#RandomNumberGeneratorService = cms.Service("RandomNumberGeneratorService",
#    generator = cms.PSet(
#        initialSeed = cms.untracked.uint32(1),
#        engineName = cms.untracked.string('HepJamesRandom')
#    )
#)


# Input source
process.source = cms.Source("EmptySource",
			    )

process.options = cms.untracked.PSet(
    SkipEvent = cms.untracked.vstring('ProductNotFound')
)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    version = cms.untracked.string('$Revision: 1.19 $'),
    annotation = cms.untracked.string('SingleTaupt_50_cfi nevts:800'),
    name = cms.untracked.string('Applications')
)

# Output definition

process.AODSIMoutput = cms.OutputModule("PoolOutputModule",
    compressionLevel = cms.untracked.int32(4),
    compressionAlgorithm = cms.untracked.string('LZMA'),
    eventAutoFlushCompressedSize = cms.untracked.int32(15728640),
    outputCommands = process.AODSIMEventContent.outputCommands,
    fileName = cms.untracked.string('file:step.root'),
    dataset = cms.untracked.PSet(
        filterName = cms.untracked.string(''),
        dataTier = cms.untracked.string('AODSIM')
    ),
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('generation_step')
    )
)

# Additional output definition

process.AODSIMoutput.outputCommands.append('keep *_particleFlowRecHit*_*_*')
process.AODSIMoutput.outputCommands.append('keep recoPFRecHits*_*_*_*')
process.AODSIMoutput.outputCommands.append('keep recoPFClusters*_*_*_*')


process.AODSIMoutput.outputCommands.append('keep *_particleFlowRecHit*_*_*')
process.AODSIMoutput.outputCommands.append('keep recoPFRecHits*_*_*_*')
process.AODSIMoutput.outputCommands.append('keep recoPFClusters*_*_*_*')
process.AODSIMoutput.outputCommands.append('keep *_ecalRecHit*_*_*')

# added after Emmanuelle discussion
process.AODSIMoutput.outputCommands.append('keep *_g4Sim*_*_*')
process.AODSIMoutput.outputCommands.append('keep *_particleFlow*_*_*')
#process.AODSIMoutput.outputCommands.append('drop *_*_*Clean*_*')
#process.AODSIMoutput.outputCommands.append('drop *_ak5*_*_*')
#process.AODSIMoutput.outputCommands.append('drop *_ak8*_*_*')
#process.AODSIMoutput.outputCommands.append('drop *_kt*_*_*')
#process.AODSIMoutput.outputCommands.append('drop *_ca8*_*_*')
process.AODSIMoutput.outputCommands.append('drop *_tevMuons_*_*')
process.AODSIMoutput.outputCommands.append('drop *_generalV0Candidates_*_*')
process.AODSIMoutput.outputCommands.append('drop *_*Digi*_*_*')
process.AODSIMoutput.outputCommands.append('drop *_*l1extraParticles*_*_*')


# Other statements
process.genstepfilter.triggerConditions=cms.vstring("generation_step")
from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'PHYS14_25_V1', '')

process.generator = cms.EDProducer("Pythia6PtGun",
    PGunParameters = cms.PSet(
        MinPhi = cms.double(-3.14159265359),
        MinPt = cms.double(20.0),
        ParticleID = cms.vint32(-15),
        MaxEta = cms.double(2.3),
        MaxPhi = cms.double(3.14159265359),
        MinEta = cms.double(-2.3),
        AddAntiParticle = cms.bool(False),
        MaxPt = cms.double(400.0001)
    ),
    PythiaParameters = cms.PSet(
        pythiaUESettings = cms.vstring('MSTJ(11)=3     ! Choice of the fragmentation function', 
            'MSTJ(22)=2     ! Decay those unstable particles', 
            'PARJ(71)=10 .  ! for which ctau  10 mm', 
            'MSTP(2)=1      ! which order running alphaS', 
            'MSTP(33)=0     ! no K factors in hard cross sections', 
            'MSTP(51)=7     ! structure function chosen', 
            'MSTP(81)=1     ! multiple parton interactions 1 is Pythia default', 
            'MSTP(82)=4     ! Defines the multi-parton model', 
            'MSTU(21)=1     ! Check on possible errors during program execution', 
            'PARP(82)=1.9409   ! pt cutoff for multiparton interactions', 
            'PARP(89)=1960. ! sqrts for which PARP82 is set', 
            'PARP(83)=0.5   ! Multiple interactions: matter distrbn parameter', 
            'PARP(84)=0.4   ! Multiple interactions: matter distribution parameter', 
            'PARP(90)=0.16  ! Multiple interactions: rescaling power', 
            'PARP(67)=2.5    ! amount of initial-state radiation', 
            'PARP(85)=1.0  ! gluon prod. mechanism in MI', 
            'PARP(86)=1.0  ! gluon prod. mechanism in MI', 
            'PARP(62)=1.25   ! ', 
            'PARP(64)=0.2    ! ', 
            'MSTP(91)=1     !', 
            'PARP(91)=2.1   ! kt distribution', 
            'PARP(93)=15.0  ! '),
        parameterSets = cms.vstring('pythiaUESettings', 
            'pythiaTauJets'),
        pythiaTauJets = cms.vstring(
            'MDME(89,1)=0      ! no tau->electron', 
            'MDME(90,1)=0      ! no tau->muon',
#            'MDME(91,1)=1      ! no tau->muon',
#            'MDME(92,1)=1      ! no tau->muon',
#            'MDME(93,1)=1      ! no tau->muon',
#            'MDME(94,1)=1      ! no tau->muon',
#            'MDME(95,1)=0      ! no tau->muon',
#            'MDME(96,1)=0      ! no tau->muon',
#            'MDME(97,1)=0      ! no tau->muon',
#            'MDME(98,1)=0      ! no tau->muon',
#            'MDME(99,1)=0      ! no tau->muon',
#            'MDME(100,1)=0      ! no tau->muon',
#            'MDME(101,1)=0      ! no tau->muon',
#            'MDME(102,1)=0      ! no tau->muon',
#            'MDME(103,1)=0      ! no tau->muon',
#            'MDME(104,1)=0      ! no tau->muon',
#            'MDME(105,1)=0      ! no tau->muon',
#            'MDME(106,1)=0      ! no tau->muon',
#            'MDME(107,1)=0      ! no tau->muon',
#            'MDME(108,1)=0      ! no tau->muon',
#            'MDME(109,1)=0      ! no tau->muon',
#            'MDME(110,1)=1      ! no tau->muon',
#            'MDME(111,1)=0      ! no tau->muon',
#            'MDME(112,1)=0      ! no tau->muon',
#            'MDME(113,1)=0      ! no tau->muon',
#            'MDME(114,1)=0      ! no tau->muon',
#            'MDME(115,1)=0      ! no tau->muon',
#            'MDME(116,1)=0      ! no tau->muon',
#            'MDME(117,1)=0      ! no tau->muon',
#            'MDME(118,1)=0      ! no tau->muon',
#            'MDME(119,1)=0      ! no tau->muon',
#            'MDME(120,1)=0      ! no tau->muon',
#            'MDME(121,1)=0      ! no tau->muon',
#            'MDME(122,1)=0      ! no tau->muon',
#            'MDME(123,1)=0      ! no tau->muon',
#            'MDME(124,1)=0      ! no tau->muon',
#            'MDME(125,1)=0      ! no tau->muon',
#            'MDME(126,1)=0      ! no tau->muon',
#            'MDME(127,1)=0      ! no tau->muon',
#            'MDME(128,1)=0      ! no tau->muon',
#            'MDME(129,1)=0      ! no tau->muon',
#            'MDME(130,1)=0      ! no tau->muon',
#            'MDME(131,1)=0      ! no tau->muon',
#            'MDME(132,1)=0      ! no tau->muon',
#            'MDME(133,1)=0      ! no tau->muon',
#            'MDME(134,1)=0      ! no tau->muon',
#            'MDME(135,1)=0      ! no tau->muon',
#            'MDME(136,1)=0      ! no tau->muon',
#            'MDME(137,1)=0      ! no tau->muon',
#            'MDME(138,1)=0      ! no tau->muon',
#            'MDME(139,1)=0      ! no tau->muon',
#            'MDME(140,1)=0      ! no tau->muon',
#            'MDME(141,1)=0      ! no tau->muon',
#            'MDME(142,1)=0      ! no tau->muon',
            )
	),
)


# Path and EndPath definitions
process.generation_step = cms.Path(process.pgen)
process.simulation_step = cms.Path(process.psim)
process.digitisation_step = cms.Path(process.pdigi)
process.L1simulation_step = cms.Path(process.SimL1Emulator)
process.digi2raw_step = cms.Path(process.DigiToRaw)
process.raw2digi_step = cms.Path(process.RawToDigi)
process.L1Reco_step = cms.Path(process.L1Reco)
process.reconstruction_step = cms.Path(process.reconstruction)
process.genfiltersummary_step = cms.EndPath(process.genFilterSummary)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.AODSIMoutput_step = cms.EndPath(process.AODSIMoutput)

addWeightedIsolation(process)

# Schedule definition
process.schedule = cms.Schedule(process.generation_step,process.genfiltersummary_step,process.simulation_step,process.digitisation_step,process.L1simulation_step,process.digi2raw_step,process.raw2digi_step,process.L1Reco_step,process.reconstruction_step,process.endjob_step,process.AODSIMoutput_step)
# filter all path with the production filter sequence
for path in process.paths:
	getattr(process,path)._seq = process.generator * getattr(process,path)._seq 


#process.load("RecoTauTag.Configuration.RecoPFTauTag_cff")
#for path in process.paths:
#	getattr(process,path)._seq = process.PFTau * getattr(process,path)._seq 


# customisation of the process.

# Automatic addition of the customisation function from SLHCUpgradeSimulations.Configuration.postLS1Customs
from SLHCUpgradeSimulations.Configuration.postLS1Customs import customisePostLS1 

#call to customisation function customisePostLS1 imported from SLHCUpgradeSimulations.Configuration.postLS1Customs
process = customisePostLS1(process)



# End of customisation functions
