// -*- C++ -*-
//
// Package:    GeantAnalyzer
// Class:      GeantAnalyzer
// 
/**\class GeantAnalyzer GeantAnalyzer.cc SLHCUpgradeSimulations/GeantAnalyzer/src/GeantAnalyzer.cc

   Description: [one line class summary]

   Implementation:
   [Notes on implementation]
*/
//
// Original Author:  Emmanuelle Perez,40 1-A28,+41227671915,
//         Created:  Thu Nov 14 11:22:13 CET 2013
// $Id$
//
//


// system include files
#include <memory>

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


void traceParent(std::vector<int> trackid, 
		 std::vector<int> gen, 
		 std::vector<int> parent,
		 std::vector<int> pdg,
		 int original,
		 int& _gen_){

  //  std::cout << "enter traceParent" << original << " " << std::endl;

  for(int is=0; is < (int)trackid.size(); is++){

    //    std::cout << "\t original = " << original << ", track id = " << trackid.at(is) << ", gen id = " << gen.at(is) << std::endl;
    if(original==trackid.at(is)){

      //      std::cout << "Internal : " << is << " track ID = " << trackid.at(is) << ", gen. pdgId = " << gen.at(is) << ", parent ID = " << parent.at(is) << std::endl;

      if(gen.at(is) != -1){
	//	std::cout << "found genparticle = " << gen.at(is) << ", pdg = " << pdg.at(is)  << std::endl;
	_gen_ = pdg.at(is);

      }else{
	int next = parent.at(is);
	traceParent(trackid, gen, parent, pdg, next, _gen_);
      }
    }
  }
}


void traceTrack(std::vector<int> trackid, 
		std::vector<int> gen, 
		std::vector<int> parent,
		std::vector<int> pdg,
		int original,
		int& _track_){
  
  
  for(int is=0; is < (int)trackid.size(); is++){
    if(original==trackid.at(is)){
      if(gen.at(is) != -1){
	_track_ = trackid.at(is);
      }else{
	int next = parent.at(is);
	traceTrack(trackid, gen, parent, pdg, next, _track_);
      }
    }
  }
}



Int_t decaymode_id(std::string str){
  if(str=="electron") return -2;
  else if(str=="muon") return -1;
  else if(str=="oneProng0Pi0") return 0;
  else if(str=="oneProng1Pi0") return 1;
  else if(str=="oneProng2Pi0") return 2;
  else if(str=="oneProng3Pi0") return 3;
  else if(str=="oneProngOther") return 4;  
  else if(str=="threeProng0Pi0") return 10;
  else if(str=="threeProng1Pi0") return 11;
  else if(str=="threeProngOther") return 14;
  else if(str=="rare") return 15;
  else return -9;
}

using namespace std;
using namespace edm;



//
// class declaration
//

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

  void PrintSimHits(edm::Handle<edm::PSimHitContainer> simHitslowHandle, TString detector="") ;
  void PrintCaloHits(edm::Handle<edm::PCaloHitContainer> simHitslowHandle, float threshold=0.) ;
  void FillTheMainMapForDetIds() ;

  // template, such that it can be used for EcalRecHits as well
  template<typename T> void PrintPFRecHits(edm::Handle< T > pfRecHitsHandle, float threshold = 0., bool physonly=false) ;

  // that's needed because PFRecHit and EcalRecHit don't have the same
  // method name to retrieve the detId !
  unsigned int GetDetId(vector<reco::PFRecHit>::const_iterator  rh) { return rh -> detId() ; }
  unsigned int GetDetId(EcalRecHitCollection::const_iterator rh) { return rh -> id() ; }

  void PrintPFClusters(  edm::Handle< vector<reco::PFCluster> > pPFClustersECALHandle  , int verbose = 0) ;
  //  void PrintPFTaus(edm::Handle< vector<reco::PFTau> > pPFTausHandle ) ;
  void PrintPFTaus(reco::PFTauRef PFTau, const edm::Event& iEvent, Int_t counter, Int_t dm, Float_t pt, Float_t eta, Float_t energy) ;

  void EnergyLossAlongTrack(const SimTrack* itrack,
			    edm::Handle<edm::SimTrackContainer>   simTrackHandle,
			    edm::Handle<edm::SimVertexContainer>  simVtxHandle ,
			    vector<float>& VectorOfMomenta ,
			    TString offset="" );


  map<unsigned int, unsigned int> PCaloHitMap;   // ( detId, SimTrackId )
  map<unsigned int, map<unsigned int, float> > PCaloHitEnergyMap;  //  ( detId, ( SimTrackId, energy) )

  // to keep trace of the SimTrackId that gives the largest deposit in detid.
  map<unsigned int, int > TrackIdMap;	//  (simTrackId, pdgId )
  map<unsigned int, float> RecHitMap;	// ( detId, energy of RecHit)
  map<float, unsigned int> ClusterMap;   // ( energy of cluster, SimTrackId)
  vector<int> PrimariesSimTrackId;   // vector of SimTrackId of primary particles. Includes photons from the decay of primary Pi0's
  vector<int> SecondariesSimTrackId;
  vector<int> SecondariesSimTrackR;
  vector<int> SecondariesSimTrackpt;
  vector<int> SecondariesGenParticles;
  vector<int> SecondariesParents;
  vector<int> SecondariesPdgId;
  map<unsigned int, vector<unsigned int> > SimTrackHistory;  // (simTrackId, vector or processIds) for the history of the track
  map<unsigned int, vector<int> > SimTrackPdgIdHistory;  // (simTrackId, vector or processIds) for the history of the track
  map<unsigned int, vector<float> > SimTrackRHistory;  // (simTrackId, vector or processIds) for the history of the track

  map<unsigned int, vector<int> > SimTrackVertexHistory;  // (simTrackId, vector or simVtxIds) for the history of the track
  map<unsigned int, unsigned int> TrackIdMapIndexInHandle;   // (simTrackId, index in simTrackHandle)
  map<unsigned int, vector<float> > SimTrackMomentaHistory;   // ( simTrackId, vector of Ptrack along the track)


  bool doPrintSimHits;
  bool doPrintCaloHits;
  bool doPrintRecHits;

  edm::InputTag src_;
  edm::InputTag genTauSrc_;
  edm::InputTag disc_;
  edm::InputTag nIso_;

  Int_t counter = -1;

  edm::Service<TFileService> fs_;
  TH2F* history;

  TFile* file;
  TTree* tree;

  // tau by tau variables
  Int_t evtnum;
  Int_t evtcounter;
  Float_t gamma_total_iso;
  Float_t tau_pt;
  Float_t tau_eta;
  Float_t tau_phi;
  Float_t tau_gen_pt;
  Float_t tau_gen_eta;
  Float_t tau_gen_energy;
  Int_t tau_dm;
  Int_t gen_dm;
  Int_t tau_dm_rough;
  Int_t gen_dm_rough;

  float EcalEnInSignalPFCands; 	// total ECAL energy carried by the PFCandidates in signal cone
  float HcalEnInSignalPFCands;	// idem for HCAL
  int nPFPhotonsInSignal;	// number of PFPhotons in signal cone
  int nPFDisplacedVertex ;	// number of PFDisplacedVertices
  float LeadingTracknormalizedChi2;	// norm. chi2 of the track of the leading charged hadron
					// of the PFTau

  // photon by photon variables
  Int_t ncluster;
  Int_t nbadcluster;
  Float_t gamma_pt;
  Float_t gamma_eta;
  Float_t gamma_phi;
  Int_t gamma_global_counter;
  Int_t gamma_photon_counter;
  
  // cluster by cluster variables
  std::vector<int> seed_pdgid;
  std::vector<int> pseed_pdgid;
  std::vector<float> pseed_pt;
  std::vector<float> pseed_R;
  std::vector<int> isPrimary;
  std::vector<int> cluster_id;
  std::vector<int> nprocess;

  std::vector<int> history_pdgid;
  std::vector<float> history_pt;
  std::vector<float> history_r;
  std::vector<int> history_ii_global;
  std::vector<int> history_ii_photon;
  std::vector<int> history_processtype;

  Int_t global_counter;
  Int_t photon_counter;

};


