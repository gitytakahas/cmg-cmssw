import ROOT
import os
import numpy as num
from DataFormats.FWLite import Events, Handle
from Display import *

ROOT.gROOT.SetBatch(True)

vertex  = Handle('std::vector<reco::Vertex>')
ecalH  = Handle ('std::vector<reco::PFRecHit>')
hcalH  = Handle ('std::vector<reco::PFRecHit>')
genParticlesH  = Handle ('std::vector<reco::GenParticle>')
ecalClustersH  = Handle ('std::vector<reco::PFCluster>')
hcalClustersH  = Handle ('std::vector<reco::PFCluster>')
tauH = Handle('std::vector<reco::PFTau>')
tauH_disc = Handle('reco::PFTauDiscriminator')


filelist = []

#for ii in range(250):
for ii in range(20):
#    if ii in [130]: continue
#for ii in range(20):
#    filename = '/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150218_only1Prong/job_' + str(ii) + '/step.root'
    filename = '/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/TauGun_20150225_allHadronicDecay/job_' + str(ii) + '/step.root'

    if os.path.exists(filename):
        filelist.append(filename)
        print 'added : ', filename
    else:
        print 'No file found : ', filename


print len(filelist), 'files will be analyzed'
events = Events(filelist)
#events = Events('/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/Production/step.root')

file = ROOT.TFile('Myroot.root', 'recreate')
event_tree = ROOT.TTree('event_tree','event_tree')
photon_tree = ROOT.TTree('per_photon','per_photon')
tau_tree = ROOT.TTree('per_tau','per_tau')
pizero_tree = ROOT.TTree('per_pizero','per_pizero')
    
tau_id = num.zeros(1, dtype=int)
tau_z = num.zeros(1, dtype=float)
tau_pvz = num.zeros(1, dtype=float)
tau_nphoton = num.zeros(1, dtype=int)
tau_nisopizero = num.zeros(1, dtype=int)
tau_nsignalpizero = num.zeros(1, dtype=int)
tau_dm = num.zeros(1, dtype=int)
tau_dm_rough = num.zeros(1, dtype=int)
tau_gen_nphoton = num.zeros(1, dtype=int)
tau_gen_nphoton_inc = num.zeros(1, dtype=int)
tau_gen_npion = num.zeros(1, dtype=int)
tau_total_pt = num.zeros(1, dtype=float)
tau_gendm = num.zeros(1, dtype=int)
tau_gendm_rough = num.zeros(1, dtype=int)
tau_genpt = num.zeros(1, dtype=float)
tau_geneta = num.zeros(1, dtype=float)
tau_genphi = num.zeros(1, dtype=float)
tau_genenergy = num.zeros(1, dtype=float)
tau_genmass = num.zeros(1, dtype=float)
tau_pt = num.zeros(1, dtype=float)
tau_eta = num.zeros(1, dtype=float)
tau_phi = num.zeros(1, dtype=float)
tau_energy = num.zeros(1, dtype=float)
tau_mass = num.zeros(1, dtype=float)
tau_emFraction = num.zeros(1, dtype=float)
tau_ecalStripSumEOverPLead = num.zeros(1, dtype=float)
tau_maximumHCALPFClusterEt = num.zeros(1, dtype=float)

photon_id = num.zeros(1, dtype=int)
photon_gendm = num.zeros(1, dtype=int)
photon_gendm_rough = num.zeros(1, dtype=int)
photon_gen_nphoton = num.zeros(1, dtype=int)
photon_gen_npion = num.zeros(1, dtype=int)
photon_genpt = num.zeros(1, dtype=float)
photon_geneta = num.zeros(1, dtype=float)
photon_genphi = num.zeros(1, dtype=float)
photon_genenergy = num.zeros(1, dtype=float)
photon_genmass = num.zeros(1, dtype=float)
photon_tau_pt = num.zeros(1, dtype=float)
photon_tau_eta = num.zeros(1, dtype=float)
photon_tau_phi = num.zeros(1, dtype=float)
photon_tau_energy = num.zeros(1, dtype=float)
photon_tau_emFraction = num.zeros(1, dtype=float)
photon_tau_ecalStripSumEOverPLead = num.zeros(1, dtype=float)
photon_tau_mass = num.zeros(1, dtype=float)
photon_dm = num.zeros(1, dtype=int)
photon_dm_rough = num.zeros(1, dtype=int)
photon_pt = num.zeros(1, dtype=float)
photon_dr = num.zeros(1, dtype=float)
photon_deta = num.zeros(1, dtype=float)
photon_dphi = num.zeros(1, dtype=float)
photon_tau_maximumHCALPFClusterEt = num.zeros(1, dtype=float)

