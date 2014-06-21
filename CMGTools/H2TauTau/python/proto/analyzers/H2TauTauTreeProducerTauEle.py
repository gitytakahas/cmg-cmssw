from CMGTools.RootTools.analyzers.TreeAnalyzerNumpy import TreeAnalyzerNumpy
from CMGTools.H2TauTau.proto.analyzers.ntuple import *
from CMGTools.RootTools.fwlite.AutoHandle import AutoHandle


class H2TauTauTreeProducerTauEle( TreeAnalyzerNumpy ):
    '''Tree producer for the H->tau tau analysis.

    Some of the functions in this class should be made available to everybody.'''
    
    def declareVariables(self):

       tr = self.tree

       var( tr, 'run', int)
       var( tr, 'lumi', int)
       var( tr, 'evt', int)
       var( tr, 'NUP', int)
       
       bookDiLepton(tr)

       var( tr, 'pfmet')
       
       bookParticle(tr, 'diTau')
       bookTau(tr, 'l1')
       bookEle(tr, 'l2')
       bookParticle(tr, 'l1Jet')
       bookParticle(tr, 'l2Jet')
       
       var( tr, 'nJets')
       var( tr, 'nJets20')
       bookJet(tr, 'jet1')
       bookJet(tr, 'jet2')

       # b jets
       var( tr, 'nBJets')
       var(tr, 'nCSVLJets')
       bookJet(tr, 'bjet1')

       bookVBF( tr, 'VBF' )
       
       var( tr, 'weight')
       var( tr, 'vertexWeight')
       var( tr, 'embedWeight')
       var( tr, 'hqtWeight')
       var( tr, 'hqtWeightUp')
       var( tr, 'hqtWeightDown')
       var( tr, 'NJetWeight')
       var( tr, 'zllWeight')

       var( tr, 'tauTriggerWeight')
       var( tr, 'tauTriggerEffData')
       var( tr, 'tauTriggerEffMC')

       var( tr, 'tauTriggerNewWeight')
       var( tr, 'tauTriggerNewWeight_18')
       var( tr, 'tauTriggerNewWeight_20')
       var( tr, 'tauTriggerNewWeight_21')
       var( tr, 'tauTriggerNewWeight_24')
       var( tr, 'tauTriggerNewWeight_27')
       var( tr, 'tauTriggerNewWeight_30')
       var( tr, 'tauTriggerNewWeight_33')
       var( tr, 'tauTriggerNewWeight_36')
       var( tr, 'tauTriggerNewWeight_39')
       var( tr, 'tauTriggerNewWeight_42')

       var( tr, 'tauTriggerNew21Weight')
       var( tr, 'tauTriggerNew21Weight_18')
       var( tr, 'tauTriggerNew21Weight_20')
       var( tr, 'tauTriggerNew21Weight_21')
       var( tr, 'tauTriggerNew21Weight_24')
       var( tr, 'tauTriggerNew21Weight_27')
       var( tr, 'tauTriggerNew21Weight_30')
       var( tr, 'tauTriggerNew21Weight_33')
       var( tr, 'tauTriggerNew21Weight_36')
       var( tr, 'tauTriggerNew21Weight_39')
       var( tr, 'tauTriggerNew21Weight_42')


       var( tr, 'tauTriggerOldWeight')
       var( tr, 'tauTriggerOldWeight_18')
       var( tr, 'tauTriggerOldWeight_20')
       var( tr, 'tauTriggerOldWeight_21')
       var( tr, 'tauTriggerOldWeight_24')
       var( tr, 'tauTriggerOldWeight_27')
       var( tr, 'tauTriggerOldWeight_30')
       var( tr, 'tauTriggerOldWeight_33')
       var( tr, 'tauTriggerOldWeight_36')
       var( tr, 'tauTriggerOldWeight_39')
       var( tr, 'tauTriggerOldWeight_42')

       var( tr, 'tauFakeRateWeight')
       var( tr, 'tauFakeRateWeightUp')
       var( tr, 'tauFakeRateWeightDown')
       
       var( tr, 'nVert')
       
       var( tr, 'isFake')
       var( tr, 'isSignal')
       var( tr, 'leptonAccept')
       var( tr, 'thirdLeptonVeto')

       var(tr, 'genMass')
       var(tr, 'genPattern')
       
       bookGenParticle(tr, 'genW')
       bookGenParticle(tr, 'genZ')
       bookGenParticle(tr, 'genWlep')
       bookGenParticle(tr, 'genWnu')
       bookGenParticle(tr, 'genZleg1')
       bookGenParticle(tr, 'genZleg2')
       
       
    def declareHandles(self):
        super(H2TauTauTreeProducerTauEle, self).declareHandles()
        self.handles['pfmetraw'] = AutoHandle(
            'cmgPFMETRaw',
            'std::vector<cmg::BaseMET>' 
            )
        
    def process(self, iEvent, event):
       self.readCollections( iEvent )
            
       tr = self.tree
       tr.reset()
       
       fill( tr, 'run', event.run) 
       fill( tr, 'lumi',event.lumi)
       fill( tr, 'evt', event.eventId)
       fill( tr, 'NUP', event.NUP)

       fillDiLepton( tr, event.diLepton )

       # import pdb; pdb.set_trace()
       pfmet = self.handles['pfmetraw'].product()[0]
       fill(tr, 'pfmet', pfmet.pt())

       fill( tr, 'tauTriggerWeight', event.diLepton.leg1().triggerWeight)
       fill( tr, 'tauTriggerEffData', event.diLepton.leg1().triggerEffData)
       fill( tr, 'tauTriggerEffMC', event.diLepton.leg1().triggerEffMC)
       fill( tr, 'tauTriggerNewWeight', event.tauTriggerNewWeight)
       fill( tr, 'tauTriggerNew21Weight', event.tauTriggerNew21Weight)
       fill( tr, 'tauTriggerOldWeight', event.tauTriggerOldWeight)

       tweight = event.diLepton.leg1().triggerEffMC
       
       if event.diLepton.leg2().pt()>18:
           fill( tr, 'tauTriggerNewWeight_18', 1./tweight)
       else:
           fill( tr, 'tauTriggerNewWeight_18', event.tauTriggerNewWeight)

       if event.diLepton.leg2().pt()>20:
           fill( tr, 'tauTriggerNewWeight_20', 1./tweight)
       else:
           fill( tr, 'tauTriggerNewWeight_20', event.tauTriggerNewWeight)

       if event.diLepton.leg2().pt()>21:
           fill( tr, 'tauTriggerNewWeight_21', 1./tweight)
       else:
           fill( tr, 'tauTriggerNewWeight_21', event.tauTriggerNewWeight)

       if event.diLepton.leg2().pt()>24:
           fill( tr, 'tauTriggerNewWeight_24', 1./tweight)
       else:
           fill( tr, 'tauTriggerNewWeight_24', event.tauTriggerNewWeight)

       if event.diLepton.leg2().pt()>27:
           fill( tr, 'tauTriggerNewWeight_27', 1./tweight)
       else:
           fill( tr, 'tauTriggerNewWeight_27', event.tauTriggerNewWeight)

       if event.diLepton.leg2().pt()>30:
           fill( tr, 'tauTriggerNewWeight_30', 1./tweight)
       else:
           fill( tr, 'tauTriggerNewWeight_30', event.tauTriggerNewWeight)

       if event.diLepton.leg2().pt()>33:
           fill( tr, 'tauTriggerNewWeight_33', 1./tweight)
       else:
           fill( tr, 'tauTriggerNewWeight_33', event.tauTriggerNewWeight)

       if event.diLepton.leg2().pt()>36:
           fill( tr, 'tauTriggerNewWeight_36', 1./tweight)
       else:
           fill( tr, 'tauTriggerNewWeight_36', event.tauTriggerNewWeight)

       if event.diLepton.leg2().pt()>39:
           fill( tr, 'tauTriggerNewWeight_39', 1./tweight)
       else:
           fill( tr, 'tauTriggerNewWeight_39', event.tauTriggerNewWeight)

       if event.diLepton.leg2().pt()>42:
           fill( tr, 'tauTriggerNewWeight_42', 1./tweight)
       else:
           fill( tr, 'tauTriggerNewWeight_42', event.tauTriggerNewWeight)


       if event.diLepton.leg2().pt()>18:
           fill( tr, 'tauTriggerNew21Weight_18', 1./tweight)
       else:
           fill( tr, 'tauTriggerNew21Weight_18', event.tauTriggerNew21Weight)

       if event.diLepton.leg2().pt()>20:
           fill( tr, 'tauTriggerNew21Weight_20', 1./tweight)
       else:
           fill( tr, 'tauTriggerNew21Weight_20', event.tauTriggerNew21Weight)

       if event.diLepton.leg2().pt()>21:
           fill( tr, 'tauTriggerNew21Weight_21', 1./tweight)
       else:
           fill( tr, 'tauTriggerNew21Weight_21', event.tauTriggerNew21Weight)

       if event.diLepton.leg2().pt()>24:
           fill( tr, 'tauTriggerNew21Weight_24', 1./tweight)
       else:
           fill( tr, 'tauTriggerNew21Weight_24', event.tauTriggerNew21Weight)

       if event.diLepton.leg2().pt()>27:
           fill( tr, 'tauTriggerNew21Weight_27', 1./tweight)
       else:
           fill( tr, 'tauTriggerNew21Weight_27', event.tauTriggerNew21Weight)

       if event.diLepton.leg2().pt()>30:
           fill( tr, 'tauTriggerNew21Weight_30', 1./tweight)
       else:
           fill( tr, 'tauTriggerNew21Weight_30', event.tauTriggerNew21Weight)

       if event.diLepton.leg2().pt()>33:
           fill( tr, 'tauTriggerNew21Weight_33', 1./tweight)
       else:
           fill( tr, 'tauTriggerNew21Weight_33', event.tauTriggerNew21Weight)

       if event.diLepton.leg2().pt()>36:
           fill( tr, 'tauTriggerNew21Weight_36', 1./tweight)
       else:
           fill( tr, 'tauTriggerNew21Weight_36', event.tauTriggerNew21Weight)

       if event.diLepton.leg2().pt()>39:
           fill( tr, 'tauTriggerNew21Weight_39', 1./tweight)
       else:
           fill( tr, 'tauTriggerNew21Weight_39', event.tauTriggerNew21Weight)

       if event.diLepton.leg2().pt()>42:
           fill( tr, 'tauTriggerNew21Weight_42', 1./tweight)
       else:
           fill( tr, 'tauTriggerNew21Weight_42', event.tauTriggerNew21Weight)




       if event.diLepton.leg2().pt()>18:
           fill( tr, 'tauTriggerOldWeight_18', 1./tweight)
       else:
           fill( tr, 'tauTriggerOldWeight_18', event.tauTriggerOldWeight)

       if event.diLepton.leg2().pt()>20:
           fill( tr, 'tauTriggerOldWeight_20', 1./tweight)
       else:
           fill( tr, 'tauTriggerOldWeight_20', event.tauTriggerOldWeight)

       if event.diLepton.leg2().pt()>21:
           fill( tr, 'tauTriggerOldWeight_21', 1./tweight)
       else:
           fill( tr, 'tauTriggerOldWeight_21', event.tauTriggerOldWeight)

       if event.diLepton.leg2().pt()>24:
           fill( tr, 'tauTriggerOldWeight_24', 1./tweight)
       else:
           fill( tr, 'tauTriggerOldWeight_24', event.tauTriggerOldWeight)

       if event.diLepton.leg2().pt()>27:
           fill( tr, 'tauTriggerOldWeight_27', 1./tweight)
       else:
           fill( tr, 'tauTriggerOldWeight_27', event.tauTriggerOldWeight)

       if event.diLepton.leg2().pt()>30:
           fill( tr, 'tauTriggerOldWeight_30', 1./tweight)
       else:
           fill( tr, 'tauTriggerOldWeight_30', event.tauTriggerOldWeight)

       if event.diLepton.leg2().pt()>33:
           fill( tr, 'tauTriggerOldWeight_33', 1./tweight)
       else:
           fill( tr, 'tauTriggerOldWeight_33', event.tauTriggerOldWeight)

       if event.diLepton.leg2().pt()>36:
           fill( tr, 'tauTriggerOldWeight_36', 1./tweight)
       else:
           fill( tr, 'tauTriggerOldWeight_36', event.tauTriggerOldWeight)

       if event.diLepton.leg2().pt()>39:
           fill( tr, 'tauTriggerOldWeight_39', 1./tweight)
       else:
           fill( tr, 'tauTriggerOldWeight_39', event.tauTriggerOldWeight)

       if event.diLepton.leg2().pt()>42:
           fill( tr, 'tauTriggerOldWeight_42', 1./tweight)
       else:
           fill( tr, 'tauTriggerOldWeight_42', event.tauTriggerOldWeight)

       
       fillParticle(tr, 'diTau', event.diLepton)
       fillTau(tr, 'l1', event.diLepton.leg1() )
       fillEle(tr, 'l2', event.diLepton.leg2() )
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

       nBJets = len(event.cleanBJets)
       if nBJets>0:
           fillJet(tr, 'bjet1', event.cleanBJets[0] )           
       fill(tr, 'nBJets', nBJets)

       # JAN - FIXME - temporarily directly count CSVL
       # jets. Eventually apply SFs as for CSVM jets
       # after rewriting BTagSF module
       nCSVLJets = 0
       for jet in event.cleanJets:
          if jet.btag('combinedSecondaryVertexBJetTags') > 0.244:
              nCSVLJets += 1
       fill(tr, 'nCSVLJets', nCSVLJets)

       if hasattr( event, 'vbf'):
           fillVBF( tr, 'VBF', event.vbf )

       fill(tr, 'weight', event.eventWeight)
       fill(tr, 'embedWeight', event.embedWeight)
       fill(tr, 'hqtWeight', event.higgsPtWeight)
       fill(tr, 'hqtWeightUp', event.higgsPtWeightUp)
       fill(tr, 'hqtWeightDown', event.higgsPtWeightDown)
       
       if hasattr( event, 'tauFakeRateWeightUp'):
           fill(tr, 'tauFakeRateWeightUp', event.tauFakeRateWeightUp)

       if hasattr( event, 'tauFakeRateWeightDown'):
           fill(tr, 'tauFakeRateWeightDown', event.tauFakeRateWeightDown)

       if hasattr( event, 'tauFakeRateWeight'):
           fill(tr, 'tauFakeRateWeight', event.tauFakeRateWeight)

       if hasattr(event, 'NJetWeight'):
          fill(tr, 'NJetWeight', event.NJetWeight)
       fill(tr, 'zllWeight', event.zllWeight)

       if hasattr( event, 'vertexWeight'): 
          fill(tr, 'vertexWeight', event.vertexWeight)
          fill(tr, 'nVert', len(event.vertices) ) 
          
       fill(tr, 'isFake', event.isFake)
       fill(tr, 'isSignal', event.isSignal)
       fill(tr, 'leptonAccept',    event.leptonAccept)
       fill(tr, 'thirdLeptonVeto', event.thirdLeptonVeto)

       if hasattr(event, 'genParticles'):
         for p in event.genParticles:
            if p.pdgId() in [23, 25, 35, 36, 37]:
              fill(tr, 'genMass', p.mass())
              break

       if hasattr(event, 'pattern'):
           fill(tr, 'genPattern', event.pattern)

       if hasattr( event, 'genZs'):
           if len(event.genZs):
               fillGenParticle(tr, 'genZ', event.genZs[0])
               fillGenParticle(tr, 'genZleg1', event.genZs[0].leg1)
               fillGenParticle(tr, 'genZleg2', event.genZs[0].leg2)
       if hasattr( event, 'genWs'):
           if len(event.genWs):
               fillGenParticle(tr, 'genW', event.genWs[0])
               fillGenParticle(tr, 'genWlep', event.genWs[0].lep)
               fillGenParticle(tr, 'genWnu', event.genWs[0].nu)
       
       self.tree.tree.Fill()
