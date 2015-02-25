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

'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_0/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_1/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_2/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_3/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_4/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_5/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_6/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_7/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_8/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_9/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_10/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_11/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_12/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_13/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_14/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_15/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_16/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_17/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_18/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_19/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_20/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_21/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_22/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_23/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_24/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_25/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_26/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_27/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_28/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_29/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_30/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_31/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_32/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_33/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_34/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_35/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_36/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_37/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_38/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_39/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_40/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_41/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_42/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_43/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_44/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_45/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_46/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_47/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_48/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_49/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_50/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_51/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_52/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_53/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_54/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_55/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_56/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_57/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_58/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_59/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_60/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_61/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_62/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_63/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_64/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_65/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_66/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_67/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_68/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_69/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_70/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_71/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_72/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_73/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_74/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_75/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_76/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_77/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_78/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_79/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_80/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_81/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_82/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_83/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_84/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_85/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_86/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_87/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_88/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_89/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_90/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_91/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_92/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_93/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_94/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_95/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_96/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_97/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_98/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_99/step.root'
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_100/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_101/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_102/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_103/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_104/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_105/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_106/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_107/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_108/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_109/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_110/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_111/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_112/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_113/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_114/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_115/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_116/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_117/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_118/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_119/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_120/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_121/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_122/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_123/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_124/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_125/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_126/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_127/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_128/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_129/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_130/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_131/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_132/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_133/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_134/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_135/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_136/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_137/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_138/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_139/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_140/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_141/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_142/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_143/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_144/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_145/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_146/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_147/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_148/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_149/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_150/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_151/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_152/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_153/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_154/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_155/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_156/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_157/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_158/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_159/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_160/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_161/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_162/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_163/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_164/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_165/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_166/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_167/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_168/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_169/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_170/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_171/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_172/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_173/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_174/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_175/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_176/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_177/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_178/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_179/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_180/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_181/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_182/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_183/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_184/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_185/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_186/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_187/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_188/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_189/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_190/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_191/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_192/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_193/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_194/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_195/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_196/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_197/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_198/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_199/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_200/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_201/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_202/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_203/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_204/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_205/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_206/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_207/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_208/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_209/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_210/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_211/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_212/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_213/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_214/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_215/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_216/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_217/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_218/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_219/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_220/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_221/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_222/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_223/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_224/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_225/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_226/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_227/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_228/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_229/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_230/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_231/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_232/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_233/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_234/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_235/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_236/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_237/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_238/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_239/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_240/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_241/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_242/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_243/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_244/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_245/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_246/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_247/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_248/step.root',
'file:/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_249/step.root',
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
