#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "RecoTauTag/RecoTau/interface/RecoTauQualityCuts.h"
#include "RecoTauTag/RecoTau/interface/RecoTauVertexAssociator.h"
#include "PhysicsTools/JetMCUtils/src/JetMCTag.cc"

#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/TauReco/interface/PFTau.h"
#include "DataFormats/TauReco/interface/PFTauFwd.h"
#include "DataFormats/TauReco/interface/PFTauDiscriminator.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/HepMCCandidate/interface/GenParticleFwd.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/JetReco/interface/GenJetCollection.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidateFwd.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/GsfTrackReco/interface/GsfTrack.h"

#include <vector>
#include <string>
#include <sstream>

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "TH1.h"
#include "TProfile.h"
#include "TProfile2D.h"
#include "TH1F.h"
#include "TH2D.h"
#include "TH1D.h"
#include "TTree.h"
#include "TFile.h"

typedef edm::View<reco::GenJet> GenJetView;

class RecoTauDifferenceAnalyzer : public edm::EDFilter {

public:
  explicit RecoTauDifferenceAnalyzer(const edm::ParameterSet& pset);
  virtual ~RecoTauDifferenceAnalyzer() {}
  virtual bool filter(edm::Event& evt, const edm::EventSetup& es);
  virtual void endJob();

private:
  reco::tau::RecoTauQualityCuts qcuts_;
  std::auto_ptr<reco::tau::RecoTauVertexAssociator> vertexAssociator_;
  edm::InputTag src1_;
  edm::InputTag src2_;
  edm::InputTag disc1_;
  edm::InputTag disc2_;
  edm::InputTag jetSrc_;
  edm::InputTag jetSrcCHS_;
  edm::InputTag genSrc_;
  edm::InputTag genTauSrc_;
  edm::InputTag vertexTag_;
  edm::InputTag chIso1_;
  edm::InputTag chIso2_;
  edm::InputTag chIso3_;
  edm::InputTag nIso1_;
  edm::InputTag nIso2_;
  edm::InputTag nIso3_;
  edm::InputTag PUIso1_;
  edm::InputTag PUIso2_;
  edm::InputTag PUIso3_;
  edm::InputTag cmbIso1_;
  edm::InputTag cmbIso2_;
  edm::InputTag muon_;
  double matchingDistance_;

  /* branch definition */

  Int_t debug_counter = 0;

  TTree* isoTuple_;
  Int_t _eventNum_;
  Int_t _success_;
  Int_t _match_gen_;
  Int_t _gen_dm_;
  Int_t _nvtx_close_;
  Float_t _gen_tau_z_;
  Float_t _vtx_density_;
  Float_t _gen_dr_;
  Int_t _nVx_;
  Int_t _nmuon_;
  Float_t  _vtx_z_;
  Int_t _vtx_isFake_;
  Float_t _vtx_rho_;
  Float_t _vtx_ndof_;
  Float_t _vtx_chi2_;  
  Float_t  _tauvispt_;
  Float_t  _tauviseta_;
  Float_t  _jet_pt_;
  Float_t  _jet_eta_;
  Float_t  _jet_phi_;
  Float_t  _pt_;
  Float_t _eta_;
  Float_t _phi_;
  Float_t _m_;
  Float_t _z_;
  Float_t _chIso_;
  Float_t _nIso_;
  Float_t _puIso_;
  Float_t _chIsoNew_;
  Float_t _nIsoNew_;
  Float_t _puIsoNew_;
  Float_t _cmbIso_;
  Float_t _vz_;
  Float_t _track_pt_;
  Float_t _track_eta_;
  Float_t _track_phi_;
  Float_t _track_chi_;
  Float_t _track_dz_;
  Float_t _track_dxy_;
  Int_t _track_nhit_;
  Int_t  _match_;
  Int_t  _dmf_;
  Int_t  _ncharged_;
  Int_t  _npizero_;

  Float_t  _jet_pt2_;
  Float_t  _jet_eta2_;
  Float_t  _jet_phi2_;
  Float_t  _pt2_;
  Float_t _eta2_;
  Float_t _phi2_;
  Float_t _m2_;
  Float_t _z2_;
  Float_t _chIso2_;
  Float_t _nIso2_;
  Float_t _puIso2_;
  Float_t _cmbIso2_;
  Float_t _vz2_;
  Float_t _track_pt2_;
  Float_t _track_eta2_;
  Float_t _track_phi2_;
  Float_t _track_chi2_;
  Float_t _track_dz2_;
  Float_t _track_dxy2_;
  Int_t _track_nhit2_;
  Int_t  _dmf2_;
  Int_t  _ncharged2_;
  Int_t  _npizero2_;
  Float_t _closest_jet_pt_;
  Float_t _closest_jet_eta_;
  Float_t _closest_jet_phi_;
  Float_t _closest_jet_dr_;


  TTree* eventTuple_;
  Int_t _nak5jet_;
  Int_t _nak5jetCHS_;
  Int_t _ntau_;
  Int_t _ntauCHS_;
  Int_t _ngentau_;


  TTree* debugTuple_;
  Int_t _evt_;
  Float_t _matchingDistance_;
  std::vector<int> d_vtx_isfake;
  std::vector<float> d_vtx_x;
  std::vector<float> d_vtx_y;
  std::vector<float> d_vtx_z;
  std::vector<float> d_vtx_ndof;
  std::vector<float> d_vtx_rho;

  std::vector<float> d_tau_pt;
  std::vector<float> d_tau_eta;
  std::vector<float> d_tau_phi;
  std::vector<float> d_tau_z;
  std::vector<float> d_tau_jet_pt;
  std::vector<float> d_tau_jet_eta;
  std::vector<float> d_tau_jet_phi;
  std::vector<int> d_tau_ncharged;
  std::vector<int> d_tau_npizero;
  std::vector<int> d_tau_ngamma;
  std::vector<int> d_tau_dmf;
  std::vector<int> d_tau_id;
  std::vector<int> d_tau_pf_id;
  std::vector<float> d_tau_pf_eta;
  std::vector<float> d_tau_pf_phi;
  std::vector<float> d_tau_pf_pt;
  std::vector<int> d_tau_pf_type;
  std::vector<float> d_tau_pf_dz;
  std::vector<float> d_tau_pf_dzmin;
  std::vector<int> d_tau_jet_pf_id;
  std::vector<float> d_tau_jet_pf_eta;
  std::vector<float> d_tau_jet_pf_phi;
  std::vector<float> d_tau_jet_pf_pt;
  std::vector<int> d_tau_jet_pf_type;
  std::vector<float> d_tau_jet_pf_dz;
  std::vector<float> d_tau_jet_pf_dzmin;
  
  std::vector<float> d_tauchs_pt;
  std::vector<float> d_tauchs_eta;
  std::vector<float> d_tauchs_phi;
  std::vector<float> d_tauchs_z;
  std::vector<float> d_tauchs_jet_pt;
  std::vector<float> d_tauchs_jet_eta;
  std::vector<float> d_tauchs_jet_phi;
  std::vector<int> d_tauchs_ncharged;
  std::vector<int> d_tauchs_npizero;
  std::vector<int> d_tauchs_ngamma;
  std::vector<int> d_tauchs_dmf;
  
