import ROOT, os, math, shelve, sys
import numpy as num
from DataFormats.FWLite import Events, Handle
from Display import *
from DeltaR import *


ROOT.gROOT.SetBatch(True)

tauH = Handle('std::vector<reco::PFTau>')
tauH_disc = Handle('reco::PFTauDiscriminator')
tauH_disc_weight = Handle('reco::PFTauDiscriminator')
tauH_ciso = Handle('reco::PFTauDiscriminator')
tauH_puiso = Handle('reco::PFTauDiscriminator')
vertexH = Handle('std::vector<reco::Vertex>')
genParticlesH  = Handle ('std::vector<reco::GenParticle>')

filelist = []
argvs = sys.argv
argc = len(argvs)

if argc != 2:
    print 'Please specify the runtype : python runTauDisplay.py <dynamic90, dynamic95, run1, standard>'
    sys.exit(0)

#runtype = 'dynamic90'
#runtype = 'dynamic95'
#runtype = 'run1'
#runtype = 'standard'

runtype = argvs[1]

print 'You selected', runtype

#s = shelve.open('save_' + runtype + '.db')

def isFinal(p):
    return not (p.numberOfDaughters() == 1 and p.daughter(0).pdgId() == p.pdgId())

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


#for ii in range(1, 40):
for ii in range(1, 30):

    filename = ''
    
    if runtype == 'standard':
        filename = 'root://eoscms//eos/cms/store/cmst3/user/ytakahas/CMG/VBF_HToTauTau_M-125_13TeV-powheg-pythia6/Phys14DR-PU20bx25_tsg_PHYS14_25_V1-v2/AODSIM/Run1_noptcut_20150505/aod_' + str(ii) + '.root'
    elif runtype == 'dynamic90':
        filename = 'root://eoscms//eos/cms/store/cmst3/user/ytakahas/CMG/VBF_HToTauTau_M-125_13TeV-powheg-pythia6/Phys14DR-PU20bx25_tsg_PHYS14_25_V1-v2/AODSIM/Dynamic90_20150501/aod_' + str(ii) + '.root'
    elif runtype == 'dynamic95':
        filename = 'root://eoscms//eos/cms/store/cmst3/user/ytakahas/CMG/VBF_HToTauTau_M-125_13TeV-powheg-pythia6/Phys14DR-PU20bx25_tsg_PHYS14_25_V1-v2/AODSIM/Dynamic95_20150505/aod_' + str(ii) + '.root'
    elif runtype == 'run1':
        filename = 'root://eoscms//eos/cms/store/cmst3/user/ytakahas/CMG/VBF_HToTauTau_M-125_13TeV-powheg-pythia6/Phys14DR-PU20bx25_tsg_PHYS14_25_V1-v2/AODSIM/Run1Default/aod_' + str(ii) + '.root'
    elif runtype == 'taugun':
        filename = '/afs/cern.ch/user/y/ytakahas/work/TauIsolation_dynamic2/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_noptcut/job_' + str(ii) + '/step.root'
    elif runtype == 'mssm':
        filename = 'root://eoscms//eos/cms/store/cmst3/user/ytakahas/CMG/ZprimeToTauTau_M-1000_Tune4C_13TeV-pythia8/Phys14DR-PU20bx25_tsg_PHYS14_25_V1-v1/AODSIM/Dynamic95_20150505/aod_' + str(ii) + '.root'


    print filename
    filelist.append(filename)

events = Events(filelist)
print len(filelist), 'files will be analyzed'


outputname = 'Myroot_' + runtype + '_v2.root'
file = ROOT.TFile(outputname, 'recreate')

h_ngen = ROOT.TH1F("h_ngen", "h_ngen",10,0,10)
h_ngenmatch = ROOT.TH1F("h_ngenmatch", "h_ngenmatch",5,0,5)

tau_tree = ROOT.TTree('per_tau','per_tau')
photon_tree = ROOT.TTree('per_photon','per_photon')

tau_eventid = num.zeros(1, dtype=int)
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
tau_gendm = num.zeros(1, dtype=int)
tau_gendm_rough = num.zeros(1, dtype=int)
tau_genptorig = num.zeros(1, dtype=float)
tau_genpt = num.zeros(1, dtype=float)
tau_geneta = num.zeros(1, dtype=float)
tau_genphi = num.zeros(1, dtype=float)
tau_gen_nphoton = num.zeros(1, dtype=int)
tau_gen_npion = num.zeros(1, dtype=int)
tau_gen_nphoton_outside = num.zeros(1, dtype=int)
tau_gen_nphoton_inside = num.zeros(1, dtype=int)
tau_gen_sumpt_outside = num.zeros(1, dtype=float)
tau_gen_sumpt_inside = num.zeros(1, dtype=float)
tau_vertex = num.zeros(1, dtype=int)
tau_gvertex = num.zeros(1, dtype=int)

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



