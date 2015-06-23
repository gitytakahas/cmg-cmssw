import ROOT, os, shelve, sys
import numpy as num
import math
from DataFormats.FWLite import Events, Handle
from Display import *
from DeltaR import *

ROOT.gROOT.SetBatch(True)

genParticlesH  = Handle ('std::vector<reco::GenParticle>')
tauH = Handle('std::vector<reco::PFTau>')
tauH_disc = Handle('reco::PFTauDiscriminator')
tauH_disc_weight = Handle('reco::PFTauDiscriminator')
tauH_ciso = Handle('reco::PFTauDiscriminator')
tauH_puiso = Handle('reco::PFTauDiscriminator')
vertexH = Handle('std::vector<reco::Vertex>')
jetH = Handle('std::vector<reco::PFJet>')

filelist = []
argvs = sys.argv
argc = len(argvs)

runtype = argvs[1]

def testGoodVertex(vertex):
    if vertex.isFake():
        return False
    if vertex.ndof()<=4:
        return False
    if abs(vertex.z())>24:
        return False
    if vertex.position().Rho()>2:
        return False
     
    return True


print 'You selected', runtype

s = shelve.open('test_' + runtype + '.db')


#for ii in range(1, 40):
for ii in range(2, 3):

    filename = ''
    
    if runtype == 'standard':
        filename = 'root://eoscms//eos/cms/store/cmst3/user/ytakahas/CMG/QCD_Pt-15to3000_Tune4C_Flat_13TeV_pythia8/Phys14DR-PU20bx25_trkalmb_PHYS14_25_V1-v1/AODSIM/Run1_noptcut_20150505/aod_' + str(ii) + '.root'
    elif runtype == 'dynamic90':
        filename = 'root://eoscms//eos/cms/store/cmst3/user/ytakahas/CMG/QCD_Pt-15to3000_Tune4C_Flat_13TeV_pythia8/Phys14DR-PU20bx25_trkalmb_PHYS14_25_V1-v1/AODSIM/Dynamic90_20150501/aod_' + str(ii) + '.root'
    elif runtype == 'dynamic95':
        filename = 'root://eoscms//eos/cms/store/cmst3/user/ytakahas/CMG/QCD_Pt-15to3000_Tune4C_Flat_13TeV_pythia8/Phys14DR-PU20bx25_trkalmb_PHYS14_25_V1-v1/AODSIM/Dynamic95_20150505/aod_' + str(ii) + '.root'
    elif runtype == 'run1':
        filename = 'root://eoscms//eos/cms/store/cmst3/user/ytakahas/CMG/QCD_Pt-15to3000_Tune4C_Flat_13TeV_pythia8/Phys14DR-PU20bx25_trkalmb_PHYS14_25_V1-v1/AODSIM/Run1Default/aod_' + str(ii) + '.root'


    print filename
    filelist.append(filename)

events = Events(filelist)
print len(filelist), 'files will be analyzed'


outputname = 'test_' + runtype + '.root'
file = ROOT.TFile(outputname, 'recreate')


h_ntau = ROOT.TH1F('h_ntau','h_ntau',30,0,30)
h_isfail = ROOT.TH1F('h_isfail','h_isfail',2,0,2)
h_isjetfail = ROOT.TH1F('h_isjetfail','h_isjetfail',2,0,2)

tau_tree = ROOT.TTree('per_tau','per_tau')
photon_tree = ROOT.TTree('per_photon','per_photon')

