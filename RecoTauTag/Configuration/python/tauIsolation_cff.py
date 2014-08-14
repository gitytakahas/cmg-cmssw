import FWCore.ParameterSet.Config as cms
import copy

# compute IsoDeposits from all PFCandidates
tauIsoDepositPFCandidates = cms.EDProducer("CandIsoDepositProducer",
    src = cms.InputTag("combinatoricRecoTaus"),
    MultipleDepositsFlag = cms.bool(False),
    trackType = cms.string('candidate'),
    ExtractorPSet = cms.PSet(
        # PFTau specific Extractor, which allows to exclude particles within tau signal cone from IsoDeposit computation
        ComponentName = cms.string('PFTauExtractor'),

        # collection of PFCandidates to be used for IsoDeposit computation
        candidateSource = cms.InputTag("pfPileUpAllChargedParticles"),

        # size of outer cone for which IsoDeposits are computed
        DR_Max = cms.double(0.8),
        # size of inner cone excluded from IsoDeposit computation
        DR_Veto = cms.double(0.),

        # max. distance in z-direction between tau production vertex and PFCandidates included in IsoDeposit computation
        # (cut per default disabled, since well-defined for PFCandidates associated to tracks (PFChargedHadrons) only)
        Diff_z = cms.double(1.e+4),
        # max. distance in x-y between tau production vertex and PFCandidates included in IsoDeposit computation
        # (cut per default disabled, since well-defined for PFCandidates associated to tracks (PFChargedHadrons) only)
        Diff_r = cms.double(1.e+4),

        # collection of PFTaus, needed for excluding particles in tau signal cone from IsoDeposit
        tauSource = cms.InputTag("combinatoricRecoTaus"),
        # maximum distance in eta-phi, needed to match PFTau to direction passed as function argument to Extractor
        dRmatchPFTau = cms.double(0.1),
        # size of cones around tau signal cone particles excluded from IsoDeposit computation
        dRvetoPFTauSignalConeConstituents = cms.double(0.01),

        DepositLabel = cms.untracked.string(''),

        isolationQualityCuts = cms.PSet(
            minTrackPt                   = cms.double(0.5),
            maxTrackChi2                 = cms.double(100.),
            maxTransverseImpactParameter = cms.double(-1.),
            maxDeltaZ                    = cms.double(-1.),
            minTrackVertexWeight         = cms.double(-1.), # Tracks weight in vertex
            minTrackPixelHits            = cms.uint32(0),
            minTrackHits                 = cms.uint32(3),
            minGammaEt                   = cms.double(0.5),
            #useTracksInsteadOfPFHadrons  = cms.bool(False),
        )
    )
)

# compute IsoDeposits from PFChargedHadrons
# (enable cut on z and x-y distance between tau and PFCandidate production vertex)
tauIsoDepositPFChargedHadrons = copy.deepcopy(tauIsoDepositPFCandidates)
tauIsoDepositPFChargedHadrons.ExtractorPSet.candidateSource = cms.InputTag("pfAllChargedHadrons")
tauIsoDepositPFChargedHadrons.ExtractorPSet.DR_Max = cms.double(0.5)
tauIsoDepositPFChargedHadrons.ExtractorPSet.Diff_z = cms.double(0.2)
tauIsoDepositPFChargedHadrons.ExtractorPSet.Diff_r = cms.double(0.1)

# compute IsoDeposits from PFNeutralHadrons
tauIsoDepositPFNeutralHadrons = copy.deepcopy(tauIsoDepositPFChargedHadrons)
tauIsoDepositPFNeutralHadrons.ExtractorPSet.candidateSource = cms.InputTag("pfAllNeutralHadrons")

# compute IsoDeposits from PFGammas
tauIsoDepositPFGammas = copy.deepcopy(tauIsoDepositPFCandidates)
tauIsoDepositPFGammas.ExtractorPSet.candidateSource = cms.InputTag("pfAllPhotons")

RecoPFTauIsolation = cms.Sequence( tauIsoDepositPFCandidates
                                 * tauIsoDepositPFChargedHadrons
                                 * tauIsoDepositPFNeutralHadrons
                                 * tauIsoDepositPFGammas )
