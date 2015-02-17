import ROOT
import os
import numpy as num
from DataFormats.FWLite import Events, Handle
from Display import *

ROOT.gROOT.SetBatch(True)

ecalH  = Handle ('std::vector<reco::PFRecHit>')
hcalH  = Handle ('std::vector<reco::PFRecHit>')
genParticlesH  = Handle ('std::vector<reco::GenParticle>')
ecalClustersH  = Handle ('std::vector<reco::PFCluster>')
hcalClustersH  = Handle ('std::vector<reco::PFCluster>')
# tracksH  = Handle ('std::vector<reco::PFRecTrack>')

tauH = Handle('std::vector<reco::PFTau>')
tauH_disc = Handle('reco::PFTauDiscriminator')
tauH_disc_ch = Handle('reco::PFTauDiscriminator')


filelist = []

for ii in range(20):

#    if ii in [0, 1, 34, 44, 58, 64, 71, 76, 81, 93, 99]: continue
#for ii in range(92,97):
#for ii in range(20):
    filename = '/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/TauGun_20150214/job_' + str(ii) + '/step.root'
#    filename = '/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/test/job_' + str(ii) + '/step.root'
#    filename = '/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/TauGun_20150213_orig/job_' + str(ii) + '/step.root'

    if os.path.exists(filename):
        filelist.append(filename)
        print 'added : ', filename
    else:
        print 'No file found : ', filename


events = Events(filelist)
#events = Events('/afs/cern.ch/user/y/ytakahas/work/TauIsolation/CMSSW_7_2_3/src/TauGun_20150213_orig/job_98/step.root')

file = ROOT.TFile('Myroot.root', 'recreate')
ttree = ROOT.TTree('per_tau','per_tau')
etree = ROOT.TTree('per_event','per_event')
    
e_nphoton = num.zeros(1, dtype=int)
e_dm = num.zeros(1, dtype=int)
e_gen_nphoton_notau = num.zeros(1, dtype=int)
e_gen_nphoton = num.zeros(1, dtype=int)
e_gen_npion = num.zeros(1, dtype=int)
e_total = num.zeros(1, dtype=float)
e_gendm = num.zeros(1, dtype=int)
e_genpt = num.zeros(1, dtype=float)
e_geneta = num.zeros(1, dtype=float)
e_genphi = num.zeros(1, dtype=float)
e_taupt = num.zeros(1, dtype=float)
e_taueta = num.zeros(1, dtype=float)
e_tauphi = num.zeros(1, dtype=float)
e_ntau = num.zeros(1, dtype=int)

t_gendm = num.zeros(1, dtype=int)
t_gen_nphoton = num.zeros(1, dtype=int)
t_gen_npion = num.zeros(1, dtype=int)
t_genpt = num.zeros(1, dtype=float)
t_geneta = num.zeros(1, dtype=float)
t_genphi = num.zeros(1, dtype=float)
t_taupt = num.zeros(1, dtype=float)
t_taueta = num.zeros(1, dtype=float)
t_tauphi = num.zeros(1, dtype=float)
t_dm = num.zeros(1, dtype=int)
t_energy = num.zeros(1, dtype=float)
t_dr = num.zeros(1, dtype=float)
t_deta = num.zeros(1, dtype=float)
t_dphi = num.zeros(1, dtype=float)


etree.Branch('e_nphoton', e_nphoton, 'e_nphoton/I')
etree.Branch('e_total', e_total, 'e_total/D')
etree.Branch('e_dm', e_dm, 'e_dm/I')
etree.Branch('e_gen_nphoton_notau', e_gen_nphoton_notau, 'e_gen_nphoton_notau/I')
etree.Branch('e_gen_nphoton', e_gen_nphoton, 'e_gen_nphoton/I')
etree.Branch('e_gen_npion', e_gen_npion, 'e_gen_npion/I')
etree.Branch('e_gendm', e_gendm, 'e_gendm/I')
etree.Branch('e_genpt', e_genpt, 'e_genpt/D')
etree.Branch('e_geneta', e_geneta, 'e_geneta/D')
etree.Branch('e_genphi', e_genphi, 'e_genphi/D')
etree.Branch('e_taupt', e_taupt, 'e_taupt/D')
etree.Branch('e_taueta', e_taueta, 'e_taueta/D')
etree.Branch('e_tauphi', e_tauphi, 'e_tauphi/D')
etree.Branch('e_ntau', e_ntau, 'e_ntau/I')

