// Take the isolation pt sums calculated for reconstructed tau 
// candidates and store them in PFTau objects

// Author: Pavel Jez, Universite Catholique de Louvain

//#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"

#include "DataFormats/TauReco/interface/PFTau.h"
#include "DataFormats/Common/interface/ValueMap.h"


class RecoTauIsoSumFiller : public edm::stream::EDProducer<> {
  public:
    RecoTauIsoSumFiller(const edm::ParameterSet& pset);
    virtual ~RecoTauIsoSumFiller(){}
    void produce(edm::Event& evt, const edm::EventSetup& es) override;
  private:
    edm::InputTag src_;
    edm::EDGetTokenT<std::vector<reco::PFTau> >PFTauToken_;
  
    std::vector<edm::InputTag> inputTagIsoVals;
    std::vector<edm::EDGetTokenT<edm::ValueMap<double> > > tokenIsoVals;

};

RecoTauIsoSumFiller::RecoTauIsoSumFiller(const edm::ParameterSet& pset){
  src_ = pset.getParameter<edm::InputTag>("src");
  PFTauToken_ = consumes<std::vector<reco::PFTau> >(src_);
  edm::ParameterSet pfIsoVals = pset.getParameter<edm::ParameterSet>("pfIsolationValues");
  if (! pfIsoVals.empty()) {
    inputTagIsoVals.push_back(pfIsoVals.getParameter<edm::InputTag>("pfSumChargedHadronPt"));
    inputTagIsoVals.push_back(pfIsoVals.getParameter<edm::InputTag>("pfSumPhotonEt"));
    inputTagIsoVals.push_back(pfIsoVals.getParameter<edm::InputTag>("pfSumNeutralHadronEt"));
    inputTagIsoVals.push_back(pfIsoVals.getParameter<edm::InputTag>("pfSumPUPt"));
    }

  tokenIsoVals.resize(inputTagIsoVals.size());
  for(size_t j=0; j < tokenIsoVals.size(); j++) {
    tokenIsoVals[j] = consumes<edm::ValueMap<double> >(inputTagIsoVals[j]);
  }

  produces<reco::PFTauCollection>();
}

void RecoTauIsoSumFiller::produce(edm::Event& evt, const edm::EventSetup& es){

  edm::Handle<std::vector<reco::PFTau> > Taus;
  evt.getByToken(PFTauToken_,Taus);

  std::vector< edm::Handle< edm::ValueMap<double> > > tauIsolationValues;
  tauIsolationValues.resize(tokenIsoVals.size());

  for (size_t j = 0; j < tokenIsoVals.size(); j++) {
    evt.getByToken(tokenIsoVals[j], tauIsolationValues[j]);
  }
  
  std::auto_ptr<reco::PFTauCollection> tausOut(new reco::PFTauCollection);

  size_t iPFTau = 0;
  //  for(reco::PFTauCollection::size_type iPFTau = 0; iPFTau < Taus->size(); iPFTau++) {
    for (const reco::PFTau & iTau : *Taus) {
    //    std::cout << iTau.pt() << std::endl;
    reco::PFTau myTau = reco::PFTau(iTau);
    reco::PFTauRef tau(Taus, iPFTau);
    
    float tmpIso=float((*tauIsolationValues[0])[tau]);
    myTau.setisolationPFChargedHadrCandsPtSum(tmpIso);
    tmpIso=float((*tauIsolationValues[1])[tau]);
    myTau.setisolationPFGammaCandsEtSum(tmpIso);
    tmpIso=float((*tauIsolationValues[2])[tau]);
    myTau.setisolationPFNeutralHadrCandsPtSum(tmpIso);
    tmpIso=float((*tauIsolationValues[3])[tau]);
    myTau.setisolationPFPUCandsEtSum(tmpIso);

    tausOut->push_back(myTau);
    iPFTau++;
  }

  evt.put(tausOut);
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(RecoTauIsoSumFiller);
