from CMGTools.RootTools.analyzers.TreeAnalyzerNumpy import TreeAnalyzerNumpy
from CMGTools.H2TauTau.proto.analyzers.ntuple import *
from CMGTools.RootTools.fwlite.AutoHandle import AutoHandle
from CMGTools.RootTools.utils.DeltaR import bestMatch, cleanObjectCollection, matchObjectCollection
import math

from ROOT import TLorentzVector

def getHemispheres(jets):

    nJets = len(jets)

    possibleHem1s = []
    possibleHem2s = []

    if nJets < 2 :
        
        emptyHem1 = TLorentzVector()
        emptyHem2 = TLorentzVector()
        
        return [emptyHem1, emptyHem2]


    nComb = pow(2, nJets);

    # step 1: store all possible partitions of the input jets

    j_count = 0

    for i in range(1, nComb-1):

        j_temp1 = TLorentzVector()
        j_temp2 = TLorentzVector()

        itemp = i
        j_count = nComb/2
        count = 0;

        while(j_count > 0):  #decompose i into binary '1's and '0's ; put the '1' jets into j_temp1 and the '0' jets into j_temp2

            if(itemp/j_count == 1):
                j_temp1 += jets[count]
            else:
                j_temp2 += jets[count]


            itemp -= j_count*(itemp/j_count) #note this is always (0 or 1)*j_count
            j_count /= 2
            count += 1

        possibleHem1s.append(j_temp1)
        possibleHem2s.append(j_temp2)


    #step 2: choose the partition that minimizes m1^2 + m2^2

    mMin = -1.

    myHem1 = TLorentzVector()
    myHem2 = TLorentzVector()

    for i in range(0, len(possibleHem1s)):

        mTemp = possibleHem1s[i].M2() + possibleHem2s[i].M2()

        if (mMin < 0 or  mTemp < mMin):

            mMin = mTemp;
            myHem1 = possibleHem1s[i]
            myHem2 = possibleHem2s[i]


 

    # return the hemispheres in decreasing order of pt

    hemsOut = []

    if(myHem1.Pt() > myHem2.Pt()):
        hemsOut.append(myHem1)
        hemsOut.append(myHem2)
    else:
        hemsOut.append(myHem2)
        hemsOut.append(myHem1)


    return hemsOut





def computeMR(hem1, hem2):
    return math.sqrt(pow(hem1.P() + hem2.P(), 2) - pow(hem1.Pz() + hem2.Pz(), 2))



def computeRsq(hem1, hem2, pfMet):

    mR = computeMR(hem1, hem2)
    term1 = pfMet.pt()/2*(hem1.Pt() + hem2.Pt())
    term2 = pfMet.px()/2*(hem1.Px() + hem2.Px()) + pfMet.py()/2*(hem1.Py() + hem2.Py()); #dot product of MET with (p1T + p2T)
    mTR = math.sqrt(term1 - term2)

    print 'check !', mTR, mR
    if mR ==0:
        return -1, -1
    else:
        return mTR, (mTR / mR) * (mTR / mR)