tau_id = num.zeros(1, dtype=int)
tau_nphoton = num.zeros(1, dtype=int)
tau_nphoton_signal = num.zeros(1, dtype=int)
tau_nphoton_outside = num.zeros(1, dtype=int)
tau_photonsumpt_outside = num.zeros(1, dtype=float)
tau_photonsumpt_outside_weight1 = num.zeros(1, dtype=float)
tau_photonsumpt_outside_weight2 = num.zeros(1, dtype=float)
tau_photonsumpt_outside_weight3 = num.zeros(1, dtype=float)
tau_nphoton_inside = num.zeros(1, dtype=int)
tau_nphoton_iso_inside = num.zeros(1, dtype=int)
tau_nphoton_iso_outside = num.zeros(1, dtype=int)
tau_photonsumpt_inside = num.zeros(1, dtype=float)
tau_photonsumpt_iso_inside = num.zeros(1, dtype=float)
tau_photonsumpt_iso_outside = num.zeros(1, dtype=float)
tau_photon_ratio = num.zeros(1, dtype=float)
tau_nisopizero = num.zeros(1, dtype=int)
tau_nsignalpizero = num.zeros(1, dtype=int)
tau_dm = num.zeros(1, dtype=int)
tau_dm_rough = num.zeros(1, dtype=int)
tau_niso = num.zeros(1, dtype=float)
tau_niso_weighted = num.zeros(1, dtype=float)
tau_ciso = num.zeros(1, dtype=float)
tau_ciso_old = num.zeros(1, dtype=float)
tau_puiso = num.zeros(1, dtype=float)
tau_pt = num.zeros(1, dtype=float)
tau_eta = num.zeros(1, dtype=float)
tau_phi = num.zeros(1, dtype=float)
tau_energy = num.zeros(1, dtype=float)
tau_mass = num.zeros(1, dtype=float)
tau_emFraction = num.zeros(1, dtype=float)
tau_corjetpt = num.zeros(1, dtype=float)
tau_corjeteta = num.zeros(1, dtype=float)
tau_corjetphi = num.zeros(1, dtype=float)
tau_vertex = num.zeros(1, dtype=int)
tau_gvertex = num.zeros(1, dtype=int)
tau_adR_signal = num.zeros(1, dtype=float)
tau_wdR_signal = num.zeros(1, dtype=float)
tau_adR_iso = num.zeros(1, dtype=float)
tau_wdR_iso = num.zeros(1, dtype=float)

photon_pt = num.zeros(1, dtype=float)
photon_eta = num.zeros(1, dtype=float)
photon_phi = num.zeros(1, dtype=float)
photon_dr = num.zeros(1, dtype=float)
photon_deta = num.zeros(1, dtype=float)
photon_dphi = num.zeros(1, dtype=float)
photon_isOutside = num.zeros(1, dtype=int)
photon_isIsolation = num.zeros(1, dtype=int)
photon_dm_rough = num.zeros(1, dtype=int)
photon_dm = num.zeros(1, dtype=int)
photon_taupt = num.zeros(1, dtype=float)
photon_taueta = num.zeros(1, dtype=float)
photon_tauphi = num.zeros(1, dtype=float)
photon_vertex = num.zeros(1, dtype=int)
photon_gvertex = num.zeros(1, dtype=int)
photon_niso = num.zeros(1, dtype=float)

tau_tree.Branch('tau_id', tau_id, 'tau_id/I')
tau_tree.Branch('tau_nphoton', tau_nphoton, 'tau_nphoton/I')
tau_tree.Branch('tau_nphoton_signal', tau_nphoton_signal, 'tau_nphoton_signal/I')
tau_tree.Branch('tau_vertex', tau_vertex, 'tau_vertex/I')
tau_tree.Branch('tau_gvertex', tau_gvertex, 'tau_gvertex/I')
tau_tree.Branch('tau_nisopizero', tau_nisopizero, 'tau_nisopizero/I')
tau_tree.Branch('tau_nsignalpizero', tau_nsignalpizero, 'tau_nsignalpizero/I')
tau_tree.Branch('tau_niso', tau_niso, 'tau_niso/D')
tau_tree.Branch('tau_niso_weighted', tau_niso_weighted, 'tau_niso_weighted/D')
tau_tree.Branch('tau_ciso', tau_ciso, 'tau_ciso/D')
tau_tree.Branch('tau_ciso_old', tau_ciso_old, 'tau_ciso_old/D')
tau_tree.Branch('tau_puiso', tau_puiso, 'tau_puiso/D')
tau_tree.Branch('tau_dm', tau_dm, 'tau_dm/I')
tau_tree.Branch('tau_dm_rough', tau_dm_rough, 'tau_dm_rough/I')
tau_tree.Branch('tau_pt', tau_pt, 'tau_pt/D')
tau_tree.Branch('tau_eta', tau_eta, 'tau_eta/D')
tau_tree.Branch('tau_phi', tau_phi, 'tau_phi/D')
tau_tree.Branch('tau_energy', tau_energy, 'tau_energy/D')
tau_tree.Branch('tau_mass', tau_mass, 'tau_mass/D')
tau_tree.Branch('tau_emFraction', tau_emFraction, 'tau_emFraction/D')
tau_tree.Branch('tau_nphoton_outside', tau_nphoton_outside, 'tau_nphoton_outside/I')
tau_tree.Branch('tau_photonsumpt_outside', tau_photonsumpt_outside, 'tau_photonsumpt_outside/D')
tau_tree.Branch('tau_photonsumpt_outside_weight1', tau_photonsumpt_outside_weight1, 'tau_photonsumpt_outside_weight1/D')
tau_tree.Branch('tau_photonsumpt_outside_weight2', tau_photonsumpt_outside_weight2, 'tau_photonsumpt_outside_weight2/D')
tau_tree.Branch('tau_photonsumpt_outside_weight3', tau_photonsumpt_outside_weight3, 'tau_photonsumpt_outside_weight3/D')