class MyEcalRecHit: public EcalRecHit 
{
public:
  unsigned detId() const {return id() ;}
};

// constructors and destructor
GeantAnalyzer::GeantAnalyzer(const edm::ParameterSet& iConfig)

{
  //now do what ever initialization is needed

  src_ = iConfig.getParameter<edm::InputTag>("src");
  genTauSrc_ = iConfig.getParameter<edm::InputTag>("genTauSrc");
  disc_ = iConfig.getParameter<edm::InputTag>("disc");
  nIso_ = iConfig.getParameter<edm::InputTag>("nIso");

  //doPrintSimHits = true;
  //doPrintCaloHits = true;
  //doPrintRecHits = true;
  
  doPrintSimHits = false;
  doPrintCaloHits = false;
  doPrintRecHits = false;

  file = new TFile("Myroot.root","recreate");
  tree = new TTree("tree","tree");

  // tau by tau
  tree->Branch("evtnum",&evtnum,"evtnum/I");
  tree->Branch("evtcounter",&evtcounter,"evtcounter/I");
  tree->Branch("ncluster",&ncluster,"ncluster/I");
  tree->Branch("nbadcluster",&nbadcluster,"nbadcluster/I");
  tree->Branch("gamma_total_iso",&gamma_total_iso,"gamma_total_iso/F");

  tree->Branch("tau_pt",&tau_pt,"tau_pt/F");
  tree->Branch("tau_eta",&tau_eta,"tau_eta/F");
  tree->Branch("tau_phi",&tau_phi,"tau_phi/F");
  tree->Branch("tau_gen_pt",&tau_gen_pt,"tau_gen_pt/F");
  tree->Branch("tau_gen_eta",&tau_gen_eta,"tau_gen_eta/F");
  tree->Branch("tau_gen_energy",&tau_gen_energy,"tau_gen_energy/F");

  tree->Branch("tau_dm",&tau_dm,"tau_dm/I");
  tree->Branch("gen_dm",&gen_dm,"gen_dm/I");
  tree->Branch("tau_dm_rough",&tau_dm_rough,"tau_dm_rough/I");
  tree->Branch("gen_dm_rough",&gen_dm_rough,"gen_dm_rough/I");

  tree->Branch("EcalEnInSignalPFCands",&EcalEnInSignalPFCands,"EcalEnInSignalPFCands/F");
  tree->Branch("HcalEnInSignalPFCands",&HcalEnInSignalPFCands,"HcalEnInSignalPFCands/F");
  tree->Branch("nPFPhotonsInSignal",&nPFPhotonsInSignal,"nPFPhotonsInSignal/I");
  tree->Branch("nPFDisplacedVertex",&nPFDisplacedVertex,"nPFDisplacedVertex/I");
  tree->Branch("LeadingTracknormalizedChi2",&LeadingTracknormalizedChi2,"LeadingTracknormalizedChi2/F");


  // photon by photon
  tree->Branch("gamma_global_counter",&gamma_global_counter,"gamma_global_counter/I");
  tree->Branch("gamma_photon_counter",&gamma_photon_counter,"gamma_photon_counter/I");
  tree->Branch("gamma_pt",&gamma_pt,"gamma_pt/F");
  tree->Branch("gamma_eta",&gamma_eta,"gamma_eta/F");
  tree->Branch("gamma_phi",&gamma_phi,"gamma_phi/F");

  // cluster by cluster variables
  tree->Branch("cluster_id",&cluster_id);
  tree->Branch("seed_pdgid",&seed_pdgid);
  tree->Branch("pseed_pdgid",&pseed_pdgid);
  tree->Branch("pseed_pt",&pseed_pt);
  tree->Branch("pseed_R",&pseed_R);
  tree->Branch("isPrimary",&isPrimary);
  tree->Branch("nprocess",&nprocess);

  tree->Branch("history_pdgid",&history_pdgid);
  tree->Branch("history_pt",&history_pt);
  tree->Branch("history_r",&history_r);
  tree->Branch("history_ii_global",&history_ii_global);
  tree->Branch("history_ii_photon",&history_ii_photon);
  tree->Branch("history_processtype",&history_processtype);

  global_counter = 0;
  photon_counter = 0;

}


GeantAnalyzer::~GeantAnalyzer(){
  file->Write();
  file->Close();
}