pizero_pt = num.zeros(1, dtype=float)
pizero_eta = num.zeros(1, dtype=float)
pizero_phi = num.zeros(1, dtype=float)
pizero_mass = num.zeros(1, dtype=float)
pizero_energy = num.zeros(1, dtype=float)
pizero_invmass = num.zeros(1, dtype=float)
pizero_invpt = num.zeros(1, dtype=float)
pizero_isSignal = num.zeros(1, dtype=int)
pizero_dm = num.zeros(1, dtype=int)
pizero_gendm = num.zeros(1, dtype=int)
pizero_n = num.zeros(1, dtype=int)
pizero_id = num.zeros(1, dtype=int)

event_ntau = num.zeros(1, dtype=int)
event_ngentau = num.zeros(1, dtype=int)
event_gentaupt = num.zeros(1, dtype=float)
event_gentaueta = num.zeros(1, dtype=float)
event_gendm = num.zeros(1, dtype=int)

event_tree.Branch('event_ntau', event_ntau, 'event_ntau/I')
event_tree.Branch('event_ngentau', event_ngentau, 'event_ngentau/I')
event_tree.Branch('event_gentaupt', event_gentaupt, 'event_gentaupt/D')
event_tree.Branch('event_gentaueta', event_gentaueta, 'event_gentaueta/D')
event_tree.Branch('event_gendm', event_gendm, 'event_gendm/I')

tau_tree.Branch('tau_id', tau_id, 'tau_id/I')
tau_tree.Branch('tau_nphoton', tau_nphoton, 'tau_nphoton/I')
tau_tree.Branch('tau_nisopizero', tau_nisopizero, 'tau_nisopizero/I')
tau_tree.Branch('tau_nsignalpizero', tau_nsignalpizero, 'tau_nsignalpizero/I')
tau_tree.Branch('tau_total_pt', tau_total_pt, 'tau_total_pt/D')
tau_tree.Branch('tau_dm', tau_dm, 'tau_dm/I')
tau_tree.Branch('tau_dm_rough', tau_dm_rough, 'tau_dm_rough/I')
tau_tree.Branch('tau_gen_nphoton', tau_gen_nphoton, 'tau_gen_nphoton/I')
tau_tree.Branch('tau_gen_nphoton_inc', tau_gen_nphoton_inc, 'tau_gen_nphoton_inc/I')
tau_tree.Branch('tau_gen_npion', tau_gen_npion, 'tau_gen_npion/I')
tau_tree.Branch('tau_gendm', tau_gendm, 'tau_gendm/I')
tau_tree.Branch('tau_gendm_rough', tau_gendm_rough, 'tau_gendm_rough/I')
tau_tree.Branch('tau_genpt', tau_genpt, 'tau_genpt/D')
tau_tree.Branch('tau_geneta', tau_geneta, 'tau_geneta/D')
tau_tree.Branch('tau_genphi', tau_genphi, 'tau_genphi/D')
tau_tree.Branch('tau_pt', tau_pt, 'tau_pt/D')
tau_tree.Branch('tau_eta', tau_eta, 'tau_eta/D')
tau_tree.Branch('tau_phi', tau_phi, 'tau_phi/D')
tau_tree.Branch('tau_z', tau_z, 'tau_z/D')
tau_tree.Branch('tau_pvz', tau_pvz, 'tau_pvz/D')
tau_tree.Branch('tau_energy', tau_energy, 'tau_energy/D')
tau_tree.Branch('tau_mass', tau_mass, 'tau_mass/D')
tau_tree.Branch('tau_emFraction', tau_emFraction, 'tau_emFraction/D')
tau_tree.Branch('tau_ecalStripSumEOverPLead', tau_ecalStripSumEOverPLead, 'tau_ecalStripSumEOverPLead/D')
tau_tree.Branch('tau_maximumHCALPFClusterEt', tau_maximumHCALPFClusterEt, 'tau_maximumHCALPFClusterEt/D')
tau_tree.Branch('tau_genenergy', tau_genenergy, 'tau_genenergy/D')
tau_tree.Branch('tau_genmass', tau_genmass, 'tau_genmass/D')


