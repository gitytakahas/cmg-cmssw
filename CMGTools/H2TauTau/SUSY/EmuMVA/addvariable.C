#include <iostream>
#include <string>
#include "TFile.h"
#include "TTree.h"
#include "TMath.h"

void addvariable(TString filename, TString output, TString process){

  Double_t lum = 19700;
  Double_t weight_tt2l = 25.144*lum/12011428;
  Double_t weight_tt1l = 104.921*lum/24953451;
  Double_t weight_dy = 3503.71*lum/30459503;
  Double_t weight_w = 36257.2*lum/57709905;
  Double_t weight_data = 1;



  std::cout << "Process = " << process << std::endl;
  std::cout << "input file = " <<  filename << std::endl;
  std::cout << "output file = " <<  output << std::endl;

  TFile *lFile = new TFile(filename);
  TTree *lTree = (TTree*) lFile->FindObjectAny("H2TauTauTreeProducerTauMu");

  Double_t leptonAccept = 0;
  Double_t thirdLeptonVeto = 0;
  Double_t l1_threeHitIso = 0;

  Double_t l1_againstMuonTight = 0;
  Double_t l1_againstElectronLoose = 0;
  Double_t l1_dxy = 0;
  Double_t l1_dz = 0;
  Double_t l1_pt = 0;

  Double_t l2_relIso05 = 0;
  Double_t l2_tightId = 0;
  Double_t l2_dxy = 0;
  Double_t l2_dz = 0;
  Double_t l2_pt = 0;

  Double_t weight = 0;

  lTree->SetBranchAddress("leptonAccept", &leptonAccept);
  lTree->SetBranchAddress("thirdLeptonVeto", &thirdLeptonVeto);
  lTree->SetBranchAddress("l1_threeHitIso", &l1_threeHitIso);
  lTree->SetBranchAddress("l1_againstMuonTight", &l1_againstMuonTight);
  lTree->SetBranchAddress("l1_againstElectronLoose", &l1_againstElectronLoose);
  lTree->SetBranchAddress("l1_dxy", &l1_dxy);
  lTree->SetBranchAddress("l1_dz", &l1_dz);
  lTree->SetBranchAddress("l1_pt", &l1_pt);

  lTree->SetBranchAddress("l2_relIso05", &l2_relIso05);
  lTree->SetBranchAddress("l2_tightId", &l2_tightId);
  lTree->SetBranchAddress("l2_dxy", &l2_dxy);
  lTree->SetBranchAddress("l2_dz", &l2_dz);
  lTree->SetBranchAddress("l2_pt", &l2_pt);

  lTree->SetBranchAddress("weight", &weight);

  TFile *lOFile = new TFile(output,"RECREATE");
  TTree *lOTree = lTree->CloneTree(0);
   
  Int_t pid;
  lOTree->Branch("pid", &pid, "pid/I");

  Double_t weight2;
  lOTree->Branch("weight2", &weight2, "weight2/D");

  std::cout << "process : " << process << std::endl;
   

  for (Long64_t i0=0; i0<lTree->GetEntries(); i0++) {
    lTree->GetEntry(i0);


//    std::cout << "lepton_accept " << leptonAccept << std::endl;
//    std::cout << "3rd lepton veto " << thirdLeptonVeto << std::endl;
//    std::cout << "threeHitIso " << l1_threeHitIso << std::endl;
//    std::cout << "l1_againstMuonTight " << l1_againstMuonTight << std::endl;
//    std::cout << "l1_againstElectronLooose " << l1_againstElectronLoose << std::endl;
//    std::cout << "l1_dxy " << l1_dxy << std::endl;
//    std::cout << "l1_dz " << l1_dz << std::endl;
//    std::cout << "l1_pt " << l1_pt << std::endl;
//    
//    std::cout << "l2_reliso "<<l2_relIso05 << std::endl;
//    std::cout << "l2_tightid "<<l2_tightId << std::endl;
//    std::cout << "l2_dxy " << l2_dxy << std::endl;
//    std::cout << "l2_dz " << l2_dz << std::endl;
//    std::cout << "l2_pt " << l2_pt << std::endl;

    
    if(!(leptonAccept && thirdLeptonVeto && l1_threeHitIso<1.5 && l1_againstMuonTight>0.5 && l1_againstElectronLoose>0.5 && l1_dxy<0.045 && l1_dz<0.2 && l1_pt>20)) continue;
    if(!(l2_relIso05<0.1 && l2_tightId>0.5 && l2_dxy<0.045 && l2_dz<0.2 && l2_pt>20)) continue;

    if(process=="DYJets") pid=1;
    else if(process=="TTJetsFullLept" || process=="TTJetsSemiLept") pid=2;
    else if(process=="WJets") pid=3;
    else if(process=="data_Run2012A" || process=="data_Run2012B" || process=="data_Run2012C" || process=="data_Run2012D") pid=0;
    
    if(process=="DYJets") weight2 = weight*weight_dy;
    else if(process=="TTJetsFullLept") weight2 = weight*weight_tt2l;
    else if(process=="TTJetsSemiLept") weight2 = weight*weight_tt1l;
    else if(process=="DYJets") weight2 = weight*weight_dy;
    else if(process=="WJets") weight2 = weight*weight_w;
    else if(process=="data_Run2012A" || process=="data_Run2012B" || process=="data_Run2012C" || process=="data_Run2012D") weight2 = weight;


    lOTree->Fill();    
  }

  lOTree->Write();
  lOFile->Close();

  delete lFile;

  lFile = 0; lTree = 0; lOTree = 0;

}

