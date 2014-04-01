from CMGTools.RootTools.fwlite.Analyzer import Analyzer
from ROOT import TF1, TFile

class TauTriggerWeighter( Analyzer ):
    '''Gets tau trigger efficiency weight and puts it in the event.'''

    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(TauTriggerWeighter,self).__init__(cfg_ana, cfg_comp, looperName)

        self.func = None
        self.funcold = None
        self.func21 = None
        
#        if self.cfg_comp.isMC==True and self.cfg_comp.isEmbed==False:
        if hasattr(self.cfg_ana, 'turnon'):
            self.file = TFile(self.cfg_ana.turnon)
            self.func = self.file.Get('graphTurnOnVsOfflineTauPt_L1UpgradeTau4x4_l1TauPtGt15_efficiency_fit')
            
        if hasattr(self.cfg_ana, 'oldturnon'):
            self.fileold = TFile(self.cfg_ana.oldturnon)
            self.funcold = self.fileold.Get('graphTurnOnVsOfflineTauPt_L1TauOrJet_l1TauPtGt35_efficiency_fit')

        if hasattr(self.cfg_ana, 'turnon21'):
            self.file21 = TFile(self.cfg_ana.turnon21)
            self.func21 = self.file21.Get('graphTurnOnVsOfflineTauPt_L1UpgradeTau2x1_l1TauPtGt15_efficiency_fit')

        else:
            print 'No turnon curve specified'

    def beginLoop(self):
        super(TauTriggerWeighter,self).beginLoop()

    def process(self, iEvent, event):

        event.tauTriggerNewWeight = 1.
        event.tauTriggerOldWeight = 1.
        event.tauTriggerNew21Weight = 1.

        if self.func is not None:
            taupt = event.diLepton.leg1().pt()
            event.tauTriggerNewWeight = self.func.Eval(taupt)
            
            if event.tauTriggerNewWeight > 1:
                event.tauTriggerNewWeight = 1.
        else:
            pass

        if self.func21 is not None:
            taupt = event.diLepton.leg1().pt()
            event.tauTriggerNew21Weight = self.func21.Eval(taupt)
            
            if event.tauTriggerNew21Weight > 1:
                event.tauTriggerNew21Weight = 1.
        else:
            pass

        if self.funcold is not None:
            taupt = event.diLepton.leg1().pt()
            event.tauTriggerOldWeight = self.funcold.Eval(taupt)
            
            if event.tauTriggerOldWeight > 1:
                event.tauTriggerOldWeight = 1.
        else:
            pass

        return True
                
