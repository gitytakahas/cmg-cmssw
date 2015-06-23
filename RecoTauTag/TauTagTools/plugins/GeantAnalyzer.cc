// system include files
#include <memory>
#include <algorithm>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "FWCore/Utilities/interface/InputTag.h"


// Gen-level stuff:
#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "SimDataFormats/GeneratorProducts/interface/HepMCProduct.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/Math/interface/LorentzVector.h"
#include "RecoTauTag/TauTagTools/interface/GeneratorTau.h"
#include "SimDataFormats/TrackingHit/interface/PSimHitContainer.h"
#include "SimDataFormats/TrackingHit/interface/PSimHit.h"
#include "SimDataFormats/CaloHit/interface/PCaloHitContainer.h"
#include "SimDataFormats/CaloHit/interface/PCaloHit.h"
#include "SimDataFormats/Track/interface/SimTrack.h"
#include "SimDataFormats/Track/interface/SimTrackContainer.h"
#include "SimDataFormats/Vertex/interface/SimVertex.h"
#include "SimDataFormats/Vertex/interface/SimVertexContainer.h"


////////////////////////////
// DETECTOR GEOMETRY HEADERS
#include "MagneticField/Engine/interface/MagneticField.h"
#include "MagneticField/Records/interface/IdealMagneticFieldRecord.h"
#include "Geometry/TrackerGeometryBuilder/interface/TrackerGeometry.h"
#include "Geometry/TrackerGeometryBuilder/interface/PixelGeomDetUnit.h"
#include "Geometry/TrackerGeometryBuilder/interface/PixelGeomDetType.h"
#include "Geometry/TrackerGeometryBuilder/interface/PixelTopologyBuilder.h"
#include "Geometry/Records/interface/TrackerDigiGeometryRecord.h"
#include "Geometry/TrackerGeometryBuilder/interface/RectangularPixelTopology.h"
#include "Geometry/CommonDetUnit/interface/GeomDetType.h"
#include "Geometry/CommonDetUnit/interface/GeomDetUnit.h"

#include "DataFormats/SiPixelDetId/interface/PXBDetId.h"
#include "DataFormats/SiPixelDetId/interface/PXFDetId.h"
#include "DataFormats/SiStripDetId/interface/TIBDetId.h"
#include "DataFormats/SiStripDetId/interface/TIDDetId.h"
#include "DataFormats/SiStripDetId/interface/TOBDetId.h"
#include "DataFormats/SiStripDetId/interface/TECDetId.h"
#include "DataFormats/EcalDetId/interface/EcalSubdetector.h"
#include "DataFormats/EcalDetId/interface/EBDetId.h"
#include "DataFormats/EcalDetId/interface/EEDetId.h"
#include "DataFormats/ParticleFlowReco/interface/PFRecHit.h"
#include "DataFormats/EcalRecHit/interface/EcalRecHitCollections.h"
#include "PhysicsTools/JetMCUtils/src/JetMCTag.cc"
#include "DataFormats/ParticleFlowReco/interface/PFCluster.h"
#include "DataFormats/TauReco/interface/PFTau.h"
#include "DataFormats/JetReco/interface/GenJetCollection.h"
#include "RecoTauTag/RecoTau/interface/RecoTauQualityCuts.h"
#include "RecoTauTag/RecoTau/interface/RecoTauVertexAssociator.h"
#include "DataFormats/TauReco/interface/PFTauFwd.h"
#include "DataFormats/TauReco/interface/PFTauDiscriminator.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"
#include "DataFormats/ParticleFlowReco/interface/PFBlockElement.h"
#include "DataFormats/ParticleFlowReco/interface/PFBlock.h"
#include "DataFormats/ParticleFlowReco/interface/PFBlockElementCluster.h"
#include "DataFormats/ParticleFlowReco/interface/PFBlockElementTrack.h"
#include "DataFormats/ParticleFlowReco/interface/PFDisplacedVertex.h"
#include "DataFormats/ParticleFlowReco/interface/PFDisplacedVertexCandidate.h"

