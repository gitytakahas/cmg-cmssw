import ROOT
import math
import copy

# Based on initial code by Michalis Bachtis


ROOT.gStyle.SetFrameLineWidth (2)
ROOT.gStyle.SetPadLeftMargin  (0.15)
ROOT.gStyle.SetPadRightMargin (0.07)
ROOT.gStyle.SetTitleSize(0.05,"X")
ROOT.gStyle.SetTitleSize(0.05,"Y")
ROOT.gStyle.SetLabelSize(0.05,"X")
ROOT.gStyle.SetLabelSize(0.05,"Y")
ROOT.gStyle.SetNdivisions(506)
ROOT.gStyle.SetTitleOffset(1.3,"Y")

def deltaR2( e1, p1, e2, p2):
    de = e1 - e2
    dp = deltaPhi(p1, p2)
    return de*de + dp*dp


def deltaR( *args ):
    return math.sqrt( deltaR2(*args) )


def deltaPhi( p1, p2):
    '''Computes delta phi, handling periodic limit conditions.'''
    res = p1 - p2
    while res > math.pi:
        res -= 2*math.pi
    while res < -math.pi:
        res += 2*math.pi
    return res


def dmname(dm):
    if dm==0:
        return 'OneProng0PiZero'
    elif dm==1:
        return 'OneProng1PiZero'
    elif dm==2:
        return "OneProng2PiZero"
    elif dm==3:
        return "OneProng3PiZero"
    elif dm==4:
        return "OneProngNPiZero"
    elif dm==5:
        return "TwoProng0PiZero"
    elif dm==6:
        return "TwoProng1PiZero"
    elif dm==7:
        return "TwoProng2PiZero"
    elif dm==8:
        return "TwoProng3PiZero"
    elif dm==9:
        return "TwoProngNPiZero"
    elif dm==10:
        return "ThreeProng0PiZero"
    elif dm==11:
        return "ThreeProng1PiZero"
    elif dm==12:
        return "ThreeProng2PiZero"
    elif dm==13:
        return "ThreeProng3PiZero"
    elif dm==14:
        return "ThreeProngNPiZero"
    elif dm==15:
        return "RareDecayMode"
    else:
        return "Unknown"


def p4sumvis(particles):
    visparticles = [p for p in particles if abs(p.pdgId()) not in [12, 14, 16]]
    p4 = visparticles[-1].p4() if particles else 0.
    visparticles.pop()
    for p in visparticles:
        p4 += p.p4()
    return p4

def finalDaughters(particle, daughters):
    '''Fills daughters with all the daughters of particle.
    Recursive function.'''
    if particle.numberOfDaughters() == 0:
        daughters.append(particle)
    else:
        foundDaughter = False
        for i in range( particle.numberOfDaughters() ):
            dau = particle.daughter(i)
            if dau.status() >= 1:
                daughters = finalDaughters( dau, daughters )
                foundDaughter = True
        if not foundDaughter:
            daughters.append(particle)

    return daughters



def returnGenDecayMode(TauDaughters):

    nphoton = len([p for p in TauDaughters if abs(p.pdgId())==22])
#    nmuon = len([p for p in TauDaughters if abs(p.pdgId())==13])
#    nelectron = len([p for p in TauDaughters if abs(p.pdgId())==11])
    npion = len([p for p in TauDaughters if abs(p.pdgId())==211])

#    if nmuon==1: return 'muon',-1,nphoton, npion
#    elif nelectron == 1 : return 'electron',-2,nphoton, npion
    
    if npion==1:
        if nphoton == 0 : return 'oneProng0Pi0',0,nphoton, npion
        elif nphoton == 2 : return 'oneProng1Pi0',1,nphoton, npion
        elif nphoton == 4 : return 'oneProng2Pi0',2,nphoton, npion
        elif nphoton == 6 : return 'oneProng3Pi0',3,nphoton, npion
        elif nphoton == 8 : return 'oneProng4Pi0',4,nphoton, npion
        else: return 'oneProngOther',-3,nphoton, npion
    elif npion==3:
        if nphoton == 0 : return 'threeProng0Pi0', 10,nphoton, npion
        elif nphoton == 2 : return 'threeProng1Pi0', 11,nphoton, npion
        elif nphoton == 4 : return 'threeProng2Pi0', 12,nphoton, npion
        elif nphoton == 6 : return 'threeProng3Pi0', 13,nphoton, npion
        else: return 'threeProngOther', -4,nphoton, npion
    else:
        return 'rare', -5,nphoton, npion





