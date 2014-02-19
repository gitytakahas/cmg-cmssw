import operator
from CMGTools.RootTools.analyzers.DiLeptonAnalyzer import DiLeptonAnalyzer
from CMGTools.RootTools.fwlite.AutoHandle import AutoHandle
from CMGTools.RootTools.physicsobjects.DiObject import MuonElectron
#from CMGTools.RootTools.physicsobjects.PhysicsObjects import Electron
from CMGTools.RootTools.physicsobjects.HTauTauElectron import HTauTauElectron as Electron
from CMGTools.RootTools.physicsobjects.PhysicsObjects import Muon, GenParticle
from CMGTools.RootTools.utils.DeltaR import deltaR

class MuEleAnalyzer( DiLeptonAnalyzer ):

    DiObjectClass = MuonElectron
    #COLIN what should I do for the di-lepton veto?? None I guess
    LeptonClass = Muon
    OtherLeptonClass = Electron
    
    def declareHandles(self):
        super(MuEleAnalyzer, self).declareHandles()

        self.handles['diLeptons'] = AutoHandle(
            'cmgMuEleCorSVFitFullSel',
            'std::vector<cmg::DiTauObject<cmg::Muon ,cmg::Electron>>'
            )
        self.handles['leptons'] = AutoHandle(
            'cmgMuonSel',
            'std::vector<cmg::Muon>'
            )

        self.handles['otherLeptons'] = AutoHandle(
            'cmgElectronSel',
            'std::vector<cmg::Electron>'
            )

        self.mchandles['genParticles'] = AutoHandle( 'genParticlesPruned',
                                                     'std::vector<reco::GenParticle>' )


    def buildDiLeptons(self, cmgDiLeptons, event):
        '''Build di-leptons, associate best vertex to both legs,
        select di-leptons with a tight ID muon.
        The tight ID selection is done so that dxy and dz can be computed
        (the muon must not be standalone).
        '''
        diLeptons = []
        for index, dil in enumerate(cmgDiLeptons):
            pydil = self.__class__.DiObjectClass(dil)
            pydil.leg1().associatedVertex = event.goodVertices[0]
            pydil.leg2().associatedVertex = event.goodVertices[0]
            if not self.testLeg2( pydil.leg2(), 99999 ):
                continue
            pydil.mvaMetSig = mvaMetSig = dil.metSig()
            diLeptons.append( pydil )
        return diLeptons


    def buildLeptons(self, cmgLeptons, event):
        '''Build muons for veto, associate best vertex, select loose ID muons.
        The loose ID selection is done to ensure that the muon has an inner track.'''
        leptons = []
        for index, lep in enumerate(cmgLeptons):
            pyl = self.__class__.LeptonClass(lep)
            pyl.associatedVertex = event.goodVertices[0]
            leptons.append( pyl )
        return leptons


    def buildOtherLeptons(self, cmgOtherLeptons, event):
        '''Build electrons for third lepton veto, associate best vertex.
        '''
        otherLeptons = []
        for index, lep in enumerate(cmgOtherLeptons):
            pyl = self.__class__.OtherLeptonClass(lep)
            pyl.associatedVertex = event.goodVertices[0]
            otherLeptons.append( pyl )
        return otherLeptons


    def process(self, iEvent, event):

#        import pdb; pdb.set_trace()
        # First, run over the parent dilepton object
        result = super(MuEleAnalyzer, self).process(iEvent, event)

        # Second, check the trigger path
#        print 'type_check -> ', type(event.diLepton)
        if hasattr(event, 'diLepton')==False:
            return False
        
#        import pdb; pdb.set_trace()
#        if len(event.diLepton):
#            return False

    #            print '[WARNING] No dilepton object is found'
#            return False

        print 'HLT path = ', event.hltPath