ttree.Branch('t_gendm', t_gendm, 't_gendm/I')
ttree.Branch('t_gen_nphoton', t_gen_nphoton, 't_gen_nphoton/I')
ttree.Branch('t_gen_npion', t_gen_npion, 't_gen_npion/I')
ttree.Branch('t_genpt', t_genpt, 't_genpt/D')
ttree.Branch('t_geneta', t_geneta, 't_geneta/D')
ttree.Branch('t_genphi', t_genphi, 't_genphi/D')
ttree.Branch('t_taupt', t_taupt, 't_taupt/D')
ttree.Branch('t_taueta', t_taueta, 't_taueta/D')
ttree.Branch('t_tauphi', t_tauphi, 't_tauphi/D')
ttree.Branch('t_dm', t_dm, 't_dm/I')
ttree.Branch('t_energy', t_energy, 't_energy/D')
ttree.Branch('t_dr', t_dr, 't_dr/D')
ttree.Branch('t_deta', t_deta, 't_deta/D')
ttree.Branch('t_dphi', t_dphi, 't_dphi/D')


counter = 0
evtid = -1

for event in events:
    
    print '---------------------- evt = ', evtid, '--------------------------'


    evtid += 1  

    event.getByLabel('particleFlowRecHitECAL',ecalH)
    event.getByLabel('particleFlowRecHitHBHE',hcalH)
    event.getByLabel('genParticles',genParticlesH)
    event.getByLabel('particleFlowClusterECAL',ecalClustersH)
    event.getByLabel('particleFlowClusterHBHE', hcalClustersH)
   
    event.getByLabel("hpsPFTauProducer", tauH)
    event.getByLabel("hpsPFTauMVA3IsolationNeutralIsoPtSum", tauH_disc)
    event.getByLabel("hpsPFTauMVA3IsolationChargedIsoPtSum", tauH_disc_ch)

    ecal = ecalH.product()
    hcal = hcalH.product()
    genParticles = genParticlesH.product()
    ecalClusters = ecalClustersH.product()
    hcalClusters = hcalClustersH.product()

    taus = tauH.product()
    taus_disc = tauH_disc.product()
    taus_disc_ch = tauH_disc_ch.product()
    
    genTaus = [p for p in genParticles if abs(p.pdgId()) == 15]
    genPhotons = [p for p in genParticles if abs(p.pdgId()) == 22]

    for genParticle in genTaus:

        finDaughters = finalDaughters(genParticle, [])
        genParticle.genVisP4 = p4sumvis(finDaughters)

        gen_dm, gen_dmid, nphoton, npion = returnGenDecayMode(finDaughters)

        print '* Generated tau info *************************************'
        print '# of charged pions', npion
        print '# of photons', nphoton, '\n'
        print 'gen tau pT = ', genTaus[0].pt(), gen_dm

        recoTau = []

        displayECAL = DisplayManager('ECAL', genParticle.eta(), genParticle.phi(), 0.6)
        displayHCAL = DisplayManager('HCAL', genParticle.eta(), genParticle.phi(), 0.6)

        if not (gen_dmid in [0,1,2,10]): continue

        for tau in taus:
            print 'check1'
            if not deltaR(tau.eta(), tau.phi(), genParticle.genVisP4.eta(), genParticle.genVisP4.phi()) < 0.5:
                continue

            print 'check2', tau.decayMode()
            if tau.decayMode() < 0 : continue