class DisplayManager(object):
    def __init__(self,name,eta,phi,radius=0.5):
        self.etaPhiVew = ROOT.TGraph()
        self.etaPhiVew.SetName(name)
        self.rechits=[]
        self.genParticles=[]
        self.photons=[]
        self.CH=[]
        self.tracks=[]
        self.clusters=[]
        self.clusterLinks=[]
        self.recoTau=[]
        self.etaCenter=eta
        self.phiCenter=phi
        self.radius=radius
        self.name=name

    def markerByType(self,particle):
        if particle.pdgId()==22:
            return 20
        elif abs(particle.pdgId())==11:
            return 3
        elif abs(particle.pdgId())==13:
            return 5
#        elif particle.charge()!=0:
        elif abs(particle.pdgId())==211:
            return 21
        elif particle.charge()!=0:
            print 'charged particle = ', particle.pdgId(), particle.status()
            return 27
        elif particle.charge()==0:
            print 'neutral particle = ', particle.pdgId(), particle.status()
            return 25
        else:
            return -1

        
    def addRecHit(self,recHit,depth=1,fraction=1):
        if deltaR(recHit.position().Eta(),recHit.position().Phi(),self.etaCenter,self.phiCenter)>self.radius:
            return

        
        corners=[]
        for corner in recHit.getCornersXYZ():
            corners.append({'eta':corner.Eta(),'phi':corner.Phi(),'rho':corner.Rho()})


        rechit={'corners':corners,'energy':recHit.energy()*fraction,'depth':depth}
        self.rechits.append(rechit)

    def addCluster(self,cluster,links=False,linkMinFraction=0.2):
        if deltaR(cluster.position().Eta(),cluster.position().Phi(),self.etaCenter,self.phiCenter)>self.radius:
            return
        self.clusters.append(ROOT.TGraph())
        self.clusters[-1].SetPoint(0,cluster.position().Eta(),cluster.position().Phi())
        self.clusters[-1].SetMarkerStyle(20)
        self.clusters[-1].SetMarkerColor(ROOT.kViolet)

#        import pdb; pdb.set_trace()
        print '\t\t\t cluster : eta = ', cluster.position().Eta(), ', phi = ', cluster.position().Phi(), ', energy = ', cluster.energy()

        if links:
            for fraction in cluster.recHitFractions():
                if fraction.fraction() > linkMinFraction: #JAN - add minimum fraction
                    self.clusterLinks.append(ROOT.TGraph())
                    self.clusterLinks[-1].SetPoint(0,cluster.position().Eta(),cluster.position().Phi())
                    self.clusterLinks[-1].SetPoint(1,fraction.recHitRef().position().Eta(),fraction.recHitRef().position().Phi())
                    self.clusterLinks[-1].SetLineColor(ROOT.kViolet)
                



    def addTrack(self,track):
        N = track.nTrajectoryPoints()
        if deltaR(track.trackRef().innerMomentum().Eta(),track.trackRef().innerMomentum().Phi(),self.etaCenter,self.phiCenter)>self.radius:
            return
        self.tracks.append(ROOT.TGraph())
        ii=0
        self.tracks[-1].SetPoint(ii,track.trackRef().innerMomentum().Eta(),track.trackRef().innerMomentum().Phi())
        ii=ii+1
        for i,point in enumerate(track.trajectoryPoints()):
            print 'Seeing point', point.position().Eta(),point.position().Phi()
            if point.position().Eta() !=0.0 and point.position().Phi()!=0 and i>2:
                self.tracks[-1].SetPoint(ii,point.position().Eta(),point.position().Phi())
                print 'Added',ii 
                ii=ii+1
        self.tracks[-1].SetMarkerStyle(7)

        

    def addGenParticle(self,particle):
        if deltaR(particle.eta(),particle.phi(),self.etaCenter,self.phiCenter)>self.radius:
            return

        marker = self.markerByType(particle)
        if marker<0:
            print 'Unknown particle Type',particle.pdgId()
            return
        
        self.genParticles.append(ROOT.TGraph(1))
        self.genParticles[-1].SetPoint(0,particle.eta(),particle.phi())
        self.genParticles[-1].SetMarkerStyle(marker)