tau_tree.Branch('tau_nphoton_inside', tau_nphoton_inside, 'tau_nphoton_inside/I')
tau_tree.Branch('tau_nphoton_iso_inside', tau_nphoton_iso_inside, 'tau_nphoton_iso_inside/I')
tau_tree.Branch('tau_nphoton_iso_outside', tau_nphoton_iso_outside, 'tau_nphoton_iso_outside/I')

tau_tree.Branch('tau_photonsumpt_inside', tau_photonsumpt_inside, 'tau_photonsumpt_inside/D')
tau_tree.Branch('tau_photonsumpt_iso_inside', tau_photonsumpt_iso_inside, 'tau_photonsumpt_iso_inside/D')
tau_tree.Branch('tau_photonsumpt_iso_outside', tau_photonsumpt_iso_outside, 'tau_photonsumpt_iso_outside/D')
tau_tree.Branch('tau_photon_ratio', tau_photon_ratio, 'tau_photon_ratio/D')
tau_tree.Branch('tau_corjetpt', tau_corjetpt, 'tau_corjetpt/D')
tau_tree.Branch('tau_corjeteta', tau_corjeteta, 'tau_corjeteta/D')
tau_tree.Branch('tau_corjetphi', tau_corjetphi, 'tau_corjetphi/D')

tau_tree.Branch('tau_adR_signal', tau_adR_signal, 'tau_adR_signal/D')
tau_tree.Branch('tau_wdR_signal', tau_wdR_signal, 'tau_wdR_signal/D')
tau_tree.Branch('tau_adR_iso', tau_adR_iso, 'tau_adR_iso/D')
tau_tree.Branch('tau_wdR_iso', tau_wdR_iso, 'tau_wdR_iso/D')

photon_tree.Branch('photon_pt', photon_pt, 'photon_pt/D')
photon_tree.Branch('photon_eta', photon_eta, 'photon_eta/D')
photon_tree.Branch('photon_phi', photon_phi, 'photon_phi/D')
photon_tree.Branch('photon_dr', photon_dr, 'photon_dr/D')
photon_tree.Branch('photon_deta', photon_deta, 'photon_deta/D')
photon_tree.Branch('photon_dphi', photon_dphi, 'photon_dphi/D')
photon_tree.Branch('photon_isOutside', photon_isOutside, 'photon_isOutside/I')
photon_tree.Branch('photon_isIsolation', photon_isIsolation, 'photon_isIsolation/I')
photon_tree.Branch('photon_dm_rough', photon_dm_rough, 'photon_dm_rough/I')
photon_tree.Branch('photon_dm', photon_dm, 'photon_dm/I')
photon_tree.Branch('photon_taupt', photon_taupt, 'photon_taupt/D')
photon_tree.Branch('photon_taueta', photon_taueta, 'photon_taueta/D')
photon_tree.Branch('photon_tauphi', photon_tauphi, 'photon_tauphi/D')
photon_tree.Branch('photon_vertex', photon_vertex, 'photon_vertex/I')
photon_tree.Branch('photon_gvertex', photon_gvertex, 'photon_gvertex/I')
photon_tree.Branch('photon_niso', photon_niso, 'photon_niso/D')