#        import pdb; pdb.set_trace();

        if event.hltPath.find('HLT_Mu8_Ele17_CaloId')!=-1:
            if not (event.diLepton.leg1().pt() > 10. and event.diLepton.leg2().pt() > 20.):
                return False
            
        elif event.hltPath.find('HLT_Mu17_Ele8_CaloId')!=-1:
            if not (event.diLepton.leg1().pt() > 20. and event.diLepton.leg2().pt() > 10.):
                return False
        else:
            print 'Wrong trigger information. Returning false : ', event.hltPath
            return False


#        print 'check -> ', event.leptons, event.otherLeptons, event.diLepton
        if self.triLeptonVeto(event.leptons, event.otherLeptons, event.diLepton)==False:
            print 'There find third lepton ... veto !'
            return False

        if self.dimuonVeto(event.leptons, event.diLepton)==False:
             print 'There find another dimuon ... veto !'
             return False
        
        
        if result is False:
            result = self.selectionSequence(event, fillCounter=False,
                                            leg1IsoCut = -9999,
                                            leg2IsoCut = 9999)
            if result is False:
                # really no way to find a suitable di-lepton,
                # even in the control region
                return False
            event.isSignal = False
        else:
            event.isSignal = True
       
        event.genMatched = None
        if self.cfg_comp.isMC:

            genParticles = self.mchandles['genParticles'].product()
            event.genParticles = map( GenParticle, genParticles)
            leg1DeltaR, leg2DeltaR = event.diLepton.match( event.genParticles ) 
            if leg1DeltaR>-1 and leg1DeltaR < 0.1 and \
               leg2DeltaR>-1 and leg2DeltaR < 0.1:
                event.genMatched = True
            else:
                event.genMatched = False
                
        return True





# Yuta
# This is for tau
#    def testLeg1ID(self, tau):
#        if tau.decayMode() == 0 and \
#               tau.calcEOverP() < 0.2: #reject muons faking taus in 2011B
#            return False
#        #return tau.tauID("againstMuonTight2")>0.5 and \
#        # JAN: revert back to old muon rejection (Jose HN)
#        return tau.tauID("againstMuonTight")>0.5 and \
#               tau.tauID("againstElectronLoose")>0.5 and \
#               self.testVertex( tau )
        

#    def testLeg1Iso(self, tau, isocut):
#        '''if isocut is None, returns true if three-hit iso cut is passed.
#        Otherwise, returns true if iso MVA > isocut.'''
#        if isocut is None:
#            return tau.tauID('byCombinedIsolationDeltaBetaCorrRaw3Hits') < 1.5
#        else:
#            return tau.tauID("byRawIsoMVA")>isocut


    def testVertex(self, lepton):
        '''Tests vertex constraints, for mu and tau'''
#        return abs(lepton.dxy()) < 0.045 and \
#        TauMu -> d0 < 0.045, MuEle -> d0 < 0.02
        return abs(lepton.dxy()) < 0.02 and \
               abs(lepton.dz()) < 0.2 

    def testVertexNormal(self, lepton):
        '''Tests vertex constraints, for mu and tau'''