class H2TauTauTreeProducerTauMu( TreeAnalyzerNumpy ):
    '''Tree producer for the H->tau tau analysis.

    Some of the functions in this class should be made available to everybody.'''
    
    def declareVariables(self):

        tr = self.tree

        var( tr, 'run', int)
        var( tr, 'lumi', int)
        var( tr, 'evt', int)
        var( tr, 'NUP', int)
        var( tr, 'rho')
        var( tr, 'HT_jet30')
        var( tr, 'HT_jet20')
        var( tr, 'MR')
        var( tr, 'MTR')
        var( tr, 'Rsq')
        var( tr, 'njets40')
        
        bookDiLepton(tr)
        bookMinimum(tr, 'outgoing1')
        bookMinimum(tr, 'outgoing2')
        var( tr, 'outgoing_dphi')
        var( tr, 'outgoing_deta')
        var( tr, 'outgoing_mjj')
        var( tr, 'outgoing_dR')
        var( tr, 'noutgoing', int)

        var( tr, 'genhiggspt')
        var( tr, 'genhiggseta')
        var( tr, 'ngenhiggs', int)
        
        var( tr, 'pfmet')

        bookParticle(tr, 'diTau')
        bookTau(tr, 'l1')
        bookGenParticle(tr, 'l1_gen')
        var(tr, 'l1_gen_vis_pt')
        var(tr, 'l1_gen_vis_eta')
        var(tr, 'l1_gen_vis_phi')
        bookMuon(tr, 'l2')
        bookGenParticle(tr, 'l2_gen')
        bookParticle(tr, 'l1Jet')
        bookParticle(tr, 'l2Jet')

        var( tr, 'nJets')
        var( tr, 'nJets20')
        var( tr, 'ngenjet')
        bookJet(tr, 'jet1')
        bookJet(tr, 'jet2')
        bookJet(tr, 'jet3')
        bookJet(tr, 'jet4')
        var( tr, 'jet1_isME')
        var( tr, 'jet1_isME_flavour')
        var( tr, 'jet2_isME')
        var( tr, 'jet2_isME_flavour')
        var( tr, 'jet3_isME')
        var( tr, 'jet3_isME_flavour')
        var( tr, 'jet4_isME')
        var( tr, 'jet4_isME_flavour')

        var( tr, 'jet1_isgjet')
        var( tr, 'jet2_isgjet')
        var( tr, 'jet3_isgjet')
        var( tr, 'jet4_isgjet')
        var( tr, 'jet1_isgjetpt')
        var( tr, 'jet2_isgjetpt')
        var( tr, 'jet3_isgjetpt')
        var( tr, 'jet4_isgjetpt')

        # b jets
        var( tr, 'nBJets')
        var(tr, 'nCSVLJets')
        bookJet(tr, 'bjet1')

        bookVBF( tr, 'VBF' )
        #bookJet(tr, 'cjet') # leading central veto jet from VBF

        var( tr, 'weight')
        var( tr, 'vertexWeight')
        var( tr, 'embedWeight')
        var( tr, 'hqtWeight')
        var( tr, 'hqtWeightUp')
        var( tr, 'hqtWeightDown')
        var( tr, 'NJetWeight')

        var( tr, 'tauFakeRateWeight')
        var( tr, 'tauFakeRateWeightUp')
        var( tr, 'tauFakeRateWeightDown')

        var( tr, 'nVert')

        var( tr, 'isFake')
        var( tr, 'isSignal')
        var( tr, 'leptonAccept')
        var( tr, 'thirdLeptonVeto')

        var(tr, 'genMass')
        var(tr, 'genMet')
        var(tr, 'genMex')
        var(tr, 'genMey')

        self.maxNGenJets = 4
        for i in range(0, self.maxNGenJets):
            bookGenParticle(tr, 'genQG_{i}'.format(i=i))


         
    def declareHandles(self):
        super(H2TauTauTreeProducerTauMu, self).declareHandles()
        self.handles['pfmetraw'] = AutoHandle(
            'cmgPFMETRaw',
            'std::vector<cmg::BaseMET>' 
            )


        self.handles['genjets'] = AutoHandle(
            'genJetSel',
            'vector<cmg::PhysicsObjectWithPtr<edm::Ptr<reco::GenJet>>>' 
            )



    def process(self, iEvent, event):
        self.readCollections( iEvent )
                
        tr = self.tree
        tr.reset()

        fill( tr, 'run', event.run) 
        fill( tr, 'lumi',event.lumi)
        fill( tr, 'evt', event.eventId)

        # This is only relevant for the W/Z+N-jet samples
        if hasattr(event, 'NUP'):
            fill( tr, 'NUP', event.NUP)
        fill( tr, 'rho', event.rho)

        
        fillDiLepton( tr, event.diLepton )

        # import pdb; pdb.set_trace()
        pfmet = self.handles['pfmetraw'].product()[0]
        fill(tr, 'pfmet', pfmet.pt())

        fillParticle(tr, 'diTau', event.diLepton)
        fillTau(tr, 'l1', event.diLepton.leg1() )
        genTau = 0 #event.diLepton.leg1().genParticle()