  std::vector<float> d_jet_pt;
  std::vector<float> d_jet_eta;
  std::vector<float> d_jet_phi;

  std::vector<float> d_jetchs_pt;
  std::vector<float> d_jetchs_eta;
  std::vector<float> d_jetchs_phi;
  std::vector<int> d_jetchs_id;
  std::vector<int> d_jetchs_pf_id;
  std::vector<float> d_jetchs_pf_eta;
  std::vector<float> d_jetchs_pf_phi;
  std::vector<float> d_jetchs_pf_pt;
  std::vector<int> d_jetchs_pf_type;
  std::vector<float> d_jetchs_pf_dz;
  std::vector<float> d_jetchs_pf_dzmin;


  std::vector<float> d_gen_pt;
  std::vector<float> d_gen_eta;
  std::vector<float> d_gen_phi;
  std::vector<float> d_gen_z;
  std::vector<int> d_gen_mode;
  
};


Int_t decaymodeid(std::string str){
  if(str=="electron") return 0;
  else if(str=="muon") return 1;
  else if(str=="oneProng0Pi0") return 2;
  else if(str=="oneProng1Pi0") return 3;
  else if(str=="oneProng2Pi0") return 4;
  else if(str=="oneProngOther") return 5;  
  else if(str=="threeProng0Pi0") return 6;
  else if(str=="threeProng1Pi0") return 7;
  else if(str=="threeProngOther") return 8;
  else if(str=="rare") return 9;
  else return -1;
}

std::string decaymodeName(Int_t dm){

  std::string dm_string;
  if      ( dm == reco::PFTau::kOneProng0PiZero   ) dm_string = "OneProng0PiZero";
  else if ( dm == reco::PFTau::kOneProng1PiZero   ) dm_string = "OneProng1PiZero";
  else if ( dm == reco::PFTau::kOneProng2PiZero   ) dm_string = "OneProng2PiZero";
  else if ( dm == reco::PFTau::kTwoProng0PiZero   ) dm_string = "TwoProng0PiZero";
  else if ( dm == reco::PFTau::kTwoProng1PiZero   ) dm_string = "TwoProng1PiZero";
  else if ( dm == reco::PFTau::kThreeProng0PiZero ) dm_string = "ThreeProng0PiZero";
  else if ( dm == reco::PFTau::kThreeProng0PiZero ) dm_string = "ThreeProng1PiZero";
  else dm_string = "Rare";
  return dm_string;
}



std::string getPFCandidateType(reco::PFCandidate::ParticleType pfCandidateType){
  if ( pfCandidateType == reco::PFCandidate::X ) return "undefined";
  else if ( pfCandidateType == reco::PFCandidate::h ) return "PFChargedHadron";
  else if ( pfCandidateType == reco::PFCandidate::e ) return "PFElectron";
  else if ( pfCandidateType == reco::PFCandidate::mu ) return "PFMuon";
  else if ( pfCandidateType == reco::PFCandidate::gamma ) return "PFGamma";
  else if ( pfCandidateType == reco::PFCandidate::h0 ) return "PFNeutralHadron";
  else if ( pfCandidateType == reco::PFCandidate::h_HF ) return "HF_had";
  else if ( pfCandidateType == reco::PFCandidate::egamma_HF ) return "HF_em";
  else assert(0);
}


int getPFCandidateTypeID(reco::PFCandidate::ParticleType pfCandidateType){
  if ( pfCandidateType == reco::PFCandidate::X ) return -1;
  else if ( pfCandidateType == reco::PFCandidate::h ) return 0;
  else if ( pfCandidateType == reco::PFCandidate::e ) return 1;
  else if ( pfCandidateType == reco::PFCandidate::mu ) return 2;
  else if ( pfCandidateType == reco::PFCandidate::gamma ) return 3;
  else if ( pfCandidateType == reco::PFCandidate::h0 ) return 4;
  else if ( pfCandidateType == reco::PFCandidate::h_HF ) return 5;
  else if ( pfCandidateType == reco::PFCandidate::egamma_HF ) return 6;
  else assert(0);
}



void printPFCandidates(const std::vector<reco::PFCandidatePtr>& pfCandidates, 
		       const reco::Vertex::Point& evtVertexPos){
  int idx = 0;

  for ( std::vector<reco::PFCandidatePtr>::const_iterator pfCandidate = pfCandidates.begin();
	pfCandidate != pfCandidates.end(); ++pfCandidate ) {

    std::cout << getPFCandidateType((*pfCandidate)->particleId()) << " #" << idx << ": Pt = " << (*pfCandidate)->pt() << ","
	      << " eta = " << (*pfCandidate)->eta() << ", phi = " << (*pfCandidate)->phi() << ", mass = " << (*pfCandidate)->mass() << std::endl;

    std::cout << std::endl;
    ++idx;
  }
}