counter = 0
evtid = 0

for event in events:
    
    evtid += 1  
    eid = event.eventAuxiliary().id().event()

    if evtid%1000 == 0:
        print 'Event ', evtid, 'processed'

#    if evtid==50000:
#    if evtid==2000:
    if evtid==100:
        break

    event.getByLabel("ak4PFJetsL1FastL2L3", jetH)
    event.getByLabel("hpsPFTauProducer", tauH)
    event.getByLabel("hpsPFTauMVA3IsolationNeutralIsoPtSum", tauH_disc)
    event.getByLabel("hpsPFTauMVA3IsolationNeutralIsoPtSumWeight", tauH_disc_weight)
    event.getByLabel("hpsPFTauMVA3IsolationChargedIsoPtSum", tauH_ciso)
    event.getByLabel("hpsPFTauMVA3IsolationPUcorrPtSum", tauH_puiso)
    event.getByLabel("offlinePrimaryVertices", vertexH)

    taus = tauH.product()
    taus_disc = tauH_disc.product()
    taus_disc_weight = tauH_disc_weight.product()
    taus_ciso = tauH_ciso.product()
    taus_puiso = tauH_puiso.product()
    vertices = vertexH.product()
    gvertices = filter(testGoodVertex, vertices)

    jets = jetH.product()

    for tau in taus:

        if tau.pt()==0: 
            h_isfail.Fill(1)
            continue
        else:
            h_isfail.Fill(0)

#        if tau.pt() < 20: continue
#        if abs(tau.eta()) > 2.3: continue
        
        bmjet, _dr_ = bestMatch(tau, jets)
#        print 'best match jet = ', bmjet.pt(), _dr_

        if bmjet == None:
            h_isjetfail.Fill(1)
            continue
        else:
            h_isjetfail.Fill(0)


        if bmjet.pt() < 20: continue
        if abs(bmjet.eta()) > 2.3: continue

        for itau in range(len(taus_disc)):
            if tau == taus_disc.key(itau).get():
                tau.ntotal = taus_disc.value(itau)
#                print '\t isolation official : Neutr = ', taus_disc.value(itau)

        for itau in range(len(taus_disc_weight)):
            if tau == taus_disc_weight.key(itau).get():
                tau.ntotal_weight = taus_disc_weight.value(itau)
#                print '\t isolation official, weighted : Neutr = ', taus_disc_weight.value(itau)

        for itau in range(len(taus_ciso)):
            if tau == taus_ciso.key(itau).get():
                tau.ciso = taus_ciso.value(itau)

        for itau in range(len(taus_puiso)):
            if tau == taus_puiso.key(itau).get():
                tau.puiso = taus_puiso.value(itau)


        #            if not (tau.decayMode() in [0,1,2,10]): continue
        #            if not (tau.decayMode() in [0]): continue
        #            if tau.decayMode() != 1: continue