// ------------ method called for each event  ------------
void
GeantAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{

  counter+=1;

  using namespace edm;
  using namespace reco;

  edm::Handle<reco::PFTauCollection> taus;
  iEvent.getByLabel(src_, taus);

  edm::Handle<std::vector<reco::GenJet> > genTaus;
  iEvent.getByLabel(genTauSrc_, genTaus);

  edm::Handle<reco::PFTauDiscriminator> disc;
  iEvent.getByLabel(disc_, disc);

  edm::Handle<reco::PFTauDiscriminator> nIso;
  iEvent.getByLabel(nIso_,nIso);


  /*
   * First, look into tau collection and select events 
   * in case there is a tau with isolated photons around it
   */

  int ispass = 0;

  reco::PFTauRef _tau_;
  Int_t gendm = -1;
  Float_t gen_pt = -1;
  Float_t gen_eta = -1;
  Float_t gen_energy = -1;

  EcalEnInSignalPFCands = -1. ;
  HcalEnInSignalPFCands = -1.;
  nPFDisplacedVertex = -1 ;
  nPFPhotonsInSignal = -1;
  LeadingTracknormalizedChi2 = -1;
  
  for (size_t iTau = 0; iTau < taus->size(); ++iTau) { // PFtau

    reco::PFTauRef tau(taus, iTau);

    bool match_gen = false;

    if(!(tau->decayMode() == 0 ||
	 tau->decayMode() == 1 || 
	 tau->decayMode() == 2 || 
	 tau->decayMode() == 10)){
      std::cout << "Gen. info not available !" << std::endl;
      continue;
    }


    for(size_t i = 0; i < genTaus->size(); ++ i){      

      const reco::GenJet & TauCand = (*genTaus)[i];
      reco::Particle::LorentzVector visibleP4 = ((*genTaus)[i]).p4();
      
      //      if(visibleP4.pt() < 20) continue;
      //      if(TMath::Abs(visibleP4.eta()) > 2.3) continue;

      const std::vector <const reco::GenParticle*> mRefs = TauCand.getGenConstituents();
      unsigned int decayMode = 0; // 0 = hadronic, 1=electron, 2=muon 

      for(size_t igTauD =0; igTauD < mRefs.size(); igTauD++) {
	if(abs(mRefs[igTauD]->pdgId())==11) decayMode = 1;
	if(abs(mRefs[igTauD]->pdgId())==13) decayMode = 2;
      }
      
      if(decayMode!=0) continue; 


      double dR_MC = deltaR(tau->p4(), ((*genTaus)[i]).p4());
      int id = decaymode_id(genTauDecayMode(TauCand));

      if(!(id==0 ||  id==1 ||  id==2 ||  id==10)) continue;
	 
      if(dR_MC < 0.5){
	match_gen = true;
	gendm = id;

	gen_pt = visibleP4.pt();
	gen_eta = visibleP4.eta();
	gen_energy = visibleP4.energy();

	//	match_gen_pt = visibleP4.pt();
	//	match_gen_eta = visibleP4.eta();
	//	std::cout << "\t" << i << " -- Matching between gen and reco. tau : dR = " << dR_MC << " / 0.5 : " << std::endl;
	//	std::cout << "\t" << i << " -- vis pT, eta, decaymode = " << match_gen_pt << " " << match_gen_eta << " " << genTauDecayMode(TauCand) << " " << gendm<< std::endl;

      }
    }

    if(match_gen==false) continue;


    float niso = (*nIso)[tau];

    //    std::cout << "# of photon = " << tau->isolationPFGammaCands().size() 
    //	      << "# of pion = " << tau->isolationPFChargedHadrCands().size()
    //	      << " nIso = " << niso << " " << ((*disc)[tau] < 0.5) << std::endl;

    //    if(tau->isolationPFGammaCands().size() ==0 ) continue;
    if(niso==0) continue;

    ispass += 1;

    _tau_ = tau;

  }

  if(ispass!=1) return;
  

  edm::Handle< vector<reco::GenParticle> > GenParticleHandle;
  iEvent.getByLabel("genParticles","",GenParticleHandle);
  if (! GenParticleHandle.isValid() ) return;
 

  edm::Handle<edm::SimTrackContainer>   simTrackHandle;
  edm::Handle<edm::SimVertexContainer>  simVtxHandle;
  iEvent.getByLabel( "g4SimHits", simTrackHandle );
  iEvent.getByLabel( "g4SimHits", simVtxHandle );


  std::cout << " Loop over simtracks " << std::endl;

  TrackIdMap.clear();
  PrimariesSimTrackId.clear();
  SecondariesSimTrackId.clear();
  SecondariesGenParticles.clear();
  SecondariesParents.clear();
  SecondariesPdgId.clear();
  SecondariesSimTrackR.clear();
  SecondariesSimTrackpt.clear();
  SimTrackHistory.clear();
  SimTrackPdgIdHistory.clear();
  SimTrackRHistory.clear();
  SimTrackVertexHistory.clear();
  TrackIdMapIndexInHandle.clear();
  SimTrackMomentaHistory.clear();

  unsigned int index_in_Handle = -1;
  SimTrackContainer::const_iterator iterSimTracks;
  for ( iterSimTracks = simTrackHandle->begin();
        iterSimTracks != simTrackHandle->end();
        ++iterSimTracks ) {

    index_in_Handle ++;
    int genpartIndex = iterSimTracks->genpartIndex();
    int vertexIndex = iterSimTracks->vertIndex();
    const SimVertex& theSimVertex = (*simVtxHandle)[vertexIndex];
    unsigned int vertexId = theSimVertex.vertexId();
    int parentIndex = theSimVertex.parentIndex();

    unsigned int trackId = iterSimTracks -> trackId();
    TrackIdMap.insert( pair<unsigned int, int>(trackId, iterSimTracks->type()  ) ) ;
    TrackIdMapIndexInHandle.insert( pair<unsigned int, unsigned int>(trackId, index_in_Handle) ) ;

    const math::XYZVectorD tksurfPos = iterSimTracks -> trackerSurfacePosition() ;
    const math::XYZTLorentzVectorD tksurfMom =  iterSimTracks -> trackerSurfaceMomentum() ;
    float rdist = sqrt( pow( tksurfPos.x(), 2) + pow( tksurfPos.y(), 2) );
    float zdist = tksurfPos.z();
    const math::XYZTLorentzVectorD& Vtx_position =theSimVertex.position();
    unsigned int processType = theSimVertex.processType();
    float vtxR = sqrt( pow( Vtx_position.x(), 2) + pow(Vtx_position.y(), 2) ) ;

    cout << "SimTrack trackId " << trackId << " type " << iterSimTracks->type() << " processType " << processType << " genpartIndex  " << genpartIndex << " vertexId " << vertexId << " parentIndex " << parentIndex << " R " << rdist  <<  " Z " << zdist << " pxyz " << tksurfMom.px() << " " << tksurfMom.py() << " " << tksurfMom.pz() <<  " vertexR " << vtxR << endl;

    if ( genpartIndex != -1 ) PrimariesSimTrackId.push_back( trackId );

    vector<unsigned int> p0;
    p0.push_back( processType );
    SimTrackHistory.insert( pair<unsigned int, vector<unsigned int> >(trackId, p0) ) ;

    vector<int> p1;
    p1.push_back( iterSimTracks->type() );
    SimTrackPdgIdHistory.insert( pair<unsigned int, vector<int> >(trackId, p1) ) ;

    vector<float> p2;
    p2.push_back( rdist );
    SimTrackRHistory.insert( pair<unsigned int, vector<float> >(trackId, p2) ) ;

    vector<int> q0;
    q0.push_back( vertexIndex );
    SimTrackVertexHistory.insert( pair<unsigned int, vector<int> >(trackId, q0 ) ) ;

    // update the history of the parent track
    map< unsigned int, vector<unsigned int> >::iterator phis = SimTrackHistory.find( (unsigned int)parentIndex );
    map< unsigned int, vector<int> >::iterator phisPdg = SimTrackPdgIdHistory.find( (unsigned int)parentIndex );
    map< unsigned int, vector<float> >::iterator phisR = SimTrackRHistory.find( (unsigned int)parentIndex );
    map< unsigned int, vector<int> >::iterator phisVtx = SimTrackVertexHistory.find( (unsigned int)parentIndex );
    if ( phis != SimTrackHistory.end() ) {
      vector<unsigned int> vtmp = phis -> second;
      vtmp.push_back( processType  );
      SimTrackHistory[ trackId ] = vtmp;

      vector<int> xtmp = phisPdg -> second;
      xtmp.push_back( iterSimTracks->type()  );
      SimTrackPdgIdHistory[ trackId ] = xtmp;

      vector<float> rtmp = phisR -> second;
      rtmp.push_back( rdist  );
      SimTrackRHistory[ trackId ] = rtmp;

      vector<int> wtmp = phisVtx -> second;
      wtmp.push_back( vertexIndex );
      SimTrackVertexHistory[ trackId ] = wtmp ;
    }
    else {
      if (parentIndex != -1) cout << " ... problem in updating SimTrackHistory : trackId " << parentIndex << " (parent of " << trackId << ") has not been entered yet. " << endl;
    }


    SecondariesSimTrackId.push_back( trackId );
    SecondariesGenParticles.push_back(genpartIndex);
    SecondariesParents.push_back(parentIndex);
    SecondariesPdgId.push_back(iterSimTracks->type());
    SecondariesSimTrackR.push_back(rdist);
    SecondariesSimTrackpt.push_back(tksurfMom.pt());

  }  // end loop over simTracks


  // now, for the tracks that exit the tracker, look at the energy
  // lost at each vertex along the track, and fill the
  // map SimTrackMomentaHistory

  for ( iterSimTracks = simTrackHandle->begin();
        iterSimTracks != simTrackHandle->end();
        ++iterSimTracks ) {

    const math::XYZTLorentzVectorD tksurfMom =  iterSimTracks -> trackerSurfaceMomentum() ;
    //float p = sqrt( tksurfMom.perp2() );
    float p  = tksurfMom.P() ;
    unsigned int trackId = iterSimTracks -> trackId();
    if ( p <= 1e-3) continue;       // only tracks with p > 1 MeV when they exit the tracker

    const SimTrack itra = *iterSimTracks;
    const SimTrack* pitra = &itra;
    vector<float> vecP ;
    EnergyLossAlongTrack( pitra, simTrackHandle, simVtxHandle, vecP );
    /*
      if ( vecP.size() > 0) {
      for (unsigned int k=0; k < vecP.size(); k++) {
      float thep = vecP.at( k );
      cout << " " << thep << " "  ;
      }
      cout << endl;
      }
    */
    SimTrackMomentaHistory.insert( pair<unsigned int, vector<float> >(trackId, vecP ) );

  }   // end loop over SimTracks



  if (doPrintSimHits) {

    // GET SIMHITS  //
    edm::Handle<edm::PSimHitContainer> simHitslowHandle;
    iEvent.getByLabel( "g4SimHits","TrackerHitsPixelBarrelLowTof",simHitslowHandle);
    cout << " Loop over SimHits in BarrelPixel (LOW) " << endl;
    PrintSimHits(simHitslowHandle,"BPIX");

    edm::Handle<edm::PSimHitContainer> simHitsEndcapHandle;
    iEvent.getByLabel( "g4SimHits","TrackerHitsPixelEndcapHighTof",simHitsEndcapHandle);
    cout << " Loop over SimHits in EndcapPixel " << endl;
    PrintSimHits(simHitsEndcapHandle,"FPIX");

    edm::Handle<edm::PSimHitContainer> simHitsTIBHandle;
    iEvent.getByLabel( "g4SimHits","TrackerHitsTIBLowTof",simHitsTIBHandle);
    cout << " Loop over SimHits in TIB " << endl;
    PrintSimHits(simHitsTIBHandle,"TIB");

    edm::Handle<edm::PSimHitContainer> simHitsTOBHandle;
    iEvent.getByLabel( "g4SimHits","TrackerHitsTOBLowTof",simHitsTOBHandle);
    cout << " Loop over SimHits in TOB " << endl;
    PrintSimHits(simHitsTOBHandle,"TOB");

    edm::Handle<edm::PSimHitContainer> simHitsTIDHandle;
    iEvent.getByLabel( "g4SimHits","TrackerHitsTIDLowTof",simHitsTIDHandle);
    cout << " Loop over SimHits in  TID " << endl;
    PrintSimHits(simHitsTIDHandle,"TID");

    edm::Handle<edm::PSimHitContainer> simHitsTECHandle;
    iEvent.getByLabel( "g4SimHits","TrackerHitsTECLowTof",simHitsTECHandle);
    cout << " Loop over SimHits in TEC " << endl;
    PrintSimHits(simHitsTECHandle,"TEC");
  }


  // PCaloHits

  PCaloHitMap.clear();	// these two maps will be filled in PrintCaloHits and in FillTheMainMapForDetIds below
  PCaloHitEnergyMap.clear();

  edm::Handle<edm::PCaloHitContainer> simHitsEcalHandle;
  iEvent.getByLabel( "g4SimHits","EcalHitsEB",simHitsEcalHandle);
  cout << " Loop over SimHits in ECAL EB" << endl;
  float threshold = 0. ;
  PrintCaloHits(simHitsEcalHandle,threshold);

  edm::Handle<edm::PCaloHitContainer> simHitsEcalEEHandle;
  iEvent.getByLabel( "g4SimHits","EcalHitsEE",simHitsEcalEEHandle);
  cout << " Loop over SimHits in ECAL EE" << endl;
  PrintCaloHits(simHitsEcalEEHandle,threshold);

  FillTheMainMapForDetIds() ;		


  // now the RecHits

  RecHitMap.clear();	// the map is filled in PrintPFRecHits below
  threshold = 0.1;
  cout << endl << " Loop over particleFlowRecHitECAL " << endl;
  edm::Handle< vector<reco::PFRecHit> > pfRecHitsHandle;
  iEvent.getByLabel( "particleFlowRecHitECAL","",pfRecHitsHandle);
  PrintPFRecHits<vector<reco::PFRecHit> >( pfRecHitsHandle , 0.1, false);   // all PFRecHits above a threshold


  // now the clusters 

  ClusterMap.clear();

  int verbose = 0;
  edm::Handle< vector<reco::PFCluster> > pPFClustersECALHandle;
  cout << endl << " Loop over particleFlowClusterECAL " << endl ;
  iEvent.getByLabel("particleFlowClusterECAL","",pPFClustersECALHandle);
  PrintPFClusters( pPFClustersECALHandle, verbose );



 // look for PFDisplaced vertices
       edm::Handle<vector<PFDisplacedVertex> > PFDisplacedVertexHandle;
   iEvent.getByLabel( "particleFlowDisplacedVertex","",PFDisplacedVertexHandle);
   nPFDisplacedVertex = PFDisplacedVertexHandle->size();
/*
 *    // one could demand that the vertex be in the direction of the tau, e.g. :
   for (unsigned int ivtx = 0; ivtx < PFDisplacedVertexHandle->size(); ++ivtx) {
      PFDisplacedVertexRef vtx( PFDisplacedVertexHandle, ivtx) ;
      const math::XYZVector primaryDirection = vtx -> primaryDirection() ;
      float eta = primaryDirection.eta();
      float phi = primaryDirection.phi();
   }
*/


  // access the PFTau objects
  cout <<  endl << " Loop over the PFTau objects " << endl;
  PrintPFTaus( _tau_ , iEvent, counter, gendm, gen_pt, gen_eta, gen_energy);


}