#        return abs(lepton.dxy()) < 0.045 and \
#        TauMu -> d0 < 0.045, MuEle -> d0 < 0.02
        return abs(lepton.dxy()) < 0.045 and \
               abs(lepton.dz()) < 0.2 



    def testLeg1ID(self, muon):
        '''Tight muon selection'''
        return muon.tightId() and \
               self.testVertex( muon )
               

    def testLeg1Iso(self, muon, isocut):
        '''Tight muon selection, with isolation requirement'''
        if isocut is None:
            isocut = self.cfg_ana.iso1

        if abs(muon.eta() > 1.479):
            return muon.relIsoAllChargedDB05()<isocut
        else:
            return muon.relIsoAllChargedDB05()<isocut + 0.05


    def testLeg2ID(self, electron):
        '''Tight electron selection'''
        return electron.tightId() and \
               self.testVertex( electron )

    def testLeg2Iso(self, leg, isocut): #electron
        '''Tight electron selection, with isolation requirement'''
        if isocut is None:
           isocut = self.cfg_ana.iso2

        if abs(leg.eta() > 1.479):
            return leg.relIsoAllChargedDB05()<isocut
        else:
            return leg.relIsoAllChargedDB05()<isocut + 0.05

        

    def triLeptonVeto(self, leptons, otherLeptons, diLepton, ptcut = 10, isocut = 0.3):
        '''The tri-lepton veto. returns False if > 2 leptons (e or mu).'''
        # count muons
        vleptons = [lep for lep in leptons if
                    self.testLegKine(lep, ptcut=ptcut, etacut=2.4) and 
                    self.testLeg1ID(lep) and
                    self.testVertexNormal(lep) and
                    lep.relIsoAllChargedDB05() < isocut and
                    deltaR(diLepton.leg1().eta(), diLepton.leg1().phi(), lep.eta(), lep.phi()) > 0.3 and
                    deltaR(diLepton.leg2().eta(), diLepton.leg2().phi(), lep.eta(), lep.phi()) > 0.3
                    ]

        # count electrons
        votherLeptons = [olep for olep in otherLeptons if 
                         self.testLegKine(olep, ptcut=ptcut, etacut=2.5) and \
                         olep.looseIdForTriLeptonVeto()           and \
                         self.testVertexNormal( olep )           and \
                         olep.relIsoAllChargedDB05() < isocut and \
                         deltaR(diLepton.leg1().eta(), diLepton.leg1().phi(), olep.eta(), olep.phi()) > 0.3 and
                         deltaR(diLepton.leg2().eta(), diLepton.leg2().phi(), olep.eta(), olep.phi()) > 0.3
                        ]

#        print 'veto_lepton, veto_otherlepton', len(vleptons), len(votherLeptons)            

        if len(vleptons) + len(votherLeptons)> 1:
            return False
        else:
            return True
        
    def dimuonVeto(self, leptons, diLepton):
        '''The di-lepton veto, returns false if > one lepton.
        e.g. > 1 mu in the mu tau channel'''

#        for imuon in leptons:
#            dr = deltaR(diLepton.leg2().eta(), diLepton.leg2().phi(),
#                        imuon.eta(), imuon.phi())
           
#            print 'check :', 'pT = ', imuon.pt(), dr
           
        looseLeptons = [muon for muon in leptons if
                        self.testLegKine(muon, ptcut=3, etacut=2.4) and
                        deltaR(diLepton.leg2().eta(), diLepton.leg2().phi(),
                               muon.eta(), muon.phi()) < 0.3
#                        muon.isGlobalMuon() and
#                        muon.isTrackerMuon() and
#                        muon.sourcePtr().userFloat('isPFMuon') and
                       #COLIN Not sure this vertex cut is ok... check emu overlap
                       #self.testVertex(muon) and
                       # JAN: no dxy cut
#                        abs(muon.dz()) < 0.2 and
#                        self.testLeg2Iso(muon, 0.3)
                        ]

        if len(looseLeptons) > 0:
            print '# of loose leptons = ', len(looseLeptons), 'found'
            return False
        else:
            return True

#        isPlus = False
#        isMinus = False
        # import pdb; pdb.set_trace()
#        for lepton in looseLeptons:
#            if lepton.charge()<0: isMinus=True
#            elif lepton.charge()>0: isPlus=True
#            else:
#                raise ValueError('Impossible!')
#        veto = isMinus and isPlus
#        return not veto


    def bestDiLepton(self, diLeptons):
        '''Returns the best diLepton (1st precedence opposite-sign, 2nd precedence
        highest pt1 + pt2).'''
        # # FIXME - temporary TEST for bias
        # return max( diLeptons, key=operator.methodcaller( 'sumPt' ) )
        osDiLeptons = [dl for dl in diLeptons if dl.leg1().charge() != dl.leg2().charge()]
        if osDiLeptons:
            return max( osDiLeptons, key=operator.methodcaller( 'sumPt' ) )
        else:
            return max( diLeptons, key=operator.methodcaller( 'sumPt' ) )


