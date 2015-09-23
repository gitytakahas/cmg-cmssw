from CMGTools.RootTools.analyzers.TreeAnalyzerNumpy import TreeAnalyzerNumpy
from CMGTools.H2TauTau.proto.analyzers.ntuple import *
from CMGTools.RootTools.fwlite.AutoHandle import AutoHandle
from CMGTools.RootTools.utils.DeltaR import bestMatch
#from CMGTools.RootTools.analyzers.GenParticleAnalyzer import *
from CMGTools.RootTools.physicsobjects.PhysicsObjects import GenParticle, PhysicsObject, printOut
from CMGTools.RootTools.physicsobjects.PhysicsObjects import Jet, GenJet
from CMGTools.RootTools.utils.DeltaR import cleanObjectCollection

class H2TauTauTreeProducerGenerator( TreeAnalyzerNumpy ):
    '''Tree producer for the H->tau tau analysis.'''
    
    def getAllDaughters(self, p, l):
        for i in range(0, p.numberOfDaughters()):
            d = p.daughter(i)
            l.append(d)
            self.getAllDaughters(d, l)

    def getVisibleP4(self, gen):
        p4vis = gen.p4()
        daughters = []
        self.getAllDaughters(gen, daughters)
        invisDaughters = [p for p in daughters if abs(p.pdgId()) in [12, 14, 16]]
        for d in invisDaughters:
            p4vis -= d.p4()

        return p4vis

    def findCentralJets( self, leadJets, otherJets ):
        '''Finds all jets between the 2 leading jets, for central jet veto.'''
        if not len(otherJets):
            return []
        etamin = leadJets[0].eta()
        etamax = leadJets[1].eta()
        if etamin > etamax:
            etamin, etamax = etamax, etamin
        def isCentral( jet ):
            if jet.pt() < 30.:
                return False
            eta = jet.eta()
            if etamin < eta and eta < etamax:
                return True
            else:
                return False
        centralJets = filter( isCentral, otherJets )
        return centralJets


    def declareVariables(self):

        tr = self.tree

        var( tr, 'run', int)
        var( tr, 'lumi', int)
        var( tr, 'evt', int)

        bookGenParticle(tr, 'higgs')
        bookGenParticle(tr, 'l1_gen')
        bookGenParticle(tr, 'l2_gen')
        bookGenParticle(tr, 'genjet1')
        bookGenParticle(tr, 'genjet2')

        var(tr, 'mjj')
        var(tr, 'deta')
        var(tr, 'nCentral')
        var(tr, 'nGenJets')

        var(tr, 'l1_gen_vis_pt')
        var(tr, 'l1_gen_vis_eta')
        var(tr, 'l1_gen_vis_phi')
        var(tr, 'l1_gen_vis_m')
        var(tr, 'l1_gen_decay_pdgId')

        var(tr, 'l2_gen_vis_pt')
        var(tr, 'l2_gen_vis_eta')
        var(tr, 'l2_gen_vis_phi')
        var(tr, 'l2_gen_vis_m')
        var(tr, 'l2_gen_decay_pdgId')
        
        var(tr, 'genMet')
        var(tr, 'genMex')
        var(tr, 'genMey')

        self.maxNGenJets = 4
        for i in range(0, self.maxNGenJets):
            bookGenParticle(tr, 'genQG_{i}'.format(i=i))


         
    def declareHandles(self):
        super(H2TauTauTreeProducerGenerator, self).declareHandles()


        self.src = 'genParticlesPruned'

        if hasattr( self.cfg_ana, 'src'):
            self.src = self.cfg_ana.src


        self.mchandles['genParticles'] = AutoHandle( self.src,
                                                     'std::vector<reco::GenParticle>' )

        self.gensrc = 'slimmedGenJets'

        if hasattr( self.cfg_ana, 'gensrc'):
            self.gensrc = self.cfg_ana.gensrc

        self.mchandles['genJets'] = AutoHandle(self.gensrc,
                                               'std::vector<cmg::PhysicsObjectWithPtr< edm::Ptr<reco::GenJet> > >')
