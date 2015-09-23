import re

from ROOT import TFile

from CMGTools.RootTools.analyzers.GenParticleAnalyzer import *
from CMGTools.RootTools.utils.DeltaR import matchObjectCollection
from CMGTools.RootTools.physicsobjects.genutils import *
from CMGTools.RootTools.statistics.Average import Average

class Generator( GenParticleAnalyzer ):
    '''Weight the event to get the NLO Higgs pT distribution for ggH events
    '''

    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(Generator,self).__init__(cfg_ana, cfg_comp, looperName)

    def beginLoop(self):
        print self, self.__class__
        super(Generator,self).beginLoop()

    def process(self, iEvent, event):
        
        result = super(Generator, self).process(iEvent, event)
        higgsBosons = [gen for gen in event.genParticles if gen.status()==3 and gen.pdgId()==25]

        if len(higgsBosons)!=1:
            strerr = '{nhiggs} Higgs bosons, this should not happen for a ggH component. Your component is:\n {comp}'.format(nhiggs=len(higgsBosons), comp=str(self.cfg_comp))
            raise ValueError(strerr)

        event.genHiggs = higgsBosons[0] 
        higgsPt = event.genHiggs.pt()

        return True

