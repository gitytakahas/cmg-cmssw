import copy
import os 
import CMGTools.RootTools.fwlite.Config as cfg
from CMGTools.RootTools.fwlite.Config import printComps

from CMGTools.H2TauTau.triggerMap import pathsAndFilters
from CMGTools.H2TauTau.proto.weights.weighttable import mu_id_taumu_2012, mu_iso_taumu_2012
from CMGTools.H2TauTau.proto.samples.sampleShift import selectShift
from CMGTools.RootTools.RootTools import * 

shift = None

tauScaleShift = 1.0
syncntuple = False
simulatedOnly = True # Useful for systematic shifts on simulated samples, e.g. JEC
doThePlot = False # Set to true for the plotting script


# Andrew Summer 13 (MC is identical to the previous one)
puFileMC = '/afs/cern.ch/user/a/agilbert/public/HTT_Pileup/13-09-13/MC_Summer12_PU_S10-600bins.root'
puFileData = '/afs/cern.ch/user/a/agilbert/public/HTT_Pileup/13-09-13/Data_Pileup_2012_ReRecoPixel-600bins.root'

# vertexFileDir = os.environ['CMSSW_BASE'] + '/src/CMGTools/RootTools/data/Reweight/2012/Vertices'
# vertexFileData = '/'.join([vertexFileDir, 'vertices_data_2012A_2012B_start_195947.root'])

mc_vertexWeight = None

mc_tauEffWeight_mc = 'effTau_muTau_MC_2012ABCDSummer13'
mc_muEffWeight_mc = 'effMu_muTau_MC_2012ABCD'
mc_tauEffWeight = 'effTau_muTau_Data_2012ABCDSummer13'
mc_muEffWeight = 'effMu_muTau_Data_2012ABCDSummer13'
    
    
eventSelector = cfg.Analyzer(
    'EventSelector',
    toSelect = [
118190,
 59889,
 34596,
 46131
    ]
    )


jsonAna = cfg.Analyzer(
    'JSONAnalyzer',
    )

triggerAna = cfg.Analyzer(
    'TriggerAnalyzer'
    )

vertexAna = cfg.Analyzer(
    'VertexAnalyzer',
    goodVertices = 'goodPVFilter',
    vertexWeight = mc_vertexWeight,
    fixedWeight = 1,
    verbose = False,
    )

embedWeighter = cfg.Analyzer(
    'EmbedWeighter',
    isRecHit = False,
    verbose = False
    )

pileUpAna = cfg.Analyzer(
    'PileUpAnalyzer',
    true = True
    )

genErsatzAna = cfg.Analyzer(
    'GenErsatzAnalyzer',
    verbose = False
    )

TauMuAna = cfg.Analyzer(
    'TauMuAnalyzer',
    scaleShift1 = tauScaleShift,
    pt1 = 20,
    eta1 = 2.3,
    iso1 = None,
    pt2 = 20,
    eta2 = 2.1,
    iso2 = 0.1,
    m_min = 10,
    m_max = 99999,
    dR_min = 0.5,
    triggerMap = pathsAndFilters,
    mvametsigs = 'mvaMETTauMu',
    verbose = False
    )

dyJetsFakeAna = cfg.Analyzer(
    'DYJetsFakeAnalyzer',
    leptonType = 13,
    src = 'genParticlesPruned',
    )

WNJetsAna = cfg.Analyzer(
    'WNJetsAnalyzer',
    verbose = False
    )

NJetsAna = cfg.Analyzer(
    'NJetsAnalyzer',
    fillTree = True,
    verbose = False
    )

WNJetsTreeAna = cfg.Analyzer(
    'WNJetsTreeAnalyzer'
    )

higgsWeighter = cfg.Analyzer(
    'HiggsPtWeighter',
    src = 'genParticlesPruned',
    )

tauDecayModeWeighter = cfg.Analyzer(
    'TauDecayModeWeighter',
    )

tauFakeRateWeighter = cfg.Analyzer(
    'TauFakeRateWeighter'
    )

tauWeighter = cfg.Analyzer(
    'LeptonWeighter_tau',
    effWeight = mc_tauEffWeight,
    effWeightMC = mc_tauEffWeight_mc,
    lepton = 'leg1',
    verbose = False,
    disable = False,
    )

muonWeighter = cfg.Analyzer(
    'LeptonWeighter_mu',
    effWeight = mc_muEffWeight,
    effWeightMC = mc_muEffWeight_mc,
    lepton = 'leg2',
    verbose = False,
    disable = False,
    idWeight = mu_id_taumu_2012,
    isoWeight = mu_iso_taumu_2012    
    )



# defined for vbfAna and eventSorter
vbfKwargs = dict( Mjj = 500,
                  deltaEta = 3.5    
                  )