// --------------------------------------------------------------------------------------

// this fills the vector VectorOfMomenta, that contains the PT of the SimTrack
// after each interaction (vertex)
// Used to fill the map SimTrackMomentaHistory

void GeantAnalyzer::EnergyLossAlongTrack(const SimTrack* itrack,
					 edm::Handle<edm::SimTrackContainer>   simTrackHandle,
					 edm::Handle<edm::SimVertexContainer>  simVtxHandle ,
					 std::vector<float>& VectorOfMomenta ,
					 TString offset )
{


  const math::XYZTLorentzVectorD mom = itrack -> momentum();
  //float p = mom.P()  ;
  float p = mom.Pt()  ;
  VectorOfMomenta.insert( VectorOfMomenta.begin(), p );

  unsigned int trackId = itrack -> trackId();
  //cout << offset << " ... enter in EnergyLossAlongTrack  trackId = " << trackId << " momentum p = " << p << endl;

  map< unsigned int, vector<int> >::iterator phisVtx = SimTrackVertexHistory.find( trackId );
  if ( phisVtx != SimTrackVertexHistory.end() ) {
    vector<int> vertices = phisVtx -> second;

    int lastvertex = vertices.back();
    const SimVertex& theSimVertex = (*simVtxHandle)[ lastvertex ];
    int parentIndex = theSimVertex.parentIndex();   // careful, this is the simTrackId
    unsigned int vertexId = theSimVertex.vertexId();

    if ( parentIndex != -1 && vertexId != 0) {
      // need to get the index of this simTrackId in the simTrackHandle :
      int parentTrack = TrackIdMapIndexInHandle[ (unsigned int)parentIndex ];
      const SimTrack theParentTrack = (*simTrackHandle)[ parentTrack ];
      const SimTrack* pitra = &theParentTrack;
      TString offset2 = offset + "   ";
      EnergyLossAlongTrack( pitra, simTrackHandle, simVtxHandle, VectorOfMomenta, offset2 );
    } // endif

  } // endif phisVtx

}