photon_tree.Branch('photon_id', photon_id, 'photon_id/I')
photon_tree.Branch('photon_gendm', photon_gendm, 'photon_gendm/I')
photon_tree.Branch('photon_gendm_rough', photon_gendm_rough, 'photon_gendm_rough/I')
photon_tree.Branch('photon_gen_nphoton', photon_gen_nphoton, 'photon_gen_nphoton/I')
photon_tree.Branch('photon_gen_npion', photon_gen_npion, 'photon_gen_npion/I')
photon_tree.Branch('photon_genpt', photon_genpt, 'photon_genpt/D')
photon_tree.Branch('photon_geneta', photon_geneta, 'photon_geneta/D')
photon_tree.Branch('photon_genphi', photon_genphi, 'photon_genphi/D')
photon_tree.Branch('photon_genenergy', photon_genenergy, 'photon_genenergy/D')
photon_tree.Branch('photon_genmass', photon_genmass, 'photon_genmass/D')
photon_tree.Branch('photon_tau_pt', photon_tau_pt, 'photon_tau_pt/D')
photon_tree.Branch('photon_tau_eta', photon_tau_eta, 'photon_tau_eta/D')
photon_tree.Branch('photon_tau_phi', photon_tau_phi, 'photon_tau_phi/D')
photon_tree.Branch('photon_dm', photon_dm, 'photon_dm/I')
photon_tree.Branch('photon_dm_rough', photon_dm_rough, 'photon_dm_rough/I')
photon_tree.Branch('photon_pt', photon_pt, 'photon_pt/D')
photon_tree.Branch('photon_dr', photon_dr, 'photon_dr/D')
photon_tree.Branch('photon_deta', photon_deta, 'photon_deta/D')
photon_tree.Branch('photon_dphi', photon_dphi, 'photon_dphi/D')
photon_tree.Branch('photon_tau_energy', photon_tau_energy, 'photon_tau_energy/D')
photon_tree.Branch('photon_tau_mass', photon_tau_mass, 'photon_tau_mass/D')
photon_tree.Branch('photon_tau_emFraction', photon_tau_emFraction, 'photon_tau_emFraction/D')
photon_tree.Branch('photon_tau_ecalStripSumEOverPLead', photon_tau_ecalStripSumEOverPLead, 'photon_tau_ecalStripSumEOverPLead/D')
photon_tree.Branch('photon_tau_maximumHCALPFClusterEt', photon_tau_maximumHCALPFClusterEt, 'photon_tau_maximumHCALPFClusterEt/D')

pizero_tree.Branch('pizero_pt', pizero_pt, 'pizero_pt/D')
pizero_tree.Branch('pizero_eta', pizero_eta, 'pizero_eta/D')
pizero_tree.Branch('pizero_phi', pizero_phi, 'pizero_phi/D')
pizero_tree.Branch('pizero_mass', pizero_mass, 'pizero_mass/D')
pizero_tree.Branch('pizero_energy', pizero_energy, 'pizero_energy/D')
pizero_tree.Branch('pizero_invmass', pizero_invmass, 'pizero_invmass/D')
pizero_tree.Branch('pizero_invpt', pizero_invpt, 'pizero_invpt/D')
pizero_tree.Branch('pizero_isSignal', pizero_isSignal, 'pizero_isSignal/I')
pizero_tree.Branch('pizero_dm', pizero_dm, 'pizero_dm/I')
pizero_tree.Branch('pizero_gendm', pizero_gendm, 'pizero_gendm/I')
pizero_tree.Branch('pizero_n', pizero_n, 'pizero_n/I')
pizero_tree.Branch('pizero_id', pizero_id, 'pizero_id/I')



counter = 0
evtid = 0

for event in events:
    
    evtid += 1  