#include "TFile.h"
#include "TTree.h"
#include "TProfile.h"
#include "TAxis.h"
#include "TH2F.h"
#include "TString.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "TLorentzVector.h"
#include <typeinfo>       // operator typeid



using namespace std;
using namespace edm;


#include <algorithm>

const std::vector<reco::PFCandidatePtr>& getPFGammas(const reco::PFTau& tau, bool signal = true) {
  if (signal)
    return tau.signalPFGammaCands();
  return tau.isolationPFGammaCands();
}


float returnChi2(const reco::PFTau& tau){

  // leading charged hadron PFCand in signal cone

  Float_t LeadingTracknormalizedChi2 = 0;

  const PFCandidatePtr& leadingPFCharged = tau.leadPFChargedHadrCand() ;
  if ( leadingPFCharged.isNonnull() ) {
    reco::TrackRef tref = leadingPFCharged -> trackRef();
    if ( tref.isNonnull() ) {
      LeadingTracknormalizedChi2 = (float)(tref -> normalizedChi2());
    }
  }

  return LeadingTracknormalizedChi2;
}

float returnEratio(const reco::PFTau& tau){

  std::vector<reco::PFCandidatePtr> constsignal = tau.signalPFCands();
  Float_t EcalEnInSignalPFCands = 0;
  Float_t HcalEnInSignalPFCands = 0;

  typedef std::vector <reco::PFCandidatePtr>::iterator constituents_iterator;
  for(constituents_iterator it=constsignal.begin(); it != constsignal.end(); ++it) {
    reco::PFCandidatePtr & icand = *it;
    EcalEnInSignalPFCands += icand -> ecalEnergy();
    HcalEnInSignalPFCands += icand -> hcalEnergy();
  }

  Float_t total = EcalEnInSignalPFCands + HcalEnInSignalPFCands;
  if(total==0) return -1;
  else return EcalEnInSignalPFCands/total;
}



/** Calculates pt-weighted abs(deltaX(tau, candidates)).

  mode: 0 = signal cone, 1 = strip, 2 = isolation
  var: 0 = deltaR, 1 = deltaEta, 2 = deltaPhi
*/
float pt_weighted_dx(const reco::PFTau& tau, int mode = 0, int var = 0) {
  
  float sum_pt = 0.;
  float sum_dx_pt = 0.;

  float signalrad = std::max(0.05, std::min(0.1, 3./tau.pt()));

  auto& cands = getPFGammas(tau, mode < 2);

  for (auto& cand : cands) {
    // only look at electrons/photons with pT > 0.5
    if (cand->pt() < 0.5)
      continue;

    float dr = reco::deltaR(*cand, tau);
    float pt = cand->pt();
    if (mode == 2 || (mode == 0 && dr < signalrad) || (mode == 1 && dr > signalrad)) {
      sum_pt += pt;
      if (var == 0)
        sum_dx_pt += pt * dr;
      else if (var == 1)
        sum_dx_pt += pt * std::abs(cand->eta() - tau.eta());
      else if (var == 2)
        sum_dx_pt += pt * std::abs(reco::deltaPhi(cand->phi(), tau.phi()));
    }
  }
 
  if (sum_pt > 0.)
    return sum_dx_pt/sum_pt;  
  return 0.;
}

float pt_weighted_dr_signal(const reco::PFTau& tau) {
  return pt_weighted_dx(tau, 0, 0);
}

float pt_weighted_deta_strip(const reco::PFTau& tau) {
  return pt_weighted_dx(tau, 1, 1);
}

float pt_weighted_dphi_strip(const reco::PFTau& tau) {
  return pt_weighted_dx(tau, 1, 2);
}

float pt_weighted_dr_iso(const reco::PFTau& tau) {
  return pt_weighted_dx(tau, 2, 0);
}