#        import pdb; pdb.set_trace()
        genjets = self.handles['genjets'].product()

        _rmlep_ = [p for p in event.genParticles if p.status() == 3 and abs(p.pdgId()) in [11, 13, 15]]
 
        genjets, dummy = cleanObjectCollection( genjets,
                                                masks = _rmlep_,
                                                deltaRMin = 0.5 )

        fill( tr, 'ngenjet', len(genjets))


        if hasattr(event, 'genParticles'):
            sel_taus = [p for p in event.genParticles if p.status() == 3 and abs(p.pdgId()) in [11, 13, 15, 1,2,3,4,5,21]]
            _tau_, dr2min = bestMatch(event.diLepton.leg1(), sel_taus)
            if dr2min < 0.25:
                genTau = _tau_

#            for p in event.genParticles:
#                if p.status() == 3 and abs(p.pdgId()) in [15]:


        if not genTau==0:
            fillGenParticle(tr, 'l1_gen', genTau)

            def getAllDaughters(p, l):
                for i in range(0, p.numberOfDaughters()):
                    d = p.daughter(i)
                    l.append(d)
                    getAllDaughters(d, l)

            p4vis = genTau.p4()
            daughters = []
            getAllDaughters(genTau, daughters)
            invisDaughters = [p for p in daughters if abs(p.pdgId()) in [12, 14, 16]]
            for d in invisDaughters:
                p4vis -= d.p4()

            fill(tr, 'l1_gen_vis_pt', p4vis.pt())
            fill(tr, 'l1_gen_vis_eta', p4vis.eta())
            fill(tr, 'l1_gen_vis_phi', p4vis.phi())


        fillMuon(tr, 'l2', event.diLepton.leg2() )


        ht20 = event.diLepton.leg1().pt() + event.diLepton.leg2().pt()

        for ijet in event.cleanJets:
            ht20 += ijet.pt()

        ht30 = event.diLepton.leg1().pt() + event.diLepton.leg2().pt()

        for ijet in event.cleanJets30:
            ht30 += ijet.pt()
        
        fill( tr, 'HT_jet30', ht20)
        fill( tr, 'HT_jet20', ht30)

        # RAZOR variables
        alljets = []

        for ijet in event.cleanJets30:
            if ijet.pt() < 40: continue
            if abs(ijet.eta()) > 3.: continue

            _jet_ = TLorentzVector()
            _jet_.SetPtEtaPhiM(ijet.pt(), ijet.eta(), ijet.phi(), ijet.mass())

            alljets.append(_jet_)


        _njets40 = len(alljets)
        
        _higgs_ = TLorentzVector()
        _higgs_.SetPtEtaPhiM(event.diLepton.pt(), event.diLepton.eta(), event.diLepton.phi(), event.diLepton.mass())
        alljets.append(_higgs_)

        hlist = getHemispheres(alljets)

        if len(hlist) == 2:
            mr = computeMR(hlist[0], hlist[1])
            mtr, rsq = computeRsq(hlist[0], hlist[1], pfmet)

            fill( tr, 'MR', mr)
            fill( tr, 'MTR', mtr)
            fill( tr, 'Rsq', rsq)
            fill( tr, 'njets40', _njets40)
            
        genLepton = 0

#        import pdb; pdb.set_trace()

        if hasattr(event, 'genParticles'):
            sel_leptons = [p for p in event.genParticles if p.status() == 3 and abs(p.pdgId()) in [11, 13, 15, 1,2,3,4,5,21]]
            _lepton_, dr2min = bestMatch(event.diLepton.leg2(), sel_leptons)
            if dr2min < 0.25:
                genLepton = _lepton_

#            for p in event.genParticles:
#                if p.status() == 3 and abs(p.pdgId()) in [11, 13]:

                    

        if not genLepton==0:
            fillGenParticle(tr, 'l2_gen', genLepton)
            