#                                               'std::vector<reco::GenJet>')



        
        
    def process(self, iEvent, event):
        self.readCollections( iEvent )
                
        tr = self.tree
        tr.reset()

        fill( tr, 'run', iEvent.eventAuxiliary().id().run())
        fill( tr, 'lumi', iEvent.eventAuxiliary().id().luminosityBlock())
        fill( tr, 'evt', iEvent.eventAuxiliary().id().event())

        genParticles = self.mchandles['genParticles'].product()
        event.genParticles = map( GenParticle, genParticles)

        parent = [25, 23]

        higgsBosons = [gen for gen in event.genParticles if gen.status()==3 and abs(gen.pdgId()) in parent]

        if len(higgsBosons)!=1:
            strerr = '{nhiggs} Higgs bosons, this should not happen :\n {comp}'.format(nhiggs=len(higgsBosons), comp=str(self.cfg_comp))
            return False
#            raise ValueError(strerr)

        else:

            higgs = higgsBosons[0]

#            import pdb; pdb.set_trace()
            fillGenParticle(tr, 'higgs', higgs)


            genTau = []

            for i in range(0, higgs.numberOfDaughters()):
                if abs(higgs.daughter(i).pdgId())==15 and higgs.daughter(i).status()==3:
                    genTau.append(higgs.daughter(i))
                    
            flag_tau = False
            flag_mu = False

            daughters = []

            if len(genTau)==2:
                
                for itau in genTau:

                    pdgId = itau.pdgId() # this is temporal
                    for ii in range(0, itau.daughter(0).numberOfDaughters()):
                        _pdg_ = itau.daughter(0).daughter(ii).pdgId()
                        if abs(_pdg_) in [11, 13]:
                            pdgId = _pdg_


                    if abs(pdgId) in [13]:
                        
#                        import pdb; pdb.set_trace()
                        fillGenParticle(tr, 'l2_gen', itau)
                        genVisTau2 = self.getVisibleP4(itau)
                        fill(tr, 'l2_gen_vis_pt', genVisTau2.pt())
                        fill(tr, 'l2_gen_vis_eta', genVisTau2.eta())
                        fill(tr, 'l2_gen_vis_phi', genVisTau2.phi())
                        fill(tr, 'l2_gen_vis_m', genVisTau2.mass())
                        fill(tr, 'l2_gen_decay_pdgId', pdgId)
                        flag_mu = True
                        daughters.append(itau)
                    elif abs(pdgId) in [15]:
                        fillGenParticle(tr, 'l1_gen', itau)
                        genVisTau1 = self.getVisibleP4(itau)
                        fill(tr, 'l1_gen_vis_pt', genVisTau1.pt())
                        fill(tr, 'l1_gen_vis_eta', genVisTau1.eta())
                        fill(tr, 'l1_gen_vis_phi', genVisTau1.phi())
                        fill(tr, 'l1_gen_vis_m', genVisTau1.mass())
                        fill(tr, 'l1_gen_decay_pdgId', pdgId)
                        flag_tau = True
                        daughters.append(itau)


            if not (flag_tau and flag_mu):
                return False



            genJets = self.mchandles['genJets'].product()
            event.genJets = map(GenJet, genJets)

        
            selGenJets = [jet for jet in event.genJets if jet.pt() > 30 and abs(jet.eta()) < 4.7]

            cleanGenJets, dummy = cleanObjectCollection( selGenJets,
                                                                  masks = daughters,
                                                                  deltaRMin = 0.5)