RecoTauDifferenceAnalyzer::RecoTauDifferenceAnalyzer(const edm::ParameterSet& pset): 

  qcuts_(pset.exists("qualityCuts") ? pset.getParameterSet("qualityCuts").getParameterSet("isolationQualityCuts") : pset.getParameterSet("qualityCuts")){

  
  vertexAssociator_.reset(new reco::tau::RecoTauVertexAssociator(pset.getParameterSet("qualityCuts"),consumesCollector()));
  

  src1_ = pset.getParameter<edm::InputTag>("src1");
  src2_ = pset.getParameter<edm::InputTag>("src2");
  disc1_ = pset.getParameter<edm::InputTag>("disc1");
  disc2_ = pset.getParameter<edm::InputTag>("disc2");
  genSrc_= pset.getParameter<edm::InputTag>("genSrc");
  genTauSrc_ = pset.getParameter<edm::InputTag>("genTauSrc");
  jetSrc_ = pset.getParameter<edm::InputTag>("jetSrc");
  jetSrcCHS_ = pset.getParameter<edm::InputTag>("jetSrcCHS");
  matchingDistance_ = pset.getParameter<double>("matchingDistance");
  vertexTag_ = pset.getParameter<edm::InputTag>("primaryVertexSrc");  
  chIso1_ = pset.getParameter<edm::InputTag>("chIso1");
  chIso2_ = pset.getParameter<edm::InputTag>("chIso2");
  chIso3_ = pset.getParameter<edm::InputTag>("chIso3");
  nIso1_ = pset.getParameter<edm::InputTag>("nIso1");
  nIso2_ = pset.getParameter<edm::InputTag>("nIso2");
  nIso3_ = pset.getParameter<edm::InputTag>("nIso3");
  PUIso1_ = pset.getParameter<edm::InputTag>("PUIso1");
  PUIso2_ = pset.getParameter<edm::InputTag>("PUIso2");
  PUIso3_ = pset.getParameter<edm::InputTag>("PUIso3");
  cmbIso1_ = pset.getParameter<edm::InputTag>("cmbIso1");
  cmbIso2_ = pset.getParameter<edm::InputTag>("cmbIso2");
  muon_ = pset.getParameter<edm::InputTag>("muon");


  isoTuple_= new TTree("isoTuple","isoTuple");
  isoTuple_->Branch("nVx",&_nVx_, "_nVx_/I");
  isoTuple_->Branch("nmuon",&_nmuon_, "_nmuon_/I");
  isoTuple_->Branch("eventNum",&_eventNum_,"_eventNum_/I");
  isoTuple_->Branch("match_gen",&_match_gen_,"_matchgen_/I");
  isoTuple_->Branch("gen_dm",&_gen_dm_,"_gen_dm_/I");
  isoTuple_->Branch("gen_dr",&_gen_dr_,"_gen_dr_/F");
  isoTuple_->Branch("gen_tau_z",&_gen_tau_z_,"_gen_tau_z_/F");
  isoTuple_->Branch("vtx_density",&_vtx_density_,"_vtx_density_/F");
  isoTuple_->Branch("nvtx_close",&_nvtx_close_,"_nvtx_close_/I");

  isoTuple_->Branch("pt",&_pt_,"_pt_/F");
  isoTuple_->Branch("eta", &_eta_,"_eta_/F");
  isoTuple_->Branch("phi",&_phi_, "_phi_/F");
  isoTuple_->Branch("vtx_z",&_vtx_z_, "_vtx_z_/F");
  isoTuple_->Branch("vtx_isFake",&_vtx_isFake_, "_vtx_isFake_/I");
  isoTuple_->Branch("vtx_rho",&_vtx_rho_, "_vtx_rho_/F");
  isoTuple_->Branch("vtx_ndof",&_vtx_ndof_, "_vtx_ndof_/F");
  isoTuple_->Branch("vtx_chi2",&_vtx_chi2_, "_vtx_chi2_/F");
  isoTuple_->Branch("tauvispt",&_tauvispt_, "_tauvispt_/F");
  isoTuple_->Branch("tauviseta",&_tauviseta_, "_tauviseta_/F");
  isoTuple_->Branch("jet_pt",&_jet_pt_,"_jet_pt_/F");
  isoTuple_->Branch("jet_eta",&_jet_eta_,"_jet_eta_/F");
  isoTuple_->Branch("jet_phi",&_jet_phi_,"_jet_phi_/F");
  isoTuple_->Branch("jet_pt2",&_jet_pt2_,"_jet_pt2_/F");
  isoTuple_->Branch("jet_eta2",&_jet_eta2_,"_jet_eta2_/F");
  isoTuple_->Branch("jet_phi2",&_jet_phi2_,"_jet_phi2_/F");
  isoTuple_->Branch("m",&_m_, "_m_/F");
  isoTuple_->Branch("z",&_z_, "_z_/F");
  isoTuple_->Branch("chIso",&_chIso_, "_chIso_/F");
  isoTuple_->Branch("nIso",&_nIso_, "_nIso_/F");
  isoTuple_->Branch("puIso",&_puIso_, "_puIso_/F");
  isoTuple_->Branch("chIsoNew",&_chIsoNew_, "_chIsoNew_/F");
  isoTuple_->Branch("nIsoNew",&_nIsoNew_, "_nIsoNew_/F");
  isoTuple_->Branch("puIsoNew",&_puIsoNew_, "_puIsoNew_/F");
  isoTuple_->Branch("cmbIso",&_cmbIso_, "_cmbIso_/F");
  isoTuple_->Branch("vz",&_vz_, "_vz_/F");
  isoTuple_->Branch("track_pt",&_track_pt_, "_track_pt_/F");
  isoTuple_->Branch("track_eta",&_track_eta_, "_track_eta_/F");
  isoTuple_->Branch("track_phi",&_track_phi_, "_track_phi_/F");
  isoTuple_->Branch("track_chi",&_track_chi_, "_track_chi_/F");
  isoTuple_->Branch("track_nhit",&_track_nhit_, "_track_nhit_/I");
  isoTuple_->Branch("match",&_match_, "_match_/I");
  isoTuple_->Branch("dmf",&_dmf_, "_dmf_/I");
  isoTuple_->Branch("ncharged",&_ncharged_, "_ncharged_/I");
  isoTuple_->Branch("npizero",&_npizero_, "_npizero_/I");

  isoTuple_->Branch("pt2",&_pt2_,"_pt2_/F");
  isoTuple_->Branch("eta", &_eta2_,"_eta2_/F");
  isoTuple_->Branch("phi2",&_phi2_, "_phi2_/F");
  isoTuple_->Branch("m2",&_m2_, "_m2_/F");
  isoTuple_->Branch("z2",&_z2_, "_z2_/F");
  isoTuple_->Branch("chIso2",&_chIso2_, "_chIso2_/F");
  isoTuple_->Branch("nIso2",&_nIso2_, "_nIso2_/F");
  isoTuple_->Branch("puIso2",&_puIso2_, "_puIso2_/F");
  isoTuple_->Branch("cmbIso2",&_cmbIso2_, "_cmbIso2_/F");
  isoTuple_->Branch("vz2",&_vz2_, "_vz2_/F");
  isoTuple_->Branch("dmf2",&_dmf2_, "_dmf2_/I");
  isoTuple_->Branch("ncharged2",&_ncharged2_, "_ncharged2_/I");
  isoTuple_->Branch("npizero2",&_npizero2_, "_npizero2_/I");
  isoTuple_->Branch("track_pt2",&_track_pt2_, "_track_pt2_/F");
  isoTuple_->Branch("track_eta2",&_track_eta2_, "_track_eta2_/F");
  isoTuple_->Branch("track_phi2",&_track_phi2_, "_track_phi2_/F");
  isoTuple_->Branch("track_chi2",&_track_chi2_, "_track_chi2_/F");
  isoTuple_->Branch("track_nhit2",&_track_nhit2_, "_track_nhit2_/I");
  isoTuple_->Branch("closest_jet_pt",&_closest_jet_pt_, "_closest_jet_pt_/F");
  isoTuple_->Branch("closest_jet_eta",&_closest_jet_eta_, "_closest_jet_eta_/F");
  isoTuple_->Branch("closest_jet_phi",&_closest_jet_phi_, "_closest_jet_phi_/F");
  isoTuple_->Branch("closest_jet_dr",&_closest_jet_dr_, "_closest_jet_dr_/F");


  eventTuple_= new TTree("eventTuple","eventTuple");
  eventTuple_->Branch("nak5jet",&_nak5jet_, "_nak5jet_/I");
  eventTuple_->Branch("nak5jetCHS",&_nak5jetCHS_, "_nak5jetCHS_/I");
  eventTuple_->Branch("ntau",&_ntau_, "_ntau_/I");
  eventTuple_->Branch("ntauCHS",&_ntauCHS_, "_ntauCHS_/I");
  eventTuple_->Branch("ngentau",&_ngentau_, "_ngentau_/I");

  debugTuple_= new TTree("debugTuple","debugTuple");
  debugTuple_->Branch("evt",&_evt_,"_evt_/I");
  debugTuple_->Branch("matchingDistance",&_matchingDistance_,"_matchingDistance_/F");
  debugTuple_->Branch("success",&_success_,"_success_/I");
  debugTuple_->Branch("d_vtx_x", &d_vtx_x);
  debugTuple_->Branch("d_vtx_y", &d_vtx_y);
  debugTuple_->Branch("d_vtx_z", &d_vtx_z);
  debugTuple_->Branch("d_vtx_isfake", &d_vtx_isfake);
  debugTuple_->Branch("d_vtx_ndof", &d_vtx_ndof);
  debugTuple_->Branch("d_vtx_rho", &d_vtx_rho);

  debugTuple_->Branch("d_tau_pt",&d_tau_pt);
  debugTuple_->Branch("d_tau_eta",&d_tau_eta);
  debugTuple_->Branch("d_tau_phi",&d_tau_phi);
  debugTuple_->Branch("d_tau_z",&d_tau_z);
  debugTuple_->Branch("d_tau_npizero",&d_tau_npizero);
  debugTuple_->Branch("d_tau_ncharged",&d_tau_ncharged);
  debugTuple_->Branch("d_tau_ngamma",&d_tau_ngamma);
  debugTuple_->Branch("d_tau_jet_pt",&d_tau_jet_pt);
  debugTuple_->Branch("d_tau_jet_eta",&d_tau_jet_eta);
  debugTuple_->Branch("d_tau_jet_phi",&d_tau_jet_phi);
  debugTuple_->Branch("d_tau_dmf",&d_tau_dmf);
  debugTuple_->Branch("d_tau_id",&d_tau_id);
  debugTuple_->Branch("d_tau_pf_id",&d_tau_pf_id);
  debugTuple_->Branch("d_tau_pf_eta",&d_tau_pf_eta);
  debugTuple_->Branch("d_tau_pf_phi",&d_tau_pf_phi);
  debugTuple_->Branch("d_tau_pf_pt",&d_tau_pf_pt);
  debugTuple_->Branch("d_tau_pf_type",&d_tau_pf_type);
  debugTuple_->Branch("d_tau_pf_dz",&d_tau_pf_dz);
  debugTuple_->Branch("d_tau_pf_dzmin",&d_tau_pf_dzmin);
  debugTuple_->Branch("d_tau_jet_pf_id",&d_tau_jet_pf_id);
  debugTuple_->Branch("d_tau_jet_pf_eta",&d_tau_jet_pf_eta);
  debugTuple_->Branch("d_tau_jet_pf_phi",&d_tau_jet_pf_phi);
  debugTuple_->Branch("d_tau_jet_pf_pt",&d_tau_jet_pf_pt);
  debugTuple_->Branch("d_tau_jet_pf_type",&d_tau_jet_pf_type);
  debugTuple_->Branch("d_tau_jet_pf_dz",&d_tau_jet_pf_dz);
  debugTuple_->Branch("d_tau_jet_pf_dzmin",&d_tau_jet_pf_dzmin);

  
  debugTuple_->Branch("d_tauchs_pt",&d_tauchs_pt);
  debugTuple_->Branch("d_tauchs_eta",&d_tauchs_eta);
  debugTuple_->Branch("d_tauchs_phi",&d_tauchs_phi);
  debugTuple_->Branch("d_tauchs_z",&d_tauchs_z);
  debugTuple_->Branch("d_tauchs_jet_pt",&d_tauchs_jet_pt);
  debugTuple_->Branch("d_tauchs_jet_eta",&d_tauchs_jet_eta);
  debugTuple_->Branch("d_tauchs_jet_phi",&d_tauchs_jet_phi);
  debugTuple_->Branch("d_tauchs_dmf",&d_tauchs_dmf);
  debugTuple_->Branch("d_tauchs_npizero",&d_tauchs_npizero);
  debugTuple_->Branch("d_tauchs_ncharged",&d_tauchs_ncharged);
  debugTuple_->Branch("d_tauchs_ngamma",&d_tauchs_ngamma);

  debugTuple_->Branch("d_jet_pt",&d_jet_pt);
  debugTuple_->Branch("d_jet_eta",&d_jet_eta);
  debugTuple_->Branch("d_jet_phi",&d_jet_phi);

  debugTuple_->Branch("d_jetchs_pt",&d_jetchs_pt);
  debugTuple_->Branch("d_jetchs_eta",&d_jetchs_eta);
  debugTuple_->Branch("d_jetchs_phi",&d_jetchs_phi);
  debugTuple_->Branch("d_jetchs_id",&d_jetchs_id);
  debugTuple_->Branch("d_jetchs_pf_id",&d_jetchs_pf_id);
  debugTuple_->Branch("d_jetchs_pf_eta",&d_jetchs_pf_eta);
  debugTuple_->Branch("d_jetchs_pf_phi",&d_jetchs_pf_phi);
  debugTuple_->Branch("d_jetchs_pf_pt",&d_jetchs_pf_pt);
  debugTuple_->Branch("d_jetchs_pf_type",&d_jetchs_pf_type);
  debugTuple_->Branch("d_jetchs_pf_dz",&d_jetchs_pf_dz);
  debugTuple_->Branch("d_jetchs_pf_dzmin",&d_jetchs_pf_dzmin);


  debugTuple_->Branch("d_gen_pt",&d_gen_pt);
  debugTuple_->Branch("d_gen_eta",&d_gen_eta);
  debugTuple_->Branch("d_gen_phi",&d_gen_phi);
  debugTuple_->Branch("d_gen_mode",&d_gen_mode);
  debugTuple_->Branch("d_gen_z",&d_gen_z);

}

