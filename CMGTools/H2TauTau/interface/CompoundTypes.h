#ifndef COMPOUNDTYPES_H_
#define COMPOUNDTYPES_H_

#include "CMGTools/H2TauTau/interface/DiObject.h"
#include "CMGTools/H2TauTau/interface/DiTauObject.h"
#include "CMGTools/H2TauTau/interface/Electron.h"
#include "CMGTools/H2TauTau/interface/Muon.h"
#include "CMGTools/H2TauTau/interface/Tau.h"
#include "CMGTools/H2TauTau/interface/GenericTypes.h"

#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"

namespace cmg {

  typedef cmg::DiObject<cmg::Electron,cmg::Electron> DiElectron;

  typedef cmg::DiObject<cmg::Muon, cmg::Muon > DiMuon;
  typedef cmg::DiTauObject<cmg::Tau, cmg::Tau> DiTau;
  typedef cmg::DiObject<cmg::Tau,cmg::Tau> DiTauDiObject;
  typedef cmg::DiTauObject<cmg::Tau, cmg::Electron> TauEle;
  typedef cmg::DiObject<cmg::Tau,cmg::Electron> TauEleDiObject;
  typedef cmg::DiTauObject<cmg::Tau, cmg::Muon> TauMu;
  typedef cmg::DiObject<cmg::Tau,cmg::Muon> TauMuDiObject; // still need to declare DiObject to generate dictionaries
  typedef cmg::DiTauObject<cmg::Muon,cmg::Electron> MuEleDiTau;
  typedef cmg::DiObject<cmg::Muon,cmg::Electron> MuEle;


}

#endif /*COMPOUNDTYPES_H_*/