// --------------------------------------------------------------------------------------
//#  reco::PFTauRef _tau_;
void GeantAnalyzer::PrintPFTaus(reco::PFTauRef iterTau, const edm::Event& iEvent, Int_t counter, Int_t gendm, Float_t _genpt, Float_t _geneta, Float_t _gen_e) {

  photon_counter = 0;

  using namespace reco;
  typedef std::vector <reco::PFCandidatePtr>::iterator constituents_iterator;

  float pT = iterTau -> pt();
  float eta = iterTau -> eta();
  float phi = iterTau -> phi();
  float isolationCh = iterTau -> isolationPFChargedHadrCandsPtSum();
  float isolationGamma =  iterTau -> isolationPFGammaCandsEtSum() ;

  cout << " a PFTau pt " << pT << " eta " << eta << " phi " << phi << " isolationCh " << isolationCh << " isolationGamma " << isolationGamma << endl;

  EcalEnInSignalPFCands = 0;
  HcalEnInSignalPFCands = 0;
  nPFPhotonsInSignal = 0;

        // access the PFCandidates that are in the signal cone
   std::vector<reco::PFCandidatePtr> constsignal = iterTau -> signalPFCands();
   for(constituents_iterator it=constsignal.begin(); it != constsignal.end(); ++it) {
         reco::PFCandidatePtr & icand = *it;
         int pftype = icand->particleId() ;
         if ( pftype == 4) nPFPhotonsInSignal ++;
         EcalEnInSignalPFCands += icand->ecalEnergy();
         HcalEnInSignalPFCands += icand -> hcalEnergy();
    }
        // leading charged hadron PFCand in signal cone
    const PFCandidatePtr& leadingPFCharged = iterTau -> leadPFChargedHadrCand() ;
    if ( leadingPFCharged.isNonnull() ) {
      reco::TrackRef tref = leadingPFCharged -> trackRef();
      if ( tref.isNonnull() ) {
        LeadingTracknormalizedChi2 = (float)(tref -> normalizedChi2());
        //LeadingTrackd0 = (float)(tref -> d0() );
        //LeadingTracknumberOfLostHits = (int)(tref -> numberOfLostHits() );
      }
    }


	// access the PFCandidates that are in the isolation cone:
  std::vector<reco::PFCandidatePtr> constisolation = iterTau -> isolationPFCands() ;

  for(constituents_iterator it=constisolation.begin(); it!=constisolation.end(); ++it) {
    reco::PFCandidatePtr & icand = *it;
    float candPt = icand->pt();
    float candE = icand -> energy();
    float candEta = icand->eta();
    float candPhi = icand -> phi();
    float candDr   = reco::deltaR(**it,*iterTau);
    int pftype = icand->particleId() ;   // should be 4 for photons, 5 for neut hadrons

    if ( pftype != PFCandidate::ParticleType::gamma) continue;
    TString stype =  pftype == PFCandidate::ParticleType::gamma ? " photon " : " NeutHad " ;
    cout << "   " << stype << " in isolation cone pt " << candPt << " energy " << candE << " eta " << candEta << " phi " << candPhi << " dR " << candDr << endl;


    int simTrackpdgId = -999;
    unsigned int simTrackId = 0;

    // Find the corresponding PF block elements
    const PFCandidate::ElementsInBlocks& theElements = icand -> elementsInBlocks();
    if( theElements.empty() ) continue;
    const reco::PFBlockRef blockRef = theElements[0].first;
    PFBlock::LinkData linkData = blockRef->linkData();
    const edm::OwnVector<reco::PFBlockElement>& elements = blockRef->elements();


    int _nEcal = 0;
    for(unsigned jEle=0; jEle<theElements.size(); jEle++) {  
      unsigned int iEle = theElements[jEle].second;
      PFBlockElement::Type type = elements[iEle].type();
      if (type == PFBlockElement::ECAL) {
	_nEcal ++;
      }
    }

    if(_nEcal!=1) continue;


  if(cluster_id.size()!=0){
    cluster_id.clear();
    seed_pdgid.clear();
    pseed_pdgid.clear();
    pseed_pt.clear();
    pseed_R.clear();
    isPrimary.clear();
    nprocess.clear();

    history_pdgid.clear();
    history_pt.clear();
    history_r.clear();
    history_ii_global.clear();
    history_ii_photon.clear();
    history_processtype.clear();

  }



    int nEcal = 0;
    int nbadEcal = 0;
    for(unsigned jEle=0; jEle<theElements.size(); jEle++) { 	// bugfix
      unsigned int iEle = theElements[jEle].second;
      PFBlockElement::Type type = elements[iEle].type();
      if (type == PFBlockElement::ECAL) {
	nEcal ++;
	const reco::PFBlockElementCluster& et =
	  dynamic_cast<const reco::PFBlockElementCluster &>( elements[iEle] );
	float eclu = et.clusterRef()->energy();
        float etclu = et.clusterRef()->pt();
	map<float, unsigned int>::iterator cmp = ClusterMap.find( eclu );
	if ( cmp == ClusterMap.end() ) {
	  cout << " ..... WEIRD. constituent cluster was not found in cluster list... " << endl ;
	  nbadEcal++;
	}
	else {
	  simTrackId  = cmp -> second;
	  map<unsigned int, int>::iterator tmp = TrackIdMap.find( simTrackId );
	  if ( tmp == TrackIdMap.end() ) {
	    cout << " .... WEIRD... no pdgId in map TrackIdMap for simTrackId " << simTrackId << endl;
	    nbadEcal++;
	  }
	  else {
	    simTrackpdgId = tmp -> second;
	  }
	}

	TString stPrimary;
	if ( find( PrimariesSimTrackId.begin(), PrimariesSimTrackId.end(), simTrackId) != PrimariesSimTrackId.end() ) {
	  stPrimary = " [Primary] " ;
	}
	else stPrimary = " [Secondary] ";


        int _gen_ = simTrackpdgId;
        int _trackid_ = (int)simTrackId;

        if(stPrimary==" [Secondary] "){
          _gen_ = 999;
          _trackid_ = 999;
          traceParent(SecondariesSimTrackId, SecondariesGenParticles, SecondariesParents, SecondariesPdgId, simTrackId, _gen_);
          traceTrack(SecondariesSimTrackId, SecondariesGenParticles, SecondariesParents, SecondariesPdgId, simTrackId, _trackid_);
        }

        float _R_ = -1;
        float _pt_ = -1;
        for(int ii=0; ii < (int)SecondariesSimTrackR.size(); ii++){
          if(SecondariesSimTrackId.at(ii)==_trackid_){
            _R_ = SecondariesSimTrackR.at(ii);
            _pt_ = SecondariesSimTrackpt.at(ii);
          }
        }

	// retrieve the vector of processIds, i.e. the history
	vector<unsigned int> vHistory;
	map<unsigned int, vector<unsigned int> >::iterator phis;
	phis = SimTrackHistory.find( simTrackId );
	if ( phis != SimTrackHistory.end() ) {
	  vHistory = phis -> second;
	}
	else {
	  cout << " .... WEIRD... simTrackId " << simTrackId << " not found in map SimTrackHistory " << endl;
	}

	vector<int> pHistory;
	map<unsigned int, vector<int> >::iterator phisPdg;
	phisPdg = SimTrackPdgIdHistory.find( simTrackId );
	if ( phisPdg != SimTrackPdgIdHistory.end() ) {
	  pHistory = phisPdg -> second;
	}
	else {
	  cout << " .... WEIRD... simTrackId " << simTrackId << " not found in map SimTrackPdgIdHistory " << endl;
	}

	vector<float> rHistory;
	map<unsigned int, vector<float> >::iterator phisR;
	phisR = SimTrackRHistory.find( simTrackId );
	if ( phisR != SimTrackRHistory.end() ) {
	  rHistory = phisR -> second;
	}
	else {
	  cout << " .... WEIRD... simTrackId " << simTrackId << " not found in map SimTrackPdgIdHistory " << endl;
	}


	cout << "\t  ECAL cluster number " << nEcal << " et " << etclu << " induced by simTrack " << simTrackId << " pdgId of simTrack " << simTrackpdgId << " " << stPrimary << " parent pdgId " << _gen_ << ", track id = " << _trackid_ << " ProcessIds " ;

	int _simplepdgId_ = 3;
	if(abs(simTrackpdgId)==211) _simplepdgId_ = 2;
	else if(abs(simTrackpdgId)==22) _simplepdgId_ = 1;
	else if(abs(simTrackpdgId)==11) _simplepdgId_ = 0;

	Bool_t isIonization = false;
	Bool_t isBrems = false;
	Bool_t isConv = false;
	Bool_t isHad = false;
	Bool_t isDecay = false;
	Bool_t isOther = false;	
	Bool_t isSecondary = false;


	vector<float> VecOfMomenta;
	map<unsigned int, vector<float> >::iterator itMomenta = SimTrackMomentaHistory.find( simTrackId );
	if ( itMomenta != SimTrackMomentaHistory.end() ) {
	  VecOfMomenta = itMomenta -> second;

	  //	  std::cout << "size (p, process) = " << VecOfMomenta.size() << " " << vHistory.size() << std::endl;

	  //	  cout << "\t \t \t TrMomenta : " ;
	  //	  for (unsigned int vit = 0; vit < VecOfMomenta.size(); ++vit) {
//	    cout <<  VecOfMomenta.at( vit ) << " " ;	    
	  //	  }
	  //	  cout << endl;
	}



	for (unsigned int vit = 0; vit < vHistory.size(); ++vit) {
	  if(VecOfMomenta.size() == vHistory.size()){
	    cout << "\t\t Process ID = " << vHistory.at( vit) << " (PDG ID = " << pHistory.at(vit) << ", R = " << rHistory.at(vit) << ", pT = " << VecOfMomenta.at(vit)  << ") " << std::endl;
	    history_pt.push_back(VecOfMomenta.at(vit));
	  }else{
	    cout << "\t\t Process ID = " << vHistory.at( vit) << " (PDG ID = " << pHistory.at(vit) << ", R = " << rHistory.at(vit) << ", pT = -1 (unknown)) " << std::endl;
	    history_pt.push_back(-1);
	  }


	  history_pdgid.push_back(pHistory.at(vit));
	  history_r.push_back(rHistory.at(vit));
	  history_ii_global.push_back(global_counter);
	  history_ii_photon.push_back(photon_counter);

	  history_processtype.push_back(vHistory.at( vit));



	  //	  int _simpleprocessId_ = 6;
	  if(vHistory.at(vit)==2) isIonization = true;
	  else if(vHistory.at(vit)==3) isBrems = true;
	  else if(vHistory.at(vit)==14) isConv = true;
	  else if(vHistory.at(vit)==121) isHad = true;
	  else if(vHistory.at(vit)==201) isDecay = true;
	  else{
	    if(vHistory.at(vit)!=0){
	      std::cout << "isOther = " << vHistory.at(vit) << std::endl;
	      isOther = true;
	    }
	  }

	  if(vHistory.at(vit)!=0) isSecondary = true;
	}

	if(isSecondary==false) history->Fill(_simplepdgId_, 0);
	if(isIonization) history->Fill(_simplepdgId_, 1);
	if(isBrems) history->Fill(_simplepdgId_, 2);
	if(isConv) history->Fill(_simplepdgId_, 3);
	if(isHad) history->Fill(_simplepdgId_, 4);
	if(isDecay) history->Fill(_simplepdgId_, 5);
	if(isOther) history->Fill(_simplepdgId_, 6);

	cout << endl;
	// now print the vector of Transverse momenta for this track,
	// starting from the primary particle :

	

	//	std::cout << stPrimary  <<  " parent pdgId == " << _gen_ << ", track id = " << _trackid_ << ", R = " << _R_ <<  ", pt = " << _pt_ << std::endl;

	cluster_id.push_back(nEcal);
	seed_pdgid.push_back(simTrackpdgId);
	pseed_pdgid.push_back(_gen_);

	nprocess.push_back(vHistory.size()-1);
	pseed_pt.push_back(_pt_);
	pseed_R.push_back(_R_);
	isPrimary.push_back((stPrimary==" [Primary] "));

      }
    }


   
    evtnum = iEvent.id().event();
    evtcounter = counter;
    ncluster = nEcal;
    nbadcluster = nbadEcal;
    gamma_pt = candPt;
    gamma_eta = candEta;
    gamma_phi = candPhi;
    gamma_global_counter = global_counter;
    gamma_photon_counter = photon_counter;

    gamma_total_iso = isolationGamma;
    tau_pt = pT;
    tau_eta = eta;
    tau_phi = phi;
    tau_gen_pt = _genpt;
    tau_gen_eta = _geneta;
    tau_gen_energy = _gen_e;

    tau_dm = iterTau->decayMode();
    gen_dm = gendm;

    int tau_dm_rough_ = iterTau->decayMode();
    if(tau_dm_rough_==0) tau_dm_rough_ = 0;
    else if(tau_dm_rough_==1 || tau_dm_rough_==2) tau_dm_rough_ = 1;
    else if(tau_dm_rough_==10) tau_dm_rough_ = 2; 

    int gen_dm_rough_ = gen_dm;
    if(gen_dm_rough_==0) gen_dm_rough_ = 0;
    else if(gen_dm_rough_==1 || gen_dm_rough_==2) gen_dm_rough_ = 1;
    else if(gen_dm_rough_==10) gen_dm_rough_ = 2; 

    tau_dm_rough = tau_dm_rough_;
    gen_dm_rough = gen_dm_rough_;
    
   
    tree->Fill();
    photon_counter ++;

  }

  global_counter++;
}