namespace {
  reco::PFJetRef getJetRef(const reco::PFTau& tau) {
    if (tau.jetRef().isNonnull()){
      return tau.jetRef();
    }else if (tau.pfTauTagInfoRef()->pfjetRef().isNonnull()){
      std::cout << "This is pftautaginforef" << std::endl;
      return tau.pfTauTagInfoRef()->pfjetRef();
    }else{
      throw cms::Exception("cant find jet ref");
    }
  }
}

bool RecoTauDifferenceAnalyzer::filter(edm::Event& evt, const edm::EventSetup& es) {


  edm::Handle<reco::PFTauCollection> taus1;
  evt.getByLabel(src1_, taus1);
  edm::Handle<reco::PFTauCollection> taus2;
  evt.getByLabel(src2_, taus2);
  edm::Handle<reco::GenParticleCollection> genParticles;
  evt.getByLabel(genSrc_, genParticles);
  edm::Handle<std::vector<reco::GenJet> > genTaus;
  evt.getByLabel(genTauSrc_, genTaus);
  edm::Handle<std::vector<reco::PFJet> > ak5jet;
  evt.getByLabel(jetSrc_, ak5jet);
  edm::Handle<std::vector<reco::PFJet> > ak5jetCHS;
  evt.getByLabel(jetSrcCHS_, ak5jetCHS);
  edm::Handle<reco::PFTauDiscriminator> disc1;
  evt.getByLabel(disc1_, disc1);
  edm::Handle<reco::PFTauDiscriminator> disc2;
  evt.getByLabel(disc2_, disc2);
  edm::Handle<reco::PFTauDiscriminator> chIso1;
  evt.getByLabel(chIso1_,chIso1);
  edm::Handle<reco::PFTauDiscriminator> chIso2;
  evt.getByLabel(chIso2_,chIso2);
  edm::Handle<reco::PFTauDiscriminator> chIso3;
  evt.getByLabel(chIso3_,chIso3);
  edm::Handle<reco::PFTauDiscriminator> nIso1;
  evt.getByLabel(nIso1_,nIso1);
  edm::Handle<reco::PFTauDiscriminator> nIso2;
  evt.getByLabel(nIso2_,nIso2);
  edm::Handle<reco::PFTauDiscriminator> nIso3;
  evt.getByLabel(nIso3_,nIso3);
  edm::Handle<reco::PFTauDiscriminator> PUIso1;
  evt.getByLabel(PUIso1_,PUIso1);
  edm::Handle<reco::PFTauDiscriminator> PUIso2;
  evt.getByLabel(PUIso2_,PUIso2);
  edm::Handle<reco::PFTauDiscriminator> PUIso3;
  evt.getByLabel(PUIso3_,PUIso3);
  edm::Handle<reco::PFTauDiscriminator> cmbIso1;
  evt.getByLabel(cmbIso1_,cmbIso1);
  edm::Handle<reco::PFTauDiscriminator> cmbIso2;
  evt.getByLabel(cmbIso2_,cmbIso2);

  edm::Handle<std::vector<reco::Muon> > muon;
  evt.getByLabel(muon_, muon);

  Int_t nmuon = 0;
  for (size_t ii = 0; ii < muon->size(); ++ii){
    const reco::Muon &imuon = (*muon)[ii];

    if(imuon.isGlobalMuon()==1 &&
       imuon.isPFMuon()==1 && 
       imuon.pt() > 10 && TMath::Abs(imuon.eta()) < 2.3
       ) nmuon += 1;
  }


  edm::Handle<reco::VertexCollection> verticesH_;
  evt.getByLabel(vertexTag_, verticesH_);
  int nVx = verticesH_->size();
  vertexAssociator_->setEvent(evt);
  reco::Vertex::Point evtVertexPos;
  if ( verticesH_->size() > 0 ) evtVertexPos = verticesH_->front().position();

  Float_t min_vtx_dz = 1000;

  for (reco::VertexCollection::const_iterator vit=verticesH_->begin(); vit!=verticesH_->end(); vit++){

    if(vit->position().Z()==evtVertexPos.Z()) continue;

    Float_t _dz_ = TMath::Abs(vit->position().Z() - evtVertexPos.Z());
    if(min_vtx_dz > _dz_){
      min_vtx_dz = _dz_;
    }
  }
 

  Bool_t debugmode = false;

  for (size_t iTau2 = 0; iTau2 < taus2->size(); ++iTau2) { // PFtau
    reco::PFTauRef tau2(taus2, iTau2);

    bool match_gen = false;
    Float_t match_gen_pt = -1;
    Float_t match_gen_eta = -1;
    Int_t gen_dm = -1;
    Float_t match_gen_dr = 1000;
    Float_t gen_tau_z = -99;
    Int_t nvtx_close = 0;
      
    for(size_t i = 0; i < genTaus->size(); ++ i){
      
      const reco::GenJet & TauCand = (*genTaus)[i];
      reco::Particle::LorentzVector visibleP4 = ((*genTaus)[i]).p4();
      
      if(visibleP4.pt() < 5.0) continue;
      if(TMath::Abs(visibleP4.eta()) > 2.3) continue;

      const std::vector <const reco::GenParticle*> mRefs = TauCand.getGenConstituents();
      unsigned int decayMode = 0; // 0 = hadronic, 1=electron, 2=muon 
      Float_t _tau_z_ = -99;

      for(size_t igTauD =0; igTauD < mRefs.size(); igTauD++) {
	if(abs(mRefs[igTauD]->pdgId())==11) decayMode = 1;
	if(abs(mRefs[igTauD]->pdgId())==13) decayMode = 2;
	_tau_z_ = mRefs[igTauD]->vertex().z();
      }
      
      if(decayMode!=0) continue; 


      double dR_MC = deltaR(tau2->p4(),((*genTaus)[i]).p4());


      if(dR_MC < matchingDistance_){
	match_gen = true;
	match_gen_pt = visibleP4.pt();
	match_gen_eta = visibleP4.eta();
	match_gen_dr = dR_MC;
	gen_dm = decaymodeid(genTauDecayMode(TauCand));
	gen_tau_z = _tau_z_;
	
	for (reco::VertexCollection::const_iterator vit=verticesH_->begin(); vit!=verticesH_->end(); vit++){
	  Float_t _dz_ = TMath::Abs(vit->position().Z() - _tau_z_);
	  if(_dz_ < 0.5){
	    nvtx_close ++;
	  }
	}
      }
    }

    if(match_gen==false) continue;

    std::cout << "tau_dmf : " << ((*disc2)[tau2] < 0.5) << std::endl;

    if((*disc2)[tau2] < 0.5) continue;

    bool match_tau1 = false;
    reco::PFTauRef bestMatch;
    Float_t _min_dr_ = 100;

    for (size_t iTau1 = 0; iTau1 < taus1->size(); ++iTau1) {
      reco::PFTauRef tau1(taus1, iTau1);
      
      double dR_MC = deltaR(tau1->p4(), tau2->p4());

      if(dR_MC < _min_dr_ && dR_MC < matchingDistance_){
	_min_dr_ = dR_MC;
	match_tau1 = true;
	bestMatch = tau1;
      }
    }


    Float_t min_dr_jet = 100;
    reco::PFJet bestMatchJet;
    for(size_t i = 0; i < ak5jetCHS->size(); ++ i) {
      const reco::PFJet &jet = (*ak5jetCHS)[i];
           
      double dR_jet = deltaR(tau2->p4(), jet.p4());
      
      if(dR_jet < min_dr_jet){
	min_dr_jet = dR_jet;
	bestMatchJet = jet;
      }
    }


    reco::PFJetRef ass_jet = getJetRef(*tau2);

    double vz1 = -99;
    double track_pt1 = -99;
    double track_eta1 = -99;
    double track_phi1 = -99;
    double track_chi1 = -99;
    double track_dz1 = -99;
    double track_dxy1 = -99;
    int track_nhit1 = -99;

    int result2 = -99; 
    double pt2 = -99; 
    double eta2 = -99;
    double phi2 = -99;
    double z2 = -99;
    double vz2 = -99;
    double track_pt2 = -99;
    double track_eta2 = -99;
    double track_phi2 = -99;
    double track_chi2 = -99;
    double track_dz2 = -99;
    double track_dxy2 = -99;
    int track_nhit2 = -99;
    double mass2 = -99;
    double ResultChIso2 = -99;
    double ResultNIso2 = -99; 
    double ResultPUIso2 = -99; 
    double ResultChIso2New = -99;
    double ResultNIso2New = -99; 
    double ResultPUIso2New = -99; 
    double ResultCmbIso2 = -99;     
    double jet_pt2 = -99;
    double jet_eta2 = -99;
    double jet_phi2 = -99;
    int ncharged2 = -99;
    int npizero2 = -99;
    
    
    if(tau2->leadPFChargedHadrCand().isNonnull() && tau2->leadPFChargedHadrCand()->trackRef().isNonnull()){
      vz1 = tau2->leadPFChargedHadrCand()->trackRef()->vz();
      track_pt1 = tau2->leadPFChargedHadrCand()->trackRef()->pt();
      track_eta1 = tau2->leadPFChargedHadrCand()->trackRef()->eta();
      track_phi1 = tau2->leadPFChargedHadrCand()->trackRef()->phi();
      track_chi1 = tau2->leadPFChargedHadrCand()->trackRef()->normalizedChi2();
      track_nhit1 = tau2->leadPFChargedHadrCand()->trackRef()->hitPattern().numberOfValidTrackerHits();
      track_dz1 = tau2->leadPFChargedHadrCand()->trackRef()->dz(evtVertexPos);
      track_dxy1 = tau2->leadPFChargedHadrCand()->trackRef()->dxy(evtVertexPos);
    }
  
  
    if(match_tau1){

      reco::PFJetRef ass_jet2 = getJetRef(*bestMatch);

      result2 = ((*disc1)[bestMatch] > 0.5);
      pt2 = bestMatch->pt();
      eta2 = bestMatch->eta();
      phi2 = bestMatch->phi();
      
      jet_pt2 = ass_jet2->pt();
      jet_eta2 = ass_jet2->eta();
      jet_phi2 = ass_jet2->phi();

      mass2 = bestMatch->mass();
      ResultChIso2 = (*chIso1)[bestMatch];
      ResultNIso2 = (*nIso1)[bestMatch];
      ResultPUIso2 = (*PUIso1)[bestMatch];
      ResultChIso2New = (*chIso3)[bestMatch];
      ResultNIso2New = (*nIso3)[bestMatch];
      ResultPUIso2New = (*PUIso3)[bestMatch];
      ResultCmbIso2 = (*cmbIso1)[bestMatch];
      ncharged2 = bestMatch->signalPFChargedHadrCands().size();
      npizero2 = bestMatch->signalPiZeroCandidates().size();

      z2 = bestMatch->vertex().z();
    
      if(bestMatch->leadPFChargedHadrCand().isNonnull() && bestMatch->leadPFChargedHadrCand()->trackRef().isNonnull()){
	vz2 = bestMatch->leadPFChargedHadrCand()->trackRef()->vz();
	track_pt2 = bestMatch->leadPFChargedHadrCand()->trackRef()->pt();
	track_eta2 = bestMatch->leadPFChargedHadrCand()->trackRef()->eta();
	track_phi2 = bestMatch->leadPFChargedHadrCand()->trackRef()->phi();
	track_chi2 = bestMatch->leadPFChargedHadrCand()->trackRef()->normalizedChi2();
	track_nhit2 = bestMatch->leadPFChargedHadrCand()->trackRef()->hitPattern().numberOfValidTrackerHits();
	track_dz2 = bestMatch->leadPFChargedHadrCand()->trackRef()->dz(evtVertexPos);
	track_dxy2 = bestMatch->leadPFChargedHadrCand()->trackRef()->dxy(evtVertexPos);
      }
    }else{
      debugmode = true;
    }

    _eventNum_ = Int_t(evt.id().event());
    _nVx_  = Int_t(nVx);
    _nmuon_  = nmuon;
    _match_gen_ = Int_t(match_gen);
    _gen_dm_ = Int_t(gen_dm);
    _nvtx_close_ = Int_t(nvtx_close);
    _gen_dr_ = match_gen_dr;
    _gen_tau_z_ = gen_tau_z;
    _vtx_density_ = min_vtx_dz;
    
    if ( verticesH_->size() > 0 ){
      _vtx_z_ = evtVertexPos.Z();
      _vtx_isFake_ = verticesH_->front().isFake();
      _vtx_rho_ = evtVertexPos.rho();
      _vtx_ndof_ = verticesH_->front().ndof();
      _vtx_chi2_ = verticesH_->front().chi2();      
    }else{
      _vtx_z_ = -99;
      _vtx_isFake_ = -99;
      _vtx_rho_ = -99;
      _vtx_ndof_ = -99;
      _vtx_chi2_ = -99;
    }

    _tauvispt_ = match_gen_pt;
    _tauviseta_ = match_gen_eta;
    _pt_ = tau2->pt();
    _eta_  = tau2->eta();
    _phi_  = tau2->phi();
    _jet_pt_ = ass_jet->pt();
    _jet_eta_  = ass_jet->eta();
    _jet_phi_  = ass_jet->phi();
    _m_    = tau2->mass();
    _z_    = tau2->vertex().z();
    _chIso_ = (*chIso2)[tau2];
    _nIso_ = (*nIso2)[tau2];
    _puIso_ = (*PUIso2)[tau2];
    _cmbIso_ = (*cmbIso2)[tau2];
    _vz_ = Float_t(vz1);
    _match_ = Int_t(match_tau1);
    _dmf_ = Int_t((*disc2)[tau2] > 0.5);
    _ncharged_ = tau2->signalPFChargedHadrCands().size();
    _npizero_ = tau2->signalPiZeroCandidates().size(); 
    _track_pt_ = Float_t(track_pt1);
    _track_eta_ = Float_t(track_eta1);
    _track_phi_ = Float_t(track_phi1);
    _track_chi_ = Float_t(track_chi1);
    _track_dz_ = Float_t(track_dz1);
    _track_dxy_ = Float_t(track_dxy1);
    _track_nhit_ = Int_t(track_nhit1);

    _pt2_ = Float_t(pt2);
    _eta2_  = Float_t(eta2);
    _phi2_  = Float_t(phi2);
    _m2_    = Float_t(mass2);
    _z2_    = Float_t(z2);
    _chIso2_= Float_t(ResultChIso2);
    _nIso2_ = Float_t(ResultNIso2);
    _puIso2_= Float_t(ResultPUIso2);
    _chIsoNew_= Float_t(ResultChIso2New);
    _nIsoNew_ = Float_t(ResultNIso2New);
    _puIsoNew_= Float_t(ResultPUIso2New);
    _cmbIso2_=Float_t(ResultCmbIso2);
    _vz2_ = Float_t(vz2);
    _dmf2_ = Int_t(result2);
    _ncharged2_ = Int_t(ncharged2);
    _npizero2_ = Int_t(npizero2);
    _closest_jet_pt_ = bestMatchJet.pt();
    _closest_jet_eta_ = bestMatchJet.eta();
    _closest_jet_phi_ = bestMatchJet.phi();
    _closest_jet_dr_ = min_dr_jet;
    _track_pt2_ = Float_t(track_pt2);
    _track_eta2_ = Float_t(track_eta2);
    _track_phi2_ = Float_t(track_phi2);
    _track_chi2_ = Float_t(track_chi2);    
    _track_dz2_ = Float_t(track_dz2);
    _track_dxy2_ = Float_t(track_dxy2);
    _track_nhit2_ = Int_t(track_nhit2);
    _jet_pt2_ = Float_t(jet_pt2);
    _jet_eta2_  = Float_t(jet_eta2);
    _jet_phi2_  = Float_t(jet_phi2);

    isoTuple_->Fill();
  }
  

  if(debugmode==false) debug_counter += 1;


  if(debugmode==true || debug_counter <= 1){
    
    _evt_ = Int_t(evt.id().event());
    _matchingDistance_ = matchingDistance_;
    _success_ = !debugmode;
    
    d_vtx_x.clear();
    d_vtx_y.clear();
    d_vtx_z.clear();
    d_vtx_isfake.clear();
    d_vtx_ndof.clear();
    d_vtx_rho.clear();

    for (reco::VertexCollection::const_iterator vit=verticesH_->begin(); vit!=verticesH_->end(); vit++){
      d_vtx_x.push_back(vit->position().X());
      d_vtx_y.push_back(vit->position().Y());
      d_vtx_z.push_back(vit->position().Z());
      d_vtx_isfake.push_back(vit->isFake());
      d_vtx_ndof.push_back(vit->ndof());
      d_vtx_rho.push_back(vit->position().rho());
    }


    d_tau_pt.clear();
    d_tau_eta.clear();
    d_tau_phi.clear();
    d_tau_z.clear();
    d_tau_jet_pt.clear();
    d_tau_jet_eta.clear();
    d_tau_jet_phi.clear();
    d_tau_dmf.clear();
    d_tau_npizero.clear();
    d_tau_ncharged.clear();
    d_tau_ngamma.clear();
    
    d_tau_id.clear();
    d_tau_pf_id.clear();
    d_tau_pf_eta.clear();
    d_tau_pf_phi.clear();
    d_tau_pf_pt.clear();
    d_tau_pf_type.clear();
    d_tau_pf_dz.clear();
    d_tau_pf_dzmin.clear();

    d_tau_jet_pf_id.clear();
    d_tau_jet_pf_eta.clear();
    d_tau_jet_pf_phi.clear();
    d_tau_jet_pf_pt.clear();
    d_tau_jet_pf_type.clear();
    d_tau_jet_pf_dz.clear();
    d_tau_jet_pf_dzmin.clear();
    

    Int_t counter_tau = 0;

    for (size_t iTau = 0; iTau < taus2->size(); ++iTau) { // PFtau
      reco::PFTauRef tau(taus2, iTau);
      reco::PFJetRef ass_jet = getJetRef(*tau);


      bool match_gen = false;

      for(size_t i = 0; i < genTaus->size(); ++ i){
      
	const reco::GenJet & TauCand = (*genTaus)[i];
	reco::Particle::LorentzVector visibleP4 = ((*genTaus)[i]).p4();
      
	if(visibleP4.pt() < 5.0) continue;
	if(TMath::Abs(visibleP4.eta()) > 2.3) continue;

	const std::vector <const reco::GenParticle*> mRefs = TauCand.getGenConstituents();
	unsigned int decayMode = 0; // 0 = hadronic, 1=electron, 2=muon 

	for(size_t igTauD =0; igTauD < mRefs.size(); igTauD++) {
	  if(abs(mRefs[igTauD]->pdgId())==11) decayMode = 1;
	  if(abs(mRefs[igTauD]->pdgId())==13) decayMode = 2;
	}
      
	if(decayMode!=0) continue; 


	double dR_MC = deltaR(tau->p4(),((*genTaus)[i]).p4());


	if(dR_MC < matchingDistance_) match_gen = true;

      }

      if(match_gen==false) continue;
      if((*disc2)[tau] < 0.5) continue;


      d_tau_pt.push_back(tau->pt());
      d_tau_eta.push_back(tau->eta());
      d_tau_phi.push_back(tau->phi());

      d_tau_jet_pt.push_back(ass_jet->pt());
      d_tau_jet_eta.push_back(ass_jet->eta());
      d_tau_jet_phi.push_back(ass_jet->phi());

      std::vector <reco::PFCandidatePtr> jetConstituents = ass_jet->getPFConstituents();
      for ( std::vector <reco::PFCandidatePtr>::const_iterator jetConstituent = jetConstituents.begin();
	    jetConstituent != jetConstituents.end(); ++jetConstituent ) {
	
	d_tau_jet_pf_id.push_back(counter_tau);
	d_tau_jet_pf_eta.push_back((*jetConstituent)->eta());
	d_tau_jet_pf_phi.push_back((*jetConstituent)->phi());
	d_tau_jet_pf_pt.push_back((*jetConstituent)->pt());
	d_tau_jet_pf_type.push_back(getPFCandidateTypeID((*jetConstituent)->particleId()));
	
	if ((*jetConstituent)->trackRef().isNonnull() && (*jetConstituent)->trackRef().isAvailable()){
	  d_tau_jet_pf_dz.push_back((*jetConstituent)->trackRef()->dz(evtVertexPos)); 

	  Float_t min_vtx_dz = 1000;
	  Int_t vtxid = -99;
	  Int_t counter_vtx = 0;

	  for (reco::VertexCollection::const_iterator vit=verticesH_->begin(); vit!=verticesH_->end(); vit++){	    
	    reco::Vertex::Point _vtx_ = vit->position(); 
	    
	    Float_t _dz_ = TMath::Abs((*jetConstituent)->trackRef()->dz(_vtx_));
	    if(min_vtx_dz > _dz_){
	      min_vtx_dz = _dz_;
	      vtxid = counter_vtx;
	    }
	    counter_vtx += 1;
	  }
	  d_tau_jet_pf_dzmin.push_back(vtxid);


	}else{
	  d_tau_jet_pf_dz.push_back(-99);
	  d_tau_jet_pf_dzmin.push_back(-99);
	}

      }


      d_tau_z.push_back(tau->vertex().z());
      d_tau_dmf.push_back(Int_t((*disc2)[tau] > 0.5));
      d_tau_npizero.push_back(tau->signalPFChargedHadrCands().size());
      d_tau_ncharged.push_back(tau->signalPiZeroCandidates().size());
      d_tau_ngamma.push_back(tau->signalPFGammaCands().size());


      d_tau_id.push_back(counter_tau);


      const std::vector<reco::PFCandidatePtr> &pfCandidates = tau->signalPFCands();

      for ( std::vector<reco::PFCandidatePtr>::const_iterator pfCandidate = pfCandidates.begin();
	    pfCandidate != pfCandidates.end(); ++pfCandidate ) {
	
	d_tau_pf_id.push_back(counter_tau);
	d_tau_pf_eta.push_back((*pfCandidate)->eta());
	d_tau_pf_phi.push_back((*pfCandidate)->phi());
	d_tau_pf_pt.push_back((*pfCandidate)->pt());
	d_tau_pf_type.push_back(getPFCandidateTypeID((*pfCandidate)->particleId()));

	if ((*pfCandidate)->trackRef().isNonnull() && (*pfCandidate)->trackRef().isAvailable()){
	  d_tau_pf_dz.push_back((*pfCandidate)->trackRef()->dz(evtVertexPos)); 

	  Float_t min_vtx_dz = 1000;
	  Int_t vtxid = -99;
	  Int_t counter_vtx = 0;

	  for (reco::VertexCollection::const_iterator vit=verticesH_->begin(); vit!=verticesH_->end(); vit++){	    
	    reco::Vertex::Point _vtx_ = vit->position(); 
	    
	    Float_t _dz_ = TMath::Abs((*pfCandidate)->trackRef()->dz(_vtx_));
	    if(min_vtx_dz > _dz_){
	      min_vtx_dz = _dz_;
	      vtxid = counter_vtx;
	    }
	    counter_vtx += 1;
	  }
	  d_tau_pf_dzmin.push_back(vtxid);

	}else{
	  d_tau_pf_dz.push_back(-99);
	  d_tau_pf_dzmin.push_back(-99);
	}

      }

      counter_tau ++;
    }

  
    d_tauchs_pt.clear();
    d_tauchs_eta.clear();
    d_tauchs_phi.clear();
    d_tauchs_z.clear();
    d_tauchs_jet_pt.clear();
    d_tauchs_jet_eta.clear();
    d_tauchs_jet_phi.clear();
    d_tauchs_dmf.clear();
    d_tauchs_npizero.clear();
    d_tauchs_ncharged.clear();
    d_tauchs_ngamma.clear();
    


    for (size_t iTau = 0; iTau < taus1->size(); ++iTau) { // PFtau
      reco::PFTauRef tau(taus1, iTau);
      reco::PFJetRef ass_jet = getJetRef(*tau);

      d_tauchs_pt.push_back(tau->pt());
      d_tauchs_eta.push_back(tau->eta());
      d_tauchs_phi.push_back(tau->phi());

      d_tauchs_jet_pt.push_back(ass_jet->pt());
      d_tauchs_jet_eta.push_back(ass_jet->eta());
      d_tauchs_jet_phi.push_back(ass_jet->phi());

      d_tauchs_z.push_back(tau->vertex().z());
      d_tauchs_dmf.push_back(Int_t((*disc1)[tau] > 0.5));

      d_tauchs_npizero.push_back(tau->signalPFChargedHadrCands().size());
      d_tauchs_ncharged.push_back(tau->signalPiZeroCandidates().size());
      d_tauchs_ngamma.push_back(tau->signalPFGammaCands().size());
    }


    d_jet_pt.clear();
    d_jet_eta.clear();
    d_jet_phi.clear();


    for(size_t i = 0; i < ak5jet->size(); ++ i) {
      const reco::PFJet &jet = (*ak5jet)[i];
      d_jet_pt.push_back( jet.pt());
      d_jet_eta.push_back( jet.eta());
      d_jet_phi.push_back( jet.phi());
    }

    d_jetchs_pt.clear();
    d_jetchs_eta.clear();
    d_jetchs_phi.clear();
    d_jetchs_id.clear();
    d_jetchs_pf_id.clear();
    d_jetchs_pf_eta.clear();
    d_jetchs_pf_phi.clear();
    d_jetchs_pf_pt.clear();
    d_jetchs_pf_type.clear();
    d_jetchs_pf_dz.clear();
    d_jetchs_pf_dzmin.clear();

    Int_t counter_jet = 0;

    for(size_t i = 0; i < ak5jetCHS->size(); ++ i) {
      const reco::PFJet &jet = (*ak5jetCHS)[i];
      d_jetchs_pt.push_back( jet.pt());
      d_jetchs_eta.push_back( jet.eta());
      d_jetchs_phi.push_back( jet.phi());
      d_jetchs_id.push_back(counter_jet);

      // Yuta
      std::vector <reco::PFCandidatePtr> jetConstituents = jet.getPFConstituents();
      for ( std::vector <reco::PFCandidatePtr>::const_iterator jetConstituent = jetConstituents.begin();
	    jetConstituent != jetConstituents.end(); ++jetConstituent ) {
	
	d_jetchs_pf_id.push_back(counter_jet);
	d_jetchs_pf_eta.push_back((*jetConstituent)->eta());
	d_jetchs_pf_phi.push_back((*jetConstituent)->phi());
	d_jetchs_pf_pt.push_back((*jetConstituent)->pt());
	d_jetchs_pf_type.push_back(getPFCandidateTypeID((*jetConstituent)->particleId()));

	if ((*jetConstituent)->trackRef().isNonnull() && (*jetConstituent)->trackRef().isAvailable()){
	  d_jetchs_pf_dz.push_back((*jetConstituent)->trackRef()->dz(evtVertexPos)); 

	  Float_t min_vtx_dz = 1000;
	  Int_t vtxid = -99;
	  Int_t counter_vtx = 0;

	  for (reco::VertexCollection::const_iterator vit=verticesH_->begin(); vit!=verticesH_->end(); vit++){	    
	    reco::Vertex::Point _vtx_ = vit->position(); 
	    
	    Float_t _dz_ = TMath::Abs((*jetConstituent)->trackRef()->dz(_vtx_));
	    if(min_vtx_dz > _dz_){
	      min_vtx_dz = _dz_;
	      vtxid = counter_vtx;
	    }
	    counter_vtx += 1;
	  }
	  d_jetchs_pf_dzmin.push_back(vtxid);
	  

	}else{
	  d_jetchs_pf_dz.push_back(-99);
	  d_jetchs_pf_dzmin.push_back(-99);
	}

      }

      counter_jet ++;
    }
    


    d_gen_pt.clear();
    d_gen_eta.clear();
    d_gen_phi.clear();
    d_gen_mode.clear();
    d_gen_z.clear();

    for(size_t i = 0; i < genTaus->size(); ++ i){
      
      const reco::GenJet & TauCand = (*genTaus)[i];
      reco::Particle::LorentzVector visibleP4 = ((*genTaus)[i]).p4();
      
      if(visibleP4.pt() < 5.0) continue;
      if(TMath::Abs(visibleP4.eta()) > 2.3) continue;

      const std::vector <const reco::GenParticle*> mRefs = TauCand.getGenConstituents();
      unsigned int decayMode = 0; // 0 = hadronic, 1=electron, 2=muon 
      Float_t _tau_z_ = -99;

      for(size_t igTauD =0; igTauD < mRefs.size(); igTauD++) {
	if(abs(mRefs[igTauD]->pdgId())==11) decayMode = 1;
	if(abs(mRefs[igTauD]->pdgId())==13) decayMode = 2;
	_tau_z_ = mRefs[igTauD]->vertex().z();
      }
      
      if(decayMode!=0) continue; 

      d_gen_pt.push_back(visibleP4.pt());
      d_gen_eta.push_back(visibleP4.eta());
      d_gen_phi.push_back(visibleP4.phi());
      d_gen_mode.push_back(decaymodeid(genTauDecayMode(TauCand)));
      d_gen_z.push_back(_tau_z_);
    }



    debugTuple_->Fill();
  }



  _nak5jet_ = ak5jet->size();
  _nak5jetCHS_ = ak5jetCHS->size();
  _ntau_ = taus2->size();
  _ntauCHS_ = taus1->size();
  _ngentau_ = genTaus->size();
  eventTuple_->Fill();

  return true;
}

void RecoTauDifferenceAnalyzer::endJob() {

  TTree *savetree = isoTuple_->CloneTree();
  TTree *savetree2 = eventTuple_->CloneTree();
  TTree *savetree3 = debugTuple_->CloneTree();
  TFile* file = new TFile("ntuple.root","recreate");
  savetree->Write();
  savetree2->Write();
  savetree3->Write();
  file->Close();

  delete savetree;
  delete savetree2;
  delete savetree3;
  delete isoTuple_;
  delete eventTuple_;
  delete debugTuple_;

}


#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(RecoTauDifferenceAnalyzer);