#        if event.diLepton.leg2().genParticle():
#            fillGenParticle(tr, 'l2_gen', event.diLepton.leg2().genParticle())

        fillParticle(tr, 'l1Jet', event.diLepton.leg1().jet )
        fillParticle(tr, 'l2Jet', event.diLepton.leg2().jet )


        fill(tr, 'nJets20', len(event.cleanJets) )
        nJets30 = len(event.cleanJets30)
        fill(tr, 'nJets', nJets30 )
        nJets = len(event.cleanJets)
        if nJets>=1:
             fillJet(tr, 'jet1', event.cleanJets[0] )
        if nJets>=2:
             fillJet(tr, 'jet2', event.cleanJets[1] )
        if nJets>=3:
             fillJet(tr, 'jet3', event.cleanJets[2] )
        if nJets>=4:
             fillJet(tr, 'jet4', event.cleanJets[3] )



        ## Yuta added

        _outgoing_ = []

        if hasattr(event, 'genParticles'):
            _tmp_ = [p for p in event.genParticles if p.status() == 3 and abs(p.pdgId()) in [1,2,3,4,5,21]]

#            import pdb; pdb.set_trace()

            for i in _tmp_:

                if i.numberOfMothers()==0:
                    continue

                flag_proton = False
                for im in range(i.numberOfMothers()):
                    #                print i.mother(im).pdgId(),
                    if i.mother(im).pdgId()==2212: flag_proton = True

                if flag_proton:
                    continue

                flag_higgs = False
                for im in range(i.numberOfDaughters()):
                    if i.daughter(im).pdgId()==25: flag_higgs = True

                if flag_higgs:
                    continue

                _outgoing_.append(i)


            fill( tr, 'noutgoing', len(_outgoing_))

#            import pdb; pdb.set_trace()

            if len(_outgoing_)>=1:
                fillMinimum(tr, 'outgoing1', _outgoing_[0])
            if len(_outgoing_)>=2:
                fillMinimum(tr, 'outgoing2', _outgoing_[1])

                fill(tr, 'outgoing_dphi', deltaPhi(_outgoing_[0].phi(), _outgoing_[1].phi()))
                fill(tr, 'outgoing_deta', (_outgoing_[0].eta() - _outgoing_[1].eta()))
                fill(tr, 'outgoing_mjj', (_outgoing_[0].p4() + _outgoing_[1].p4()).M())

                _dphi_ = deltaPhi(_outgoing_[0].phi(), _outgoing_[1].phi())
                _deta_ = _outgoing_[0].eta() - _outgoing_[1].eta()
                _dr_ = math.sqrt(_dphi_*_dphi_ + _deta_*_deta_)
                
                fill(tr, 'outgoing_dR', _dr_)

                if self.cfg_comp.isMC:
                    higgsBosons = [gen for gen in event.genParticles if gen.status()==3 and gen.pdgId()==25]
                    fill( tr, 'ngenhiggs', len(higgsBosons))
                    
                    if len(higgsBosons)==1:
                        fill(tr, 'genhiggspt', higgsBosons[0].pt())
                        fill(tr, 'genhiggseta', higgsBosons[0].eta())
                        
                        #            import pdb; pdb.set_trace()