#    if evtid > 1000: break

    print '-'*80
    print 'Event ', evtid
    print '-'*80

    event.getByLabel('offlinePrimaryVertices',vertex)
    event.getByLabel('particleFlowRecHitECAL',ecalH)
    event.getByLabel('particleFlowRecHitHBHE',hcalH)
    event.getByLabel('genParticles',genParticlesH)
    event.getByLabel('particleFlowClusterECAL',ecalClustersH)
    event.getByLabel('particleFlowClusterHBHE', hcalClustersH)
    event.getByLabel("hpsPFTauProducer", tauH)
    event.getByLabel("hpsPFTauMVA3IsolationNeutralIsoPtSum", tauH_disc)

    vtx = vertex.product()   
    ecal = ecalH.product()
    hcal = hcalH.product()
    genParticles = genParticlesH.product()
    ecalClusters = ecalClustersH.product()
    hcalClusters = hcalClustersH.product()

    taus = tauH.product()
    taus_disc = tauH_disc.product()
    
    genTaus = [p for p in genParticles if abs(p.pdgId()) == 15]
    genPhotons = [p for p in genParticles if abs(p.pdgId()) == 22]

    _gen_pt = -1
    _gen_eta = -1
    _gen_dm = -1

    for genParticle in genTaus:

        finDaughters = finalDaughters(genParticle, [])
        genParticle.genVisP4 = p4sumvis(finDaughters)
#        import pdb; pdb.set_trace()

        _gen_pt = genParticle.genVisP4.pt()
        _gen_eta = genParticle.genVisP4.eta()

        gen_dm, gen_dmid, nphoton, npion = returnGenDecayMode(finDaughters)
        recoTau = []

        displayECAL = DisplayManager('ECAL', genParticle.eta(), genParticle.phi(), 0.6)
#        displayHCAL = DisplayManager('HCAL', genParticle.eta(), genParticle.phi(), 0.6)


        if abs(genParticle.genVisP4.eta()) > 2.3: continue
        if genParticle.genVisP4.pt() < 20: continue

        _gen_dm = gen_dmid
        if not (gen_dmid in [0,1,2,10]):
#        if not (gen_dmid in [1]): 
            print 'GG : Gen decay mode', gen_dmid
            continue

        print '* Generated tau info *************************************'
        print '# of charged pions', npion
        print '# of photons', nphoton, '\n'
        print 'gen tau pT = ', genTaus[0].pt(), gen_dm

        if len(taus) ==0:
            print 'CC : There is no reconstructed taus in the events !'
            continue
            
        if len(taus) !=1:
            print 'XX : len(tau)', len(taus)
            
        for tau in taus:

#            import pdb; pdb.set_trace()

            if tau.pt() < 20: continue
            if abs(tau.eta()) > 2.3: continue

            if not deltaR(tau.eta(), tau.phi(), genParticle.genVisP4.eta(), genParticle.genVisP4.phi()) < 0.5:
                print 'YY : dR matching failed !', deltaR(tau.eta(), tau.phi(), genParticle.genVisP4.eta(), genParticle.genVisP4.phi())
                continue


            for itau in range(len(taus_disc)):
                if tau == taus_disc.key(itau).get():
                    tau.ntotal = taus_disc.value(itau)
                    print '\t isolation official : Neutr = ', taus_disc.value(itau)