tau_tree.Branch('tau_id', tau_id, 'tau_id/I')
tau_tree.Branch('tau_vertex', tau_vertex, 'tau_vertex/I')
tau_tree.Branch('tau_gvertex', tau_gvertex, 'tau_gvertex/I')
tau_tree.Branch('tau_eventid', tau_eventid, 'tau_eventid/I')
tau_tree.Branch('tau_nphoton', tau_nphoton, 'tau_nphoton/I')
tau_tree.Branch('tau_nphoton_signal', tau_nphoton_signal, 'tau_nphoton_signal/I')
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
tau_tree.Branch('tau_gendm', tau_gendm, 'tau_gendm/I')
tau_tree.Branch('tau_gendm_rough', tau_gendm_rough, 'tau_gendm_rough/I')
tau_tree.Branch('tau_genptorig', tau_genptorig, 'tau_genptorig/D')
tau_tree.Branch('tau_genpt', tau_genpt, 'tau_genpt/D')
tau_tree.Branch('tau_geneta', tau_geneta, 'tau_geneta/D')
tau_tree.Branch('tau_genphi', tau_genphi, 'tau_genphi/D')
tau_tree.Branch('tau_gen_nphoton', tau_gen_nphoton, 'tau_gen_nphoton/I')
tau_tree.Branch('tau_gen_npion', tau_gen_npion, 'tau_gen_npion/I')
tau_tree.Branch('tau_gen_nphoton_outside', tau_gen_nphoton_outside, 'tau_gen_nphoton_outside/I')
tau_tree.Branch('tau_gen_nphoton_inside', tau_gen_nphoton_inside, 'tau_gen_nphoton_inside/I')
tau_tree.Branch('tau_gen_sumpt_outside', tau_gen_sumpt_outside, 'tau_gen_sumpt_outside/D')
tau_tree.Branch('tau_gen_sumpt_inside', tau_gen_sumpt_inside, 'tau_gen_sumpt_inside/D')


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


evtid = 0

for event in events:
    
    evtid += 1  
    eid = event.eventAuxiliary().id().event()
    
    if evtid%1000 == 0:
        print 'Event ', evtid, 'processed'

    if evtid==50000:
#    if evtid==2000:
        break

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

    event.getByLabel('genParticles',genParticlesH)
    genParticles = genParticlesH.product()
    genTaus = [p for p in genParticles if abs(p.pdgId()) == 15 and isFinal(p) and p.status()==2]

    
    # count # of generated taus
    counter = 0
    for genParticle in genTaus:
        if (genParticle.numberOfDaughters()==2 and abs(genParticle.daughter(0).pdgId())==15 and genParticle.daughter(1).pdgId()==22):
            continue
        counter += 1

    h_ngen.Fill(counter)

    for tau in taus:
        
        if tau.pt() < 20: continue
        if abs(tau.eta()) > 2.3: continue
        
        _genparticle_ = []
        signalrad = max(0.05, min(0.1, 3./tau.pt()))

        for genParticle in genTaus:
                        
#            while (genParticle.numberOfDaughters()==2 and abs(genParticle.daughter(0).pdgId())==15 and genParticle.daughter(1).pdgId()==22):
#                genParticle = genParticle.daughter(0)

            if (genParticle.numberOfDaughters()==2 and abs(genParticle.daughter(0).pdgId())==15 and genParticle.daughter(1).pdgId()==22):
                continue
             
            finDaughters = finalDaughters(genParticle, [])
            genParticle.genPt = genParticle.pt()

            genParticle.genVisP4 = p4sumvis(finDaughters)
            genParticle.genVis = p4sumvis2(finDaughters)


#            print 'wrong : pt,eta,phi = ', genParticle.genVisP4.pt(), genParticle.genVisP4.eta(), genParticle.genVisP4.phi()
#            print 'ok : pt,eta,phi = ', genParticle.genVis.Pt(), genParticle.genVis.Eta(), genParticle.genVis.Phi()


            gen_dm, gen_dmid, nphoton, npion, _photon_ = returnGenDecayMode(finDaughters)

            if gen_dm=='muon' or gen_dm=='electron': 
#                print '\t\t judged as', gen_dm, 'decaymode --> continued'
                continue

#            if genParticle.pt() < genParticle.genVis.Pt():
#                print 'This is not possible !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!', genParticle.pt(), genParticle.genVis.Pt()

            genParticle.decaymode = gen_dmid
            genParticle.nphoton = nphoton
            genParticle.npion = npion
            