jetAna = cfg.Analyzer(
    'JetAnalyzer',
    jetCol = 'cmgPFJetSel',
    jetPt = 20.,
    jetEta = 4.7,
    btagSFseed = 123456,
    relaxJetId = False, 
    jerCorr = False,
    #jesCorr = 1.,
    )

vbfSimpleAna = cfg.Analyzer(
    'VBFSimpleAnalyzer',
    vbfMvaWeights = '',
    cjvPtCut = 30.,
    **vbfKwargs
    
    )


treeProducer = cfg.Analyzer(
    'H2TauTauTreeProducerTauMu'
    )

treeProducerXCheck = cfg.Analyzer(
    'H2TauTauSyncTree',
    pt20 = False
    )

#########################################################################################

from CMGTools.H2TauTau.proto.samples.run2012.tauMu_YutaJan19_tesdown import * 

#########################################################################################

for mc in MC_list:
    mc.puFileMC = puFileMC
    mc.puFileData = puFileData

for emb in embed_list:
    emb.puFileData = None
    emb.puFileMC = None
    
WNJetsAna.nevents = [ WJets.nGenEvents,
                      W1Jets.nGenEvents,
                      W2Jets.nGenEvents,
                      W3Jets.nGenEvents,
                      W4Jets.nGenEvents
                      ]

# Fractions temporarily taken from Jose (29 May 2013):
WNJetsAna.fractions = [0.74392452, 0.175999, 0.0562617, 0.0168926, 0.00692218]

# selectedComponents = allsamples
diboson_list = [    WWJetsTo2L2Nu,
                    WZJetsTo2L2Q,
                    WZJetsTo3LNu,
                    ZZJetsTo2L2Nu,
                    ZZJetsTo2L2Q,
                    ZZJetsTo4L,
                    T_tW,
                    Tbar_tW
                    ]

WJetsSoup = copy.copy(WJets)
WJetsSoup.name = 'WJetsSoup'

DYJetsSoup = copy.copy(DYJets)
DYJetsSoup.name = 'DYJetsSoup'

VVgroup = [comp.name for comp in diboson_list]
if diboson_list == [] and doThePlot:
    VVgroup = None # This is needed for the plotting script

#higgs = mc_higgs
higgs = [c for c in mc_higgs if '125' in c.name]
#higgs = [c for c in mc_higgs if 'VH125' in c.name]

selectedComponents = [TTJetsFullLept,
    TTJetsSemiLept,
    TTJetsHadronic, 
    DYJets, WJets,
    W1Jets, W2Jets, W3Jets, W4Jets,
    W1Jets_ext, W2Jets_ext, W3Jets_ext,
    DY1Jets, DY2Jets, DY3Jets, DY4Jets,
    ]

# FOR PLOTTING:
TTgroup = None
if doThePlot:
    selectedComponents = [TTJetsFullLept,
                          TTJetsSemiLept,
                          TTJetsHadronic, #DYJets, #WJets,
                          WJetsSoup,
                          DYJetsSoup
                          ]
    TTgroup = [TTJetsFullLept.name,
               TTJetsSemiLept.name,
               TTJetsHadronic.name]

if not doThePlot:
    selectedComponents.extend( higgs )
#    selectedComponents.extend( mc_higgs_susy )
else:
#    pass
    selectedComponents.extend( higgs )
#    selectedComponents.extend( mc_higgs_susy )

if not simulatedOnly:
    selectedComponents.extend( data_list )
#    selectedComponents.extend( embed_list )

#selectedComponents = []
#selectedComponents.extend(higgs)

sequence = cfg.Sequence( [
#    eventSelector,
    jsonAna, 
    triggerAna,
    vertexAna, 
    TauMuAna,
    dyJetsFakeAna,
    # WNJetsAna,
    # WNJetsTreeAna,
    NJetsAna,
    higgsWeighter, 
    jetAna,
    vbfSimpleAna,
    pileUpAna,
    embedWeighter,
    tauDecayModeWeighter,
    tauFakeRateWeighter,
    tauWeighter, 
    muonWeighter, 
    treeProducer,
    # treeProducerXCheck
   ] )

if syncntuple:
    sequence.append( treeProducerXCheck) #Yes!

selectedComponents = [comp for comp in selectedComponents if comp.dataset_entries > 0]

test = 2
if test==1:
    comp = W1Jets_ext
    selectedComponents = [comp]
    comp.splitFactor = 1

elif test==2:
#    selectedComponents = [DYJets, DY1Jets, DY2Jets, DY3Jets, DY4Jets]
    selectedComponents = allsamples

    for comp in selectedComponents:
        comp.splitFactor = 250

config = cfg.Config( components = selectedComponents,
                     sequence = sequence )

printComps(config.components, True)