#            if not (tau.decayMode() in [0,1,2,10]): continue
#            if not (tau.decayMode() in [0]): continue

            print '\t Matched tau ******************************************'
            print '\t reco. tau pT = ', tau.pt(), ', eta = ', tau.eta(), ', phi = ', tau.phi(), ', mass = ', tau.mass()
            print '\t reco. tau decay mode = ', tau.decayMode(), dmname(tau.decayMode())
            print '\t reco. tau : Signal # of pi^+-', len(tau.signalPFChargedHadrCands())
            print '\t reco. tau : Signal # of neutral', len(tau.signalPFNeutrHadrCands())
            print '\t reco. tau : Signal # of strip', len(tau.signalPiZeroCandidates())
            print '\t reco. tau : Signal # of PF gamma', len(tau.signalPFGammaCands())
            print 
            print '\t reco. tau : Iso # of pi^+-', len(tau.isolationPFChargedHadrCands()), 'iso = ', tau.isolationPFChargedHadrCandsPtSum()
            print '\t reco. tau : Iso # of neutral', len(tau.isolationPFNeutrHadrCands()) 
            print '\t reco. tau : Iso # of strip', len(tau.isolationPiZeroCandidates()) 
            print '\t reco. tau : Iso # of PF gamma', len(tau.isolationPFGammaCands()), 'iso = ', tau.isolationPFGammaCandsEtSum()


            for istrip in tau.isolationPiZeroCandidates():
                pizero_pt[0] = istrip.pt()
                pizero_eta[0] = istrip.eta()
                pizero_phi[0] = istrip.phi()
                pizero_mass[0] = istrip.mass()
                pizero_energy[0] = istrip.energy()
                pizero_invmass[0] = (istrip.p4() + tau.p4()).mass()
                pizero_invpt[0] = (istrip.p4() + tau.p4()).pt()
                pizero_isSignal[0] = 0
                pizero_dm[0] = tau.decayMode()
                pizero_gendm[0] = gen_dmid
                pizero_n[0] = len(tau.isolationPiZeroCandidates())
                pizero_id[0] = evtid
                pizero_tree.Fill()

            for istrip in tau.signalPiZeroCandidates():
                pizero_pt[0] = istrip.pt()
                pizero_eta[0] = istrip.eta()
                pizero_phi[0] = istrip.phi()
                pizero_mass[0] = istrip.mass()
                pizero_energy[0] = istrip.energy()
                pizero_invmass[0] = (istrip.p4() + tau.p4()).mass()
                pizero_invpt[0] = (istrip.p4() + tau.p4()).pt()
                pizero_isSignal[0] = 1
                pizero_dm[0] = tau.decayMode()
                pizero_gendm[0] = gen_dmid
                pizero_n[0] = len(tau.signalPiZeroCandidates())
                pizero_id[0] = evtid
                pizero_tree.Fill()

            for iphoton in tau.signalPFGammaCands():
                print '\t\t signal photon pT = ', iphoton.pt(), ', eta = ', iphoton.eta(), ', phi = ', iphoton.phi()
                displayECAL.addPhoton(iphoton, 1)
                    
            for iphoton in tau.isolationPFGammaCands():
                print '\t\t iso. photon pT = ', iphoton.pt(), ', eta = ', iphoton.eta(), ', phi = ', iphoton.phi()
                displayECAL.addPhoton(iphoton,2)

                photon_id[0] = evtid
                photon_gendm[0] = gen_dmid
                photon_gendm_rough[0] = returnRough(gen_dmid)
                photon_gen_nphoton[0] = nphoton
                photon_gen_npion[0] = npion
                photon_genpt[0] = genParticle.genVisP4.pt()
                photon_geneta[0] = genParticle.genVisP4.eta()
                photon_genphi[0] = genParticle.genVisP4.phi()
                photon_genenergy[0] = genParticle.genVisP4.energy()
                photon_genmass[0] = genParticle.genVisP4.mass()
                photon_tau_pt[0] = tau.pt()
                photon_tau_eta[0] = tau.eta()
                photon_tau_phi[0] = tau.phi()
                photon_dm[0] = tau.decayMode()
                photon_dm_rough[0] = returnRough(tau.decayMode())
                photon_pt[0] = iphoton.pt()
                photon_dr[0] = deltaR(tau.eta(), tau.phi(), iphoton.eta(), iphoton.phi())
                photon_deta[0] = tau.eta() - iphoton.eta()
                photon_dphi[0] = deltaPhi(tau.phi(), iphoton.phi())
                photon_tau_ecalStripSumEOverPLead[0] = tau.ecalStripSumEOverPLead()
                photon_tau_energy[0] = tau.energy()
                photon_tau_mass[0] = tau.mass()
                photon_tau_emFraction[0] = tau.emFraction()
                photon_tau_maximumHCALPFClusterEt[0] = tau.maximumHCALPFClusterEt()
                photon_tree.Fill()


            for ich in tau.signalPFChargedHadrCands():
#                print '\t\t signal charged pT = ', ich.pt(), ' eta = ', ich.eta(), ' phi = ', ich.phi()
                displayECAL.addCH(ich, 1)
#                displayHCAL.addCH(ich, 1)
                    
            for ich in tau.isolationPFChargedHadrCands():
                print '\t\t iso. charged pT = ', ich.pt(), ' eta = ', ich.eta(), ' phi = ', ich.phi()
                displayECAL.addCH(ich, 2)