#            if hasattr(event, 'genHiggs'):

        
        if nJets>=1 and hasattr(event, 'genParticles'):
                    
            if nJets>=1:
                _gjet_, dr2min = bestMatch(event.cleanJets[0], _outgoing_)
                if dr2min < 0.25:
                    fill(tr, 'jet1_isME', True)
                    fill(tr, 'jet1_isME_flavour', _gjet_.pdgId())

                _mjet_, drmin =  bestMatch(event.cleanJets[0], genjets)
                if dr2min < 0.25:
                    fill(tr, 'jet1_isgjet', True)
                    fill(tr, 'jet1_isgjetpt', _mjet_.pt())
                

            if nJets>=2:
                _gjet_, dr2min = bestMatch(event.cleanJets[1], _outgoing_)
                if dr2min < 0.25:
                    fill(tr, 'jet2_isME', True)
                    fill(tr, 'jet2_isME_flavour', _gjet_.pdgId())

                _mjet_, drmin =  bestMatch(event.cleanJets[1], genjets)
                if dr2min < 0.25:
                    fill(tr, 'jet2_isgjet', True)
                    fill(tr, 'jet2_isgjetpt', _mjet_.pt())

            if nJets>=3:
                _gjet_, dr2min = bestMatch(event.cleanJets[2], _outgoing_)
                if dr2min < 0.25:
                    fill(tr, 'jet3_isME', True)
                    fill(tr, 'jet3_isME_flavour', _gjet_.pdgId())

                _mjet_, drmin =  bestMatch(event.cleanJets[2], genjets)
                if dr2min < 0.25:
                    fill(tr, 'jet3_isgjet', True)
                    fill(tr, 'jet3_isgjetpt', _mjet_.pt())

            if nJets>=4:
                _gjet_, dr2min = bestMatch(event.cleanJets[3], _outgoing_)
                if dr2min < 0.25:
                    fill(tr, 'jet4_isME', True)
                    fill(tr, 'jet4_isME_flavour', _gjet_.pdgId())

                _mjet_, drmin =  bestMatch(event.cleanJets[3], genjets)
                if dr2min < 0.25:
                    fill(tr, 'jet4_isgjet', True)
                    fill(tr, 'jet4_isgjetpt', _mjet_.pt())

        #### Yuta added end

        nBJets = len(event.cleanBJets)
        if nBJets>0:
             fillJet(tr, 'bjet1', event.cleanBJets[0] )                     
        fill(tr, 'nBJets', nBJets)

        # JAN - directly count CSVL jets as done in
        # other groups. May apply SFs as for CSVM jets
        # after rewriting BTagSF module in the future
        nCSVLJets = 0
        for jet in event.cleanJets:
            if jet.btag('combinedSecondaryVertexBJetTags') > 0.244:
                    nCSVLJets += 1
        fill(tr, 'nCSVLJets', nCSVLJets)

        if hasattr( event, 'vbf'):
             fillVBF( tr, 'VBF', event.vbf )
             #if len(event.vbf.centralJets) > 0:
             #        fillJet(tr, 'cjet', event.vbf.centralJets[0])

        fill(tr, 'weight', event.eventWeight)
        fill(tr, 'embedWeight', event.embedWeight)
        fill(tr, 'hqtWeight', event.higgsPtWeight)
        fill(tr, 'hqtWeightUp', event.higgsPtWeightUp)
        fill(tr, 'hqtWeightDown', event.higgsPtWeightDown)
        if hasattr( event, 'NJetWeight'):
            fill(tr, 'NJetWeight', event.NJetWeight)

        fill(tr, 'tauFakeRateWeightUp', event.tauFakeRateWeightUp)
        fill(tr, 'tauFakeRateWeightDown', event.tauFakeRateWeightDown)
        fill(tr, 'tauFakeRateWeight', event.tauFakeRateWeight)



        if hasattr( event, 'vertexWeight'): 
            fill(tr, 'vertexWeight', event.vertexWeight)
            fill(tr, 'nVert', len(event.vertices) ) 
            
        fill(tr, 'isFake', event.isFake)
        fill(tr, 'isSignal', event.isSignal)
        fill(tr, 'leptonAccept',        event.leptonAccept)
        fill(tr, 'thirdLeptonVeto', event.thirdLeptonVeto)


        if hasattr(event, 'genParticles'):
            # Get Higgs/Z mass
            for p in event.genParticles:
                if p.pdgId() in [23, 25, 35, 36, 37]:
                    fill(tr, 'genMass', p.mass())
                    break

            # Calculate gen MET
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

            # Fill hard quarks/gluons

#            import pdb; pdb.set_trace()
            quarksGluons = [p for p in event.genParticles if abs(p.pdgId()) in (1, 2, 3, 4, 5, 21) and p.status() == 3 and (p.numberOfDaughters() == 0 or p.daughter(0).status() != 3)]
            quarksGluons.sort(key=lambda x: -x.pt())
            for i in range(0, min(self.maxNGenJets, len(quarksGluons))):
                fillGenParticle(tr, 'genQG_{i}'.format(i=i), quarksGluons[i])

        self.tree.tree.Fill()