void
GeantAnalyzer::PrintSimHits(edm::Handle<edm::PSimHitContainer> simHitslowHandle, TString detector) {

  PSimHitContainer::const_iterator iterSimHits;
  for ( iterSimHits = simHitslowHandle->begin();
        iterSimHits != simHitslowHandle->end();
        ++iterSimHits) {
    unsigned int trackId = iterSimHits -> trackId();
    unsigned short processType = iterSimHits -> processType();
    int type = iterSimHits -> particleType();
    float pabs = iterSimHits -> pabs();
    float eloss = iterSimHits -> energyLoss();
    float tof = iterSimHits -> timeOfFlight();

    unsigned int detid = iterSimHits -> detUnitId();
    DetId tkId( detid );

    int layer = -1;	 // layer or disk
    TString geo = " dummy ";

    if (detector == "BPIX") {
      PXBDetId pxbdetid(tkId);
      layer = pxbdetid.layer();
      geo = " layer ";
    }
    if (detector == "FPIX") {
      PXFDetId pxbdetid(tkId);
      layer = pxbdetid.disk();
      geo = " disk ";
    }
    if (detector == "TIB") {
      TIBDetId pxbdetid(tkId);
      layer = pxbdetid.layer();
      geo = " layer ";
    }
    if (detector == "TID") {
      TIDDetId pxbdetid(tkId);
      layer = pxbdetid.wheel();
      geo = " wheel ";
    }
    if (detector == "TOB") {
      TOBDetId pxbdetid(tkId);
      layer = pxbdetid.layer();
      geo = " layer ";
    }
    if (detector == "TEC") {
      TECDetId pxbdetid(tkId);
      layer = pxbdetid.wheel();
      geo = " wheel ";
    }

   

    cout << " a hit : trackId " << trackId << " partType " << type << " processType " << processType << " p at entry " <<  pabs << " eloss " << eloss << " tof " << tof <<  " tkId.subdetId " << tkId.subdetId() << geo << layer <<endl;

  } // end loop over simhits

}