#                displayHCAL.addCH(ich, 1)

 #           for ich in tau.signalPFNeutrHadrCands():
 #               print '\t\t signal neutral pT = ', ich.pt(), ' eta = ', ich.eta(), ' phi = ', ich.phi()
 #               displayECAL.addCH(ich, 3)
                    
#            for ich in tau.isolationPFNeutrHadrCands():
#                print '\t\t iso. neutral pT = ', ich.pt(), ' eta = ', ich.eta(), ' phi = ', ich.phi()
#                displayECAL.addCH(ich, 4)

            recoTau.append(tau)


        
        if len(recoTau)!=1: 
            print 'ZZ : recoTau is not one !', len(recoTau)
            continue

        if recoTau[0].ntotal!=0:
            print "Interesting events ! ", evtid

        tau_id[0] = evtid
        tau_z[0] = recoTau[0].vertex().z()
        tau_pvz[0] = vtx[0].z()
        tau_nphoton[0] = len(recoTau[0].isolationPFGammaCands())
        tau_nisopizero[0] = len(recoTau[0].isolationPiZeroCandidates())
        tau_nsignalpizero[0] = len(recoTau[0].signalPiZeroCandidates())
        tau_dm[0] = recoTau[0].decayMode()
        tau_dm_rough[0] = returnRough(recoTau[0].decayMode())
        tau_gen_nphoton[0] = nphoton
        tau_gen_nphoton_inc[0] = len(genPhotons)
        tau_gen_npion[0] = npion
        tau_total_pt[0] = recoTau[0].ntotal
        tau_gendm[0] = gen_dmid
        tau_gendm_rough[0] = returnRough(gen_dmid)
        tau_genpt[0] = genParticle.genVisP4.pt()
        tau_geneta[0] = genParticle.genVisP4.eta()
        tau_genphi[0] = genParticle.genVisP4.phi()
        tau_pt[0] = recoTau[0].pt()
        tau_eta[0] = recoTau[0].eta()
        tau_phi[0] = recoTau[0].phi()
        tau_energy[0] = recoTau[0].energy()
        tau_mass[0] = recoTau[0].mass()
        tau_emFraction[0] = recoTau[0].emFraction()
        tau_ecalStripSumEOverPLead[0] = recoTau[0].ecalStripSumEOverPLead()
        tau_maximumHCALPFClusterEt[0] = recoTau[0].maximumHCALPFClusterEt()

        tau_genenergy[0] = genParticle.genVisP4.energy()
        tau_genmass[0] = genParticle.genVisP4.mass()
        tau_tree.Fill()

        displayECAL.addRecoTau(recoTau[0])
#        displayHCAL.addRecoTau(recoTau[0])

        #reloop on gen particles and add them in view
        for genP in genParticles:
            if genP.status()!=1 or abs(genP.pdgId()) in [12, 14, 16]:
                continue

            displayECAL.addGenParticle(genP) 
#            displayHCAL.addGenParticle(genP) 
        

        #add ECAL hits    
        for hit in ecal:
            displayECAL.addRecHit(hit,1)

        for cluster in ecalClusters:
            displayECAL.addCluster(cluster, links=True)

        #add HCAL hits    
#        for hit in hcal:
#             id = ROOT.HcalDetId(hit.detId())
#             displayHCAL.addRecHit(hit,id.depth())

#        for cluster in hcalClusters:
#            displayHCAL.addCluster(cluster, links=False)


        if counter < 1000 and recoTau[0].ntotal!=0:
#            displayHCAL.viewEtaPhi(dmname(recoTau[0].decayMode()) + ' (gen : ' + gen_dm + ')', 'HCAL_' + str(evtid), evtid, recoTau[0].ntotal)
            displayECAL.viewEtaPhi(dmname(recoTau[0].decayMode()) + ' (gen : ' + gen_dm + ')', 'ECAL_' + str(evtid), evtid, recoTau[0].ntotal)
        
            counter += 1

    event_ntau[0] = len(taus)
    event_ngentau[0] = len(genTaus)
    event_gentaupt[0] = _gen_pt
    event_gentaueta[0] = _gen_eta
    event_gendm[0] = _gen_dm
    event_tree.Fill()



#        try:
#            input("Press enter to continue")
#        except SyntaxError:
#            pass



print evtid, 'events are processed !'

file.Write()
file.Close()