#        self.genParticles[-1].SetMarkerColor(ROOT.kAzure)
        self.genParticles[-1].SetMarkerColor(ROOT.kMagenta)
        

    def addPhoton(self,particle, col=1):
        if deltaR(particle.eta(),particle.phi(),self.etaCenter,self.phiCenter)>self.radius:
            return

        self.photons.append(ROOT.TGraph(1))
        self.photons[-1].SetPoint(0,particle.eta(),particle.phi())
        self.photons[-1].SetMarkerStyle(24)
        self.photons[-1].SetMarkerColor(col)


    def addCH(self,particle, col=1):
        if deltaR(particle.eta(),particle.phi(),self.etaCenter,self.phiCenter)>self.radius:
            return

        self.CH.append(ROOT.TGraph(1))
        self.CH[-1].SetPoint(0,particle.eta(),particle.phi())
        self.CH[-1].SetMarkerStyle(25)
        self.CH[-1].SetMarkerColor(col)

    def addRecoTau(self, particle):
        
        rcircle = max(0.05, min(0.10, 3.0/particle.pt()))
        
        self.recoTau.append(ROOT.TEllipse(particle.eta(), particle.phi(), rcircle, rcircle))
        self.recoTau[-1].SetFillStyle(0)
        self.recoTau[-1].SetLineColor(ROOT.kAzure)
        self.recoTau[-1].SetLineStyle(2)
        self.recoTau[-1].SetLineWidth(2)


        self.recoTau.append(ROOT.TEllipse(particle.eta(), particle.phi(), 0.5, 0.5))
        self.recoTau[-1].SetFillStyle(0)
        self.recoTau[-1].SetLineColor(ROOT.kAzure)
        self.recoTau[-1].SetLineStyle(2)
        self.recoTau[-1].SetLineWidth(2)


    def scaleRecHit(self,hit,fraction):
        newHit = copy.deepcopy(hit)
        corners=[ROOT.TVector2(hit['corners'][0]['eta'],hit['corners'][0]['phi']), \
                 ROOT.TVector2(hit['corners'][1]['eta'],hit['corners'][1]['phi']), \
                 ROOT.TVector2(hit['corners'][2]['eta'],hit['corners'][2]['phi']), \
                 ROOT.TVector2(hit['corners'][3]['eta'],hit['corners'][3]['phi'])]

        centerOfGravity = (corners[0]+corners[1]+corners[2]+corners[3])
        centerOfGravity*=0.25
        radialVectors=[(corners[0]-centerOfGravity),\
                       (corners[1]-centerOfGravity),\
                       (corners[2]-centerOfGravity),\
                       (corners[3]-centerOfGravity)]


        for i in range(0,4):
            radialVectors[i]*=fraction
            newHit['corners'][i]['eta'] = (radialVectors[i]+centerOfGravity).X()
            newHit['corners'][i]['phi'] = (radialVectors[i]+centerOfGravity).Y()
        return newHit    
                       

    def viewEtaPhi(self, label='', fname='', counter=0, nIso=0):
        
        self.etaPhiView = ROOT.TCanvas(self.name+'etaPhiCaNVAS',self.name, 700,700)
        self.etaPhiView.cd()
        frame=self.etaPhiView.DrawFrame(self.etaCenter-self.radius,self.phiCenter-self.radius,self.etaCenter+self.radius,self.phiCenter+self.radius) 
        frame.GetXaxis().SetTitle("#eta")
        frame.GetYaxis().SetTitle("#phi")
        self.etaPhiView.Draw()
        self.etaPhiView.cd()    
        self.geolines=[]
        self.hitlines=[]
        
        #sort hits by energy
        self.rechits=sorted(self.rechits,key=lambda x: x['energy'],reverse=True)

        #first draw boundaries and calculate fractions at the same time
        
        for hit in self.rechits:
            self.geolines.append(ROOT.TGraph(5))
            self.hitlines.append(ROOT.TGraph(5))
            fraction = hit['energy']/self.rechits[0]['energy']
            for (i,corner) in enumerate(hit['corners']):
                self.geolines[-1].SetPoint(i,corner['eta'],corner['phi'])

            scaledHit = self.scaleRecHit(hit,fraction)
            for (i,corner) in enumerate(scaledHit['corners']):
                self.hitlines[-1].SetPoint(i,corner['eta'],corner['phi'])
            


            self.geolines[-1].SetPoint(4,hit['corners'][0]['eta'],hit['corners'][0]['phi'])
            self.hitlines[-1].SetPoint(4,scaledHit['corners'][0]['eta'],scaledHit['corners'][0]['phi'])

            self.geolines[-1].SetLineColor(ROOT.kGray)
            self.geolines[-1].SetLineStyle(hit['depth'])
            self.geolines[-1].Draw("Lsame")
            if hit['depth'] ==1:
