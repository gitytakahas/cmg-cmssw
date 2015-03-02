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

'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_0/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_1/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_2/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_3/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_4/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_5/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_6/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_7/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_8/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_9/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_10/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_11/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_12/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_13/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_14/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_15/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_16/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_17/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_18/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_19/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_20/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_21/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_22/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_23/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_24/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_25/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_26/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_27/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_28/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_29/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_30/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_31/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_32/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_33/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_34/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_35/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_36/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_37/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_38/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_39/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_40/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_41/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_42/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_43/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_44/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_45/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_46/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_47/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_48/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_49/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_50/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_51/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_52/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_53/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_54/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_55/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_56/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_57/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_58/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_59/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_60/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_61/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_62/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_63/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_64/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_65/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_66/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_67/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_68/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_69/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_70/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_71/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_72/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_73/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_74/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_75/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_76/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_77/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_78/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_79/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_80/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_81/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_82/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_83/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_84/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_85/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_86/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_87/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_88/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_89/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_90/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_91/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_92/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_93/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_94/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_95/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_96/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_97/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_98/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_99/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_100/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_101/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_102/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_103/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_104/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_105/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_106/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_107/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_108/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_109/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_110/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_111/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_112/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_113/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_114/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_115/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_116/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_117/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_118/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_119/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_120/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_121/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_122/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_123/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_124/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_125/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_126/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_127/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_128/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_129/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_130/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_131/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_132/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_133/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_134/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_135/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_136/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_137/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_138/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_139/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_140/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_141/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_142/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_143/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_144/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_145/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_146/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_147/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_148/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_149/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_150/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_151/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_152/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_153/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_154/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_155/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_156/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_157/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_158/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_159/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_160/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_161/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_162/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_163/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_164/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_165/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_166/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_167/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_168/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_169/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_170/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_171/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_172/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_173/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_174/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_175/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_176/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_177/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_178/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_179/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_180/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_181/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_182/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_183/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_184/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_185/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_186/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_187/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_188/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_189/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_190/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_191/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_192/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_193/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_194/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_195/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_196/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_197/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_198/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_199/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_200/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_201/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_202/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_203/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_204/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_205/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_206/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_207/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_208/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_209/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_210/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_211/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_212/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_213/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_214/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_215/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_216/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_217/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_218/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_219/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_220/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_221/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_222/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_223/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_224/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_225/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_226/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_227/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_228/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_229/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_230/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_231/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_232/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_233/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_234/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_235/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_236/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_237/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_238/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_239/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_240/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_241/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_242/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_243/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_244/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_245/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_246/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_247/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_248/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_249/step.root',
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
                                     genTauSrc = cms.InputTag("tauGenJets"),
                                     disc = cms.InputTag("hpsPFTauDiscriminationByDecayModeFinding", "", "RECO"),
                                     nIso = cms.InputTag("hpsPFTauMVA3IsolationNeutralIsoPtSum","","RECO"),
                                     minIso = cms.double(-1),
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
    process.particleFlowPtrs*
    process.pfParticleSelectionSequence*
    process.PFTau*
    process.tauAnalyzer
#        process.tauDifferenceAnalyzer
#        process.patDefaultSequence
            )


process.TFileService = cms.Service("TFileService", fileName = cms.string("dummy.root"))

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