#            if tau.decayMode() in [5,6,7,8,9] : continue


            if not (tau.decayMode() in [0,1,2,10]): 
                print 'Tau decay mode not equal 0,1,2,10 : ', tau.decayMode()
                continue

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

            for itau in range(len(taus_disc)):
                if tau == taus_disc.key(itau).get():
                    print '\t isolation official : Neutr = ', taus_disc.value(itau)
                    print '\t isolation official : Charged = ', taus_disc_ch.value(itau)
                    tau.ntotal = taus_disc.value(itau)

            for iphoton in tau.signalPFGammaCands():
                print '\t\t signal photon pT = ', iphoton.pt(), ', eta = ', iphoton.eta(), ', phi = ', iphoton.phi()
                displayECAL.addPhoton(iphoton, 1)
                    
            for iphoton in tau.isolationPFGammaCands():
                print '\t\t iso. photon pT = ', iphoton.pt(), ', eta = ', iphoton.eta(), ', phi = ', iphoton.phi()
                displayECAL.addPhoton(iphoton,2)

                t_gendm[0] = gen_dmid
                t_gen_nphoton[0] = nphoton
                t_gen_npion[0] = npion
                t_genpt[0] = genParticle.genVisP4.pt()
                t_geneta[0] = genParticle.genVisP4.eta()
                t_genphi[0] = genParticle.genVisP4.phi()
                t_taupt[0] = tau.pt()
                t_taueta[0] = tau.eta()
                t_tauphi[0] = tau.phi()
                t_dm[0] = tau.decayMode()
                t_energy[0] = iphoton.pt()
                t_dr[0] = deltaR(tau.eta(), tau.phi(), iphoton.eta(), iphoton.phi())
                t_deta[0] = tau.eta() - iphoton.eta()
                t_dphi[0] = deltaPhi(tau.phi(), iphoton.phi())

                ttree.Fill()


            for ich in tau.signalPFChargedHadrCands():
                print '\t\t signal charged pT = ', ich.pt(), ' eta = ', ich.eta(), ' phi = ', ich.phi()
                displayECAL.addCH(ich, 1)
                displayHCAL.addCH(ich, 1)
                    
            for ich in tau.isolationPFChargedHadrCands():
                print '\t\t iso. charged pT = ', ich.pt(), ' eta = ', ich.eta(), ' phi = ', ich.phi()
                displayECAL.addCH(ich, 2)
                displayHCAL.addCH(ich, 1)

 #           for ich in tau.signalPFNeutrHadrCands():
 #               print '\t\t signal neutral pT = ', ich.pt(), ' eta = ', ich.eta(), ' phi = ', ich.phi()
 #               displayECAL.addCH(ich, 3)
                    
#            for ich in tau.isolationPFNeutrHadrCands():
#                print '\t\t iso. neutral pT = ', ich.pt(), ' eta = ', ich.eta(), ' phi = ', ich.phi()
#                displayECAL.addCH(ich, 4)

            recoTau.append(tau)

        if len(recoTau)!=1: 
            continue

        if recoTau[0].ntotal!=0:
#        if nphoton!=0:
            print "Deposit :", evtid

        e_nphoton[0] = len(recoTau[0].isolationPFGammaCands())
        e_dm[0] = recoTau[0].decayMode()
        e_gen_nphoton[0] = nphoton
        e_gen_nphoton[0] = len(genPhotons)
        e_gen_npion[0] = npion
        e_total[0] = recoTau[0].ntotal
        e_gendm[0] = gen_dmid
        e_genpt[0] = genParticle.genVisP4.pt()
        e_geneta[0] = genParticle.genVisP4.eta()
        e_genphi[0] = genParticle.genVisP4.phi()
        e_taupt[0] = recoTau[0].pt()
        e_taueta[0] = recoTau[0].eta()
        e_tauphi[0] = recoTau[0].phi()
        e_ntau[0] = len(recoTau)
        etree.Fill()

        displayECAL.addRecoTau(recoTau[0])
        displayHCAL.addRecoTau(recoTau[0])

        #reloop on gen particles and add them in view
        for genP in genParticles:
            if genP.status()!=1 or abs(genP.pdgId()) in [12, 14, 16]:
                continue

            displayECAL.addGenParticle(genP) 
            displayHCAL.addGenParticle(genP) 
        

        #add HCAL hits    
        for hit in hcal:
             id = ROOT.HcalDetId(hit.detId())
             displayHCAL.addRecHit(hit,id.depth())

        #add ECAL hits    
        for hit in ecal:
            displayECAL.addRecHit(hit,1)

#        import pdb; pdb.set_trace()
#        for cluster in ecalClusters:
#            displayECAL.addCluster(cluster, links=False)

#        for cluster in hcalClusters:
#            displayHCAL.addCluster(cluster, links=False)


        if counter < 100 and recoTau[0].ntotal!=0:
#        if counter < 100:
            displayHCAL.viewEtaPhi(dmname(recoTau[0].decayMode()) + ' (gen : ' + gen_dm + ')', 'HCAL_' + str(evtid-1), counter, recoTau[0].ntotal)
            displayECAL.viewEtaPhi(dmname(recoTau[0].decayMode()) + ' (gen : ' + gen_dm + ')', 'ECAL_' + str(evtid-1), counter, recoTau[0].ntotal)
        
            counter += 1



#        try:
#            input("Press enter to continue")
#        except SyntaxError:
#            pass





file.Write()
file.Close()