// --------------------------------------------------------------------------------------------------------

void
GeantAnalyzer::PrintCaloHits(edm::Handle<edm::PCaloHitContainer> simHitslowHandle, float threshold) {

  PCaloHitContainer::const_iterator iterSimHits;
  for ( iterSimHits = simHitslowHandle->begin();
        iterSimHits != simHitslowHandle->end();
        ++iterSimHits) {

    unsigned int trackId = iterSimHits -> geantTrackId();
    unsigned int detid = iterSimHits -> id();
    float eloss = iterSimHits -> energy();

    map<unsigned int, map<unsigned int, float> >::iterator p;
    p = PCaloHitEnergyMap.find( detid );

    if ( p == PCaloHitEnergyMap.end() )  {  // new hit detid. Insert in the map
      map<unsigned int, float> mapOfaDetid;
      mapOfaDetid.insert( pair<unsigned int, float>(trackId,  eloss ) ) ;
      PCaloHitEnergyMap.insert( pair<unsigned int, map<unsigned int, float> >(detid, mapOfaDetid) ) ;
    }
    else { 	// this detId has already received some energy deposit
      map<unsigned int, float> mapOfaDetid = p -> second;
      map<unsigned int, float>::iterator pp = mapOfaDetid.find( trackId );
      if ( pp == mapOfaDetid.end() ) {    // that's a new SimTrackId for this detId
	mapOfaDetid.insert( pair<unsigned int, float>(trackId,  eloss ) ) ;
	PCaloHitEnergyMap[ detid ] = mapOfaDetid ;
      }
      else {	// this SimTrackId has already lead to an energy deposit in this detId.
		// make the sum to get the total energy deposit
	float edep = pp -> second;
	edep += eloss ;
	mapOfaDetid[ trackId ] = edep;
	PCaloHitEnergyMap[ detid ] = mapOfaDetid ;
      } //endif pp == mapOfaDetid.end()
    }
      

    // now do the printouts :

    int pdgId = -999;
    map<unsigned int, int>::iterator q;
    q = TrackIdMap.find( trackId );
    if ( q != TrackIdMap.end() ) pdgId = q -> second;

    float tof = iterSimHits -> time();
    float depth = iterSimHits -> depth();

    if (eloss < threshold) continue;

    TString seta="dummy";
    TString sphi = "dummy";

    DetId tkId( detid );
    int subdet = tkId.subdetId();
    int ieta = -1;
    int iphi = -1;
    float eta = -999;
    float phi = -999;
    if (subdet == EcalSubdetector::EcalBarrel) {
      EBDetId eb( tkId );
      ieta = eb.ieta();
      iphi = eb.iphi();
      eta = eb.approxEta();
      phi = float( iphi -1 )  + 0.05 ;
      phi = phi * 2.*TMath::Pi() / 360;	// iphi between 1 and 360
      if (phi > TMath::Pi()) phi = phi - 2.*TMath::Pi(); 
      seta = " ieta ";
      sphi = " iphi ";
    } 
    if (subdet == EcalSubdetector::EcalEndcap) {
      EEDetId eb( tkId );
      ieta = eb.ix();
      iphi = eb.iy();
      seta = " ix ";
      sphi = " iy ";
    }

    if (doPrintCaloHits) cout << " a hit : trackId " << trackId << " pdgId " << pdgId << " eloss " << eloss << " time " << tof <<  " depth " << depth << " detId " << detid << seta  << ieta << sphi  << iphi << " eta " << eta << " phi " << phi << endl;

  } // end loop over simhits

}

// ---------------------------------------------------------------------------------------


void GeantAnalyzer::FillTheMainMapForDetIds() {

  // from the map PCaloHitEnergyMap  (  detid, ( simtrackId, eloss )  ), fill the main
  // map PCaloHitMap  ( detid, simtrackId ) : 
  // When several SimTracks have deposited some energy in the detid (this may be
  // in several hits), it is the SimTrack with the largest energy deposit that will be
  // mapped to the detId.

  map<unsigned int, map<unsigned int, float> >::iterator p;

  for ( p = PCaloHitEnergyMap.begin(); p != PCaloHitEnergyMap.end(); p++) {
    unsigned int detid = p -> first;
    map<unsigned int, float> mapOfaDetid = p -> second;
    float emax = -999;
    map<unsigned int, float>::iterator q;
    unsigned theTrackId = -1;
    // loop over the SimTracks:
    for ( q = mapOfaDetid.begin();  q != mapOfaDetid.end(); q++) {
      unsigned int trackid = q -> first;
      float edep = q -> second;
      if (edep > emax) {
	emax = edep;
	theTrackId = trackid;
      }
    }  // end loop over the simtracks
    PCaloHitMap.insert( pair<unsigned int, unsigned int>(detid, theTrackId) ) ;
  }  // end loop over the hit detIds

}