#        print '\t Matched tau ******************************************'
#        print '\t reco. tau pT = ', tau.pt(), ', eta = ', tau.eta(), ', phi = ', tau.phi(), ', mass = ', tau.mass()
#        print '\t reco. tau decay mode = ', tau.decayMode()
#        print '\t reco. tau : Signal # of pi^+-', len(tau.signalPFChargedHadrCands())
#        print '\t reco. tau : Signal # of neutral', len(tau.signalPFNeutrHadrCands())
#        print '\t reco. tau : Signal # of strip', len(tau.signalPiZeroCandidates())
#        print '\t reco. tau : Signal # of PF gamma', len(tau.signalPFGammaCands())
#        print 
#        print '\t reco. tau : Iso # of pi^+-', len(tau.isolationPFChargedHadrCands()), 'iso = ', tau.isolationPFChargedHadrCandsPtSum()
#        print '\t reco. tau : Iso # of neutral', len(tau.isolationPFNeutrHadrCands()) 
#        print '\t reco. tau : Iso # of strip', len(tau.isolationPiZeroCandidates()) 
#        print '\t reco. tau : Iso # of PF gamma', len(tau.isolationPFGammaCands()), 'iso = ', tau.isolationPFGammaCandsEtSum()


        if tau.pt()==0:
            print 'Tau pT = 0 ... continue !'
            continue

        signalrad = 0.05

        if tau.pt()!=0:
            signalrad = max(0.05, min(0.1, 3./tau.pt()))

        sumpt_inside = 0
        sumpt_outside = 0
        sumpt_outside_weight1 = 0
        sumpt_outside_weight2 = 0
        sumpt_outside_weight3 = 0
        sumpt_iso_inside = 0
        sumpt_iso_outside = 0

        nphoton_inside = 0
        nphoton_outside = 0
        
        nphoton_iso_inside = 0
        nphoton_iso_outside = 0

        signal_photon = []
        iso_photon = []
        signal_dr_photon = []
        iso_dr_photon = []
        wsignal_photon = []
        wiso_photon = []

        for ii, iphoton in enumerate(tau.signalPFGammaCands()):

            if iphoton.pt() < 0.5: continue
            dr_fromtau = deltaR(tau.eta(), tau.phi(), iphoton.eta(), iphoton.phi())

 
            photon_pt[0] = iphoton.pt()
            photon_eta[0] = iphoton.eta()
            photon_phi[0] = iphoton.phi()
            photon_dr[0] = dr_fromtau
            photon_deta[0] = iphoton.eta() - tau.eta()
            photon_dphi[0] = deltaPhi(iphoton.phi(), tau.phi())
            photon_taupt[0] = tau.pt()
            photon_taueta[0] = tau.eta()
            photon_tauphi[0] = tau.phi()
            photon_isOutside[0] = (signalrad < dr_fromtau)
            photon_dm_rough[0] = returnRough(tau.decayMode())
            photon_dm[0] = tau.decayMode()
            photon_isIsolation[0] = 0
            photon_vertex[0] = len(vertices)
            photon_gvertex[0] = len(gvertices)
            photon_niso[0] = tau.ntotal_weight
            photon_tree.Fill()

            if signalrad < dr_fromtau:
                sumpt_outside += iphoton.pt()
                sumpt_outside_weight1 += iphoton.pt()*math.log(iphoton.pt()/dr_fromtau)
                sumpt_outside_weight2 += iphoton.pt()*(1/(dr_fromtau*dr_fromtau))
                sumpt_outside_weight3 += iphoton.pt()/dr_fromtau
                nphoton_outside += 1
            else:
                sumpt_inside += iphoton.pt()
                nphoton_inside += 1
                signal_photon.append(iphoton.pt())
                signal_dr_photon.append(dr_fromtau)
                wsignal_photon.append(dr_fromtau*iphoton.pt())
                
        for ii, iphoton in enumerate(tau.isolationPFGammaCands()):

            if iphoton.pt() < 0.5: continue
            dr_fromtau = deltaR(tau.eta(), tau.phi(), iphoton.eta(), iphoton.phi())

            photon_pt[0] = iphoton.pt()
            photon_eta[0] = iphoton.eta()
            photon_phi[0] = iphoton.phi()
            photon_dr[0] = dr_fromtau
            photon_deta[0] = iphoton.eta() - tau.eta()
            photon_dphi[0] = deltaPhi(iphoton.phi(), tau.phi())
            photon_isOutside[0] = (signalrad < dr_fromtau)
            photon_dm_rough[0] = returnRough(tau.decayMode())
            photon_dm[0] = tau.decayMode()
            photon_taupt[0] = tau.pt()
            photon_taueta[0] = tau.eta()
            photon_tauphi[0] = tau.phi()
            photon_isIsolation[0] = 1
            photon_vertex[0] = len(vertices)
            photon_gvertex[0] = len(gvertices)
            photon_niso[0] = tau.ntotal_weight
            photon_tree.Fill()

            iso_photon.append(iphoton.pt())
            iso_dr_photon.append(dr_fromtau)
            wiso_photon.append(dr_fromtau*iphoton.pt())

            if signalrad < dr_fromtau:
                sumpt_iso_outside += iphoton.pt()
                nphoton_iso_outside += 1
            else:
                sumpt_iso_inside += iphoton.pt()
                nphoton_iso_inside += 1


        if len(signal_photon)==0:
            tau_adR_signal[0] = -1
        else:
            tau_adR_signal[0] = sum(signal_dr_photon)/len(signal_photon)

        if sum(signal_photon)==0:
            tau_wdR_signal[0] = -1
        else:
            tau_wdR_signal[0] = sum(wsignal_photon)/sum(signal_photon)

        if len(iso_photon)==0:
            tau_adR_iso[0] = -1
        else:
            tau_adR_iso[0] = sum(iso_dr_photon)/len(iso_photon)

        if sum(iso_photon)==0:
            tau_wdR_iso[0] = -1
        else:
            tau_wdR_iso[0] = sum(wiso_photon)/sum(iso_photon)


        tau_id[0] = evtid
        tau_nphoton[0] = len(tau.isolationPFGammaCands())
        tau_nphoton_signal[0] = len(tau.signalPFGammaCands())
        tau_nisopizero[0] = len(tau.isolationPiZeroCandidates())
        tau_nsignalpizero[0] = len(tau.signalPiZeroCandidates())
        tau_dm[0] = tau.decayMode()
        tau_dm_rough[0] = returnRough(tau.decayMode())
        tau_niso[0] = tau.ntotal
        tau_niso_weighted[0] = tau.ntotal_weight
        tau_ciso[0] = tau.ciso
        tau_ciso_old[0] = tau.isolationPFChargedHadrCandsPtSum()
        tau_puiso[0] = tau.puiso