#            if abs(genParticle.genVisP4.eta()) > 2.3: continue
#            if genParticle.genVisP4.pt() < 20: continue
            if abs(genParticle.genVis.Eta()) > 2.3: continue
            if genParticle.genVis.Pt() < 20: continue

            dr = deltaR(tau.eta(), tau.phi(), genParticle.genVis.Eta(), genParticle.genVis.Phi())

            _sumpt_inside = 0
            _sumpt_outside = 0
            
            _nphoton_inside = 0
            _nphoton_outside = 0

            for iphoton in _photon_:
                dr_photon = deltaR(tau.eta(), tau.phi(), iphoton.eta(), iphoton.phi())

                if signalrad < dr_photon:
                    _sumpt_outside += iphoton.pt()
                    _nphoton_outside += 1
                else:
                    _sumpt_inside += iphoton.pt()
                    _nphoton_inside += 1

            genParticle.nphoton_inside = _nphoton_inside
            genParticle.nphoton_outside = _nphoton_outside
            genParticle.sumpt_inside = _sumpt_inside
            genParticle.sumpt_outside = _sumpt_outside

            
            if dr < 0.5:
                _genparticle_.append(genParticle)



        h_ngenmatch.Fill(len(_genparticle_))

        if len(_genparticle_) != 1:
            continue

        gp = _genparticle_[0]

#        print 'reconstructed tau pT =', tau.pt(), ' eta =', tau.eta()
#        print '\t genparticle : status = ', gp.status()
#        for ii in range(gp.numberOfDaughters()):
#            print '\t -> pdgId = ', gp.daughter(ii).pdgId(), 'status = ', gp.daughter(ii).status(), 'decaymode = ', gp.decaymode, 'tau pT = ', gp.genPt, 'vis pT = ', gp.genVisP4.pt()


        for itau in range(len(taus_disc)):
            if tau == taus_disc.key(itau).get():
                tau.ntotal = taus_disc.value(itau)

        for itau in range(len(taus_disc_weight)):
            if tau == taus_disc_weight.key(itau).get():
                tau.ntotal_weight = taus_disc_weight.value(itau)

        for itau in range(len(taus_ciso)):
            if tau == taus_ciso.key(itau).get():
                tau.ciso = taus_ciso.value(itau)

        for itau in range(len(taus_puiso)):
            if tau == taus_puiso.key(itau).get():
                tau.puiso = taus_puiso.value(itau)


        #            if not (tau.decayMode() in [0,1,2,10]): continue
        #            if not (tau.decayMode() in [0]): continue
        #            if tau.decayMode() != 1: continue




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
            photon_vertex[0] = len(vertices)
            photon_gvertex[0] = len(gvertices)
            photon_isIsolation[0] = 0



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
            photon_tree.Fill()

            if signalrad < dr_fromtau:
                sumpt_iso_outside += iphoton.pt()
                nphoton_iso_outside += 1
            else:
                sumpt_iso_inside += iphoton.pt()
                nphoton_iso_inside += 1



        tau_id[0] = evtid
        tau_eventid[0] = eid
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

        tau_gendm[0] = gp.decaymode
        tau_gendm_rough[0] = returnRough(gp.decaymode)
        tau_genptorig[0] = gp.genPt
        tau_genpt[0] = gp.genVis.Pt()
        tau_geneta[0] = gp.genVis.Eta()
        tau_genphi[0] = gp.genVis.Phi()
        tau_gen_nphoton[0] = gp.nphoton
        tau_gen_npion[0] = gp.npion

        tau_gen_nphoton_outside[0] = gp.nphoton_outside
        tau_gen_nphoton_inside[0] = gp.nphoton_inside
        tau_gen_sumpt_outside[0] = gp.sumpt_outside
        tau_gen_sumpt_inside[0] = gp.sumpt_inside

        if not (sumpt_inside + sumpt_outside ==0):
            tau_photon_ratio[0] = sumpt_inside/(sumpt_inside + sumpt_outside)
        else:
            tau_photon_ratio[0] = -1.

        tau_tree.Fill()

#        savedict = {'evt':eid, 'taupt':tau.pt(), 'taueta':tau.eta(), 'tauphi':tau.phi(), 'taudm':tau.decayMode(), 'neutral':tau.ntotal, 'nweight':tau.ntotal_weight, 'ciso':tau.isolationPFChargedHadrCandsPtSum()}
#        key = 'dict_' + str(gp.genVis.Pt()) + '_' + str(gp.genVis.Eta()) + '_' + str(gp.genVis.Phi())
#        s[key] = savedict

print evtid, 'events are processed !'

#s.close()

file.Write()
file.Close()