unsigned int n_photons_total(const reco::PFTau& tau) {
  unsigned int n_photons = 0;
  for (auto& cand : tau.signalPFGammaCands()) {
    if (cand->pt() > 0.5)
      ++n_photons;
  }
  for (auto& cand : tau.isolationPFGammaCands()) {
    if (cand->pt() > 0.5)
      ++n_photons;
  }
  return n_photons;
}



class GeantAnalyzer : public edm::EDAnalyzer {
public:

  explicit GeantAnalyzer(const edm::ParameterSet&);
  ~GeantAnalyzer();

  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

  typedef math::XYZTLorentzVector XYZTLorentzVector;
  typedef ROOT::Math::PositionVector3D<ROOT::Math::CylindricalEta3D<Double32_t> > REPPoint;

private:
  virtual void beginJob() ;
  virtual void analyze(const edm::Event&, const edm::EventSetup&);
  virtual void endJob() ;

  edm::InputTag src_;

  TFile* file;
  TTree* tree;

  float tau_Eratio;
  int tau_nphoton;	// number of PFPhotons in signal cone
  int tau_decaymode;
  float tau_leadingTrackChi2;	// norm. chi2 of the track of the leading charged hadron
					// of the PFTau
  float tau_weighted_deta_strip;
  float tau_weighted_dphi_strip;
  float tau_weighted_dr_signal;
  float tau_weighted_dr_isolation;
};


GeantAnalyzer::GeantAnalyzer(const edm::ParameterSet& iConfig)

{
  src_ = iConfig.getParameter<edm::InputTag>("src");

  file = new TFile("Myroot.root","recreate");
  tree = new TTree("tree","tree");

  tree->Branch("tau_Eratio",&tau_Eratio,"tau_Eratio/F");
  tree->Branch("tau_decaymode",&tau_decaymode,"tau_decaymode/I");
  tree->Branch("tau_nphoton",&tau_nphoton,"tau_nphoton/I");
  tree->Branch("tau_leadingTrackChi2",&tau_leadingTrackChi2,"tau_leadingTrackChi2/F");
  tree->Branch("tau_weighted_deta_strip",&tau_weighted_deta_strip,"tau_weighted_deta_strip/F");
  tree->Branch("tau_weighted_dphi_strip",&tau_weighted_dphi_strip,"tau_weighted_dphi_strip/F");
  tree->Branch("tau_weighted_dr_signal",&tau_weighted_dr_signal,"tau_weighted_dr_signal/F");
  tree->Branch("tau_weighted_dr_isolation",&tau_weighted_dr_isolation,"tau_weighted_dr_isolation/F");

}



GeantAnalyzer::~GeantAnalyzer(){
  file->Write();
  file->Close();
}



// ------------ method called for each event  ------------
void
GeantAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{


  using namespace edm;
  using namespace reco;


  edm::Handle<reco::PFTauCollection> taus;
  iEvent.getByLabel(src_, taus);

  for (size_t iTau = 0; iTau < taus->size(); ++iTau) {
    reco::PFTauRef tau(taus, iTau);

    if(tau->pt() < 20) continue;
    if(TMath::Abs(tau->eta()) > 2.3) continue;


    tau_leadingTrackChi2 = returnChi2(*tau);
    tau_Eratio = returnEratio(*tau);
    tau_weighted_deta_strip = pt_weighted_deta_strip(*tau);
    tau_weighted_dphi_strip = pt_weighted_dphi_strip(*tau);
    tau_weighted_dr_signal = pt_weighted_dr_signal(*tau);
    tau_weighted_dr_isolation = pt_weighted_dr_iso(*tau);
    tau_nphoton = n_photons_total(*tau);
    tau_decaymode = tau->decayMode();

    tree->Fill();
  }
}





void 
GeantAnalyzer::beginJob(){
}

void 
GeantAnalyzer::endJob(){
}

void
GeantAnalyzer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

DEFINE_FWK_MODULE(GeantAnalyzer);