// ---------------------------------------------------------------------------------------

template<typename T>
void GeantAnalyzer::PrintPFRecHits(edm::Handle< T > pfRecHitsHandle, float threshold, bool physonly) {

  typename T::const_iterator iterPFRecHits;

  //cout << " std::type_info " <<  demangle( typeid(T).name() ) << endl;
  //std::string ClassName = demangle( typeid(T).name() ) ;
  
  int nh = 0;

  for ( iterPFRecHits = pfRecHitsHandle->begin(); iterPFRecHits != pfRecHitsHandle->end(); ++iterPFRecHits) {
    unsigned int id = GetDetId( iterPFRecHits );

    float energy = iterPFRecHits->energy();
    RecHitMap.insert( pair<unsigned int, float>(id, energy ) ) ;

    // look for the detId in the map PCaloHitMap
    unsigned int trackId = 0;
    int pdgId = -1;
    map<unsigned int, unsigned int>::iterator p;
    p = PCaloHitMap.find( id );
    if ( p != PCaloHitMap.end() ) trackId = p -> second;

    if (trackId > 0) {
      map<unsigned int, int>::iterator q;
      q = TrackIdMap.find( trackId );
      if ( q != TrackIdMap.end() ) pdgId = q -> second;
    }


    if ( trackId <= 0 && physonly) continue;

    int ieta = -1;
    int iphi = -1;

    DetId detid( id );
    TString seta = "dummy";
    TString sphi = "dummy";
    if ( detid.det() == 3)  {	// ECAL
      int subdet = detid.subdetId();
      if (subdet == EcalSubdetector::EcalBarrel) {
	EBDetId eb( detid );
	ieta = eb.ieta();
	iphi = eb.iphi();
	seta = " ieta " ;
	sphi = " iphi ";
      }
      if (subdet == EcalSubdetector::EcalEndcap) {
	EEDetId eb( detid );
	ieta = eb.ix();
	iphi = eb.iy();
	seta = " ix ";
	sphi = " iy ";
      }
    }

    if ( energy <= threshold) continue;
    if (doPrintRecHits) cout << " id " << id << " energy " << energy << " trackId " << trackId << " pdgId " << pdgId << seta  << ieta << sphi  << iphi << endl;
    nh ++;

  }

  std::string ClassName = typeid(T).name() ;
  if ( nh > 0 && ClassName.find( "PFRecHit") != std::string::npos)  cout << " --- FOUND PFRecHit " << nh << endl;

}


// ------------------------------------------------------------------------------------------

void GeantAnalyzer::PrintPFClusters(  edm::Handle< vector<reco::PFCluster> > pPFClustersECALHandle , int verbose ) 
{

  vector<reco::PFCluster>::const_iterator iterCluster;

  for (iterCluster = pPFClustersECALHandle -> begin(); 
       iterCluster != pPFClustersECALHandle->end();
       ++iterCluster) {

    float energy = iterCluster -> energy();

    // get the seed :

    DetId seed = iterCluster -> seed();
    unsigned int detid = seed.rawId() ;
    float eta = iterCluster->eta();
    float phi = iterCluster -> phi();
    unsigned int trackId = 0;
    int pdgId = -999;

    map<unsigned int, unsigned int>::iterator p = PCaloHitMap.find( detid );
    if ( p != PCaloHitMap.end() ) {
      trackId = p -> second;
      map<unsigned int, int>::iterator q = TrackIdMap.find( trackId );
      if ( q != TrackIdMap.end() ) pdgId = q -> second;
    }

    if (verbose > 0) cout << " a PF Cluster of energy " << energy << " detid of seed " << detid << " at eta " << eta << " phi " << phi << " seeded by trackId " << trackId << " pdgId " << pdgId << endl;

    ClusterMap.insert( pair<float, unsigned int>(energy, trackId) ) ;

    if ( trackId == 0) {
      // is the seed cluster is in the preshower ?
      // check the detector of this seed
      // else, must correspond to noise digi !
      DetId::Detector  det = seed.det();	// { Tracker=1,Muon=2,Ecal=3,Hcal=4,Calo=5 }
      int subdet = seed.subdetId();   //  enum EcalSubdetector { EcalBarrel=1, EcalEndcap=2, EcalPreshower=3, EcalTriggerTower=4, EcalLaserPnDiode=5 };
      cout << "\t det = " << det << " subdetector = " << subdet << endl;
    }

    // now, loop over all RecHits that make this cluster
    const std::vector< std::pair<DetId, float> >  hitsAndFractions = iterCluster -> hitsAndFractions();
    unsigned int nhits = hitsAndFractions.size();
    for (unsigned int ihit=0; ihit < nhits; ihit++) {
      std::pair<DetId, float> dd = hitsAndFractions[ihit];
      DetId theDetid = dd.first;
      float efrac = dd.second;
      unsigned int thedetid = theDetid.rawId();
      map<unsigned int, unsigned int>::iterator p = PCaloHitMap.find( thedetid );
      unsigned int thetrackId = 0;
      int thepdgId = -999;
      if ( p != PCaloHitMap.end() ) {
	thetrackId = p -> second;
	map<unsigned int, int>::iterator q = TrackIdMap.find( thetrackId );
	if ( q != TrackIdMap.end() ) thepdgId = q -> second;
	float theenergy = -1;  // energy of this RecHit
	map<unsigned int, float>::iterator rhp = RecHitMap.find( thedetid );
	if ( rhp != RecHitMap.end()) theenergy = rhp -> second;
	if (verbose > 1) cout << "\t RecHit energy " << theenergy << " detid " << thedetid <<  " trackId " << thetrackId << " pdgId " << thepdgId << " energy frac " << efrac << endl;
      }
    } // end loop over RecHits
 


  } // end loop over clusters

}





void 
GeantAnalyzer::beginJob(){
  history = fs_->make<TH2F>("history","history",4,0,4,7,0,7);

  TString ylabel[7] = {"Primary",
		       "Ionization",
		       "Brems",
		       "Conversion",
		       "Had. Inelastic",
		       "Decay",
		       "Other"};

  TString xlabel[4] = {"e",
		       "#gamma",
		       "#pi",
		       "Other"};

  for(int ibin=1; ibin < history->GetXaxis()->GetNbins()+1; ibin++){
    history->GetXaxis()->SetBinLabel(ibin, xlabel[ibin-1]);
  }
  
  for(int ibin=1; ibin < history->GetYaxis()->GetNbins()+1; ibin++){
    history->GetYaxis()->SetBinLabel(ibin, ylabel[ibin-1]);
  }

}

void 
GeantAnalyzer::endJob(){

  for(int ibin=1; ibin < history->GetXaxis()->GetNbins()+1; ibin++){

    Float_t total = 0.;

    for(int iibin=1; iibin < history->GetYaxis()->GetNbins()+1; iibin++){
      total += history->GetBinContent(ibin, iibin);
    }

    for(int iibin=1; iibin < history->GetYaxis()->GetNbins()+1; iibin++){
      Float_t frac = (history->GetBinContent(ibin, iibin))/total;
      history->SetBinContent(ibin, iibin, frac);
    }

  }

}

void
GeantAnalyzer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

DEFINE_FWK_MODULE(GeantAnalyzer);