#            import pdb; pdb.set_trace()
            cleanGenJets.sort(key=lambda x: -x.pt())

            deta = -1
            mjj = -1
            ncentral = -1
            
            if len(cleanGenJets) >= 2:
                deta = cleanGenJets[0].eta() - cleanGenJets[1].eta()
                dijetp4 = cleanGenJets[0].p4() + cleanGenJets[1].p4()
                mjj = dijetp4.M()
                
                leadJets = cleanGenJets[:2]
                otherJets = cleanGenJets[2:]
                centralJets = self.findCentralJets( leadJets, otherJets )
                ncentral = len(centralJets)
                
                fill(tr, 'mjj', mjj)
                fill(tr, 'deta', deta)
                fill(tr, 'nCentral', ncentral)

            fill(tr, 'nGenJets', len(cleanGenJets))

            if len(cleanGenJets)>=1:
                fillGenParticle(tr, 'genjet1', cleanGenJets[0])
            if len(cleanGenJets)>=2:
                fillGenParticle(tr, 'genjet2', cleanGenJets[1])


#            genTau1 = []
#            genTau2 = []
#
#            for i in range(0, higgs.numberOfDaughters()):
#                if higgs.daughter(i).pdgId()==15 and higgs.daughter(i).status()==3:
#                    genTau1.append(higgs.daughter(i))
#                elif higgs.daughter(i).pdgId()==-15 and higgs.daughter(i).status()==3:
#                    genTau2.append(higgs.daughter(i))
#
#
#            if len(genTau1)==1:
#                fillGenParticle(tr, 'l1_gen', genTau1[0])
#                genVisTau1 = self.getVisibleP4(genTau1[0])
#                fill(tr, 'l1_gen_vis_pt', genVisTau1.pt())
#                fill(tr, 'l1_gen_vis_eta', genVisTau1.eta())
#                fill(tr, 'l1_gen_vis_phi', genVisTau1.phi())
#
#
#                pdgId1 = genTau1[0].pdgId()
#                for ii in range(0, genTau1[0].daughter(0).numberOfDaughters()):
#                    _pdg_ = genTau1[0].daughter(0).daughter(ii).pdgId()
#                    if abs(_pdg_) in [11, 13]:
#                        pdgId1 = _pdg_
#
#                fill(tr, 'l1_gen_decay_pdgId', pdgId1)
#
#
#            if len(genTau2)==1:
#                fillGenParticle(tr, 'l2_gen', genTau2[0])
#                genVisTau2 = self.getVisibleP4(genTau2[0])
#                fill(tr, 'l2_gen_vis_pt', genVisTau2.pt())
#                fill(tr, 'l2_gen_vis_eta', genVisTau2.eta())
#                fill(tr, 'l2_gen_vis_phi', genVisTau2.phi())
#
#                pdgId2 = genTau2[0].pdgId()
#                for ii in range(0, genTau2[0].daughter(0).numberOfDaughters()):
#                    _pdg_ = genTau2[0].daughter(0).daughter(ii).pdgId()
#                    if abs(_pdg_) in [11, 13]:
#                        pdgId2 = _pdg_
#
#                fill(tr, 'l2_gen_decay_pdgId', pdgId2)



            neutrinos = [p for p in event.genParticles if abs(p.pdgId()) in (12, 14, 16)]
            if neutrinos:
                genMet = neutrinos[0].p4()
                for p in neutrinos[1:]:
                    genMet += p.p4()
                fill(tr, 'genMet', p.pt())
                fill(tr, 'genMex', p.px())
                fill(tr, 'genMey', p.py())
            else:
                fill(tr, 'genMet', 0.)
                fill(tr, 'genMex', 0.)
                fill(tr, 'genMey', 0.)
          

            quarksGluons = [p for p in event.genParticles if abs(p.pdgId()) in (1, 2, 3, 4, 5, 21) and p.status() == 3 and (p.numberOfDaughters() == 0 or p.daughter(0).status() != 3)]
            quarksGluons.sort(key=lambda x: -x.pt())
            for i in range(0, min(self.maxNGenJets, len(quarksGluons))):
                fillGenParticle(tr, 'genQG_{i}'.format(i=i), quarksGluons[i])


            self.tree.tree.Fill()