#                self.hitlines[-1].SetLineColor(ROOT.kRed)
                self.hitlines[-1].SetLineColor(38)
            elif hit['depth'] ==2:
                self.hitlines[-1].SetLineColor(ROOT.kGreen)
            elif hit['depth'] ==3:
                self.hitlines[-1].SetLineColor(ROOT.kMagenta)
            elif hit['depth'] ==4:
                self.hitlines[-1].SetLineColor(ROOT.kYellow)
            elif hit['depth'] ==5:
                self.hitlines[-1].SetLineColor(ROOT.kBlue)
            self.hitlines[-1].SetLineWidth(2)
            self.hitlines[-1].Draw("Lsame")



        for particle in self.genParticles:
            particle.Draw("Psame")

        for tau in self.recoTau:
            tau.Draw("")

        for track in self.tracks:
            track.Draw("PLsame")

        for cluster in self.clusters:
            cluster.Draw("Psame")
        for link in self.clusterLinks:
            link.Draw("Lsame")            
            
        for particle in self.photons:
            particle.Draw("Psame")
                
        for particle in self.CH:
            particle.Draw("Psame")

        _str_ = label.replace('PiZero','#pi^{0}').replace('Three','3').replace('One','1').replace('Two','2').replace('Prong','prong, ').replace('one','1').replace('three','3').replace('Pi0','#pi^{0}')
#        print _str_

        self.tex = ROOT.TLatex(self.etaCenter-self.radius, self.phiCenter+self.radius + 0.05, _str_);

        self.tex.SetTextFont(42)
        self.tex.SetTextSize(0.045)
        self.tex.Draw()

        self.etex = ROOT.TLatex(self.etaCenter+self.radius - 0.15, self.phiCenter+self.radius + 0.04, 'evt : ' + str(counter));

        self.etex.SetTextFont(42)
        self.etex.SetTextSize(0.03)
        self.etex.Draw()


        self.ntex = ROOT.TLatex(self.etaCenter+self.radius - 0.35, self.phiCenter+self.radius - 0.1, '#sum p_{T}^{#gamma, iso} : ' + '{0:.1f}'.format(nIso) + ' GeV');

        self.ntex.SetTextFont(42)
        self.ntex.SetTextSize(0.03)
        self.ntex.Draw()


        self.etaPhiView.Update()
        self.etaPhiView.SaveAs('event_display/' + fname + '.gif')
        self.etaPhiView.SaveAs('event_display/' + fname + '.pdf')
        