#        tau_ciso[0] = tau.isolationPFChargedHadrCandsPtSum()
        tau_pt[0] = tau.pt()
        tau_eta[0] = tau.eta()
        tau_phi[0] = tau.phi()
        tau_energy[0] = tau.energy()
        tau_mass[0] = tau.mass()
        tau_emFraction[0] = tau.emFraction()
        tau_nphoton_outside[0] = nphoton_outside
        tau_photonsumpt_outside[0] = sumpt_outside
        tau_photonsumpt_outside_weight1[0] = sumpt_outside_weight1
        tau_photonsumpt_outside_weight2[0] = sumpt_outside_weight2
        tau_photonsumpt_outside_weight3[0] = sumpt_outside_weight3
        tau_nphoton_inside[0] = nphoton_inside
        tau_nphoton_iso_inside[0] = nphoton_iso_inside
        tau_nphoton_iso_outside[0] = nphoton_iso_outside

        tau_photonsumpt_inside[0] = sumpt_inside
        tau_photonsumpt_iso_inside[0] = sumpt_iso_inside
        tau_photonsumpt_iso_outside[0] = sumpt_iso_outside

        tau_vertex[0] = len(vertices)
        tau_gvertex[0] = len(gvertices)

        if bmjet!=None:
            tau_corjetpt[0] = bmjet.pt()
            tau_corjeteta[0] = bmjet.eta()
            tau_corjetphi[0] = bmjet.phi()
        else:
            tau_corjetpt[0] = -99
            tau_corjeteta[0] = -99
            tau_corjetphi[0] = -99

       
        if not (sumpt_inside + sumpt_outside ==0):
            tau_photon_ratio[0] = sumpt_inside/(sumpt_inside + sumpt_outside)
        else:
            tau_photon_ratio[0] = -1.

        tau_tree.Fill()

        print 'eventid=',eid, 'tau pT, eta=', tau.pt(), tau.eta(), 'dm = ', tau.decayMode(), 'nweight=', tau.ntotal_weight, 'ciso', tau.ciso

        savedict = {'evt':eid, 'taupt':tau.pt(), 'taueta':tau.eta(), 'taudm':tau.decayMode(), 'nweight':tau.ntotal_weight, 'ciso':tau.ciso}
        key = 'dict_' + str(tau.pt()) + '_' + str(tau.eta()) + '_' + str(tau.phi())
        s[key] = savedict


    h_ntau.Fill(len(taus))


print evtid, 'events are processed !'

file.Write()
file.Close()

