#include "RecoLuminosity/ROOTSchema/interface/ROOTFileBase.h"
#include "RecoLuminosity/TCPReceiver/interface/LumiStructures.hh"

#ifdef __CINT__
#ifndef ROOTSCHEMA_LINKDEF
#define ROOTSCHEMA_LINKDEF

#pragma link off all globals;
#pragma link off all classes;
#pragma link off all functions;

#pragma link C++ nestedclasses;
#pragma link C++ nestedtypedefs;

#pragma link C++ namespace HCAL_HLX;

#pragma link C++ struct HCAL_HLX::LUMI_SUMMARY+;
#pragma link C++ struct HCAL_HLX::LUMI_DETAIL+;
#pragma link C++ struct HCAL_HLX::LUMI_SECTION_HEADER+;
#pragma link C++ struct HCAL_HLX::ET_SUM_SECTION+;
#pragma link C++ struct HCAL_HLX::OCCUPANCY_SECTION+;
#pragma link C++ struct HCAL_HLX::LHC_SECTION+;
#pragma link C++ struct HCAL_HLX::LUMI_SECTION+;

#endif
#endif

