import ROOT
import math
import copy

ROOT.gStyle.SetFrameLineWidth (2)
ROOT.gStyle.SetPadLeftMargin  (0.1)
ROOT.gStyle.SetPadRightMargin (0.07)
ROOT.gStyle.SetPadBottomMargin (0.12)
ROOT.gStyle.SetTitleSize(0.05,"X")
ROOT.gStyle.SetTitleSize(0.05,"Y")
ROOT.gStyle.SetLabelSize(0.05,"X")
ROOT.gStyle.SetLabelSize(0.05,"Y")
ROOT.gStyle.SetNdivisions(506)
ROOT.gStyle.SetTitleOffset(1.3,"Y")

def LegendSettings(leg):
#    leg.SetNColumns(7)
    leg.SetBorderSize(0)
    leg.SetFillColor(10)
    leg.SetLineColor(0)
    leg.SetFillStyle(0)
    leg.SetTextSize(0.04)
    leg.SetTextFont(42)

def returnPDG(id):
    if abs(id)==211: return 0
    elif abs(id)==11: return 1
    elif abs(id)==22: return 2
    elif abs(id) in [2212, 2112]:
        return 3
    else:
        print 'abnormal pdg ID = ', id
        return 4

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


class DisplayManager(object):
    def __init__(self, name, iso):
        self.etaPhiVew = ROOT.TGraph()
        self.etaPhiVew.SetName(name)
        self.iso = iso
        self.Links=[]
        self.Points=[] 
        self.lastPoints=[]
        self.lastPointsText=[]
        self.particleDict = {}
        self.Legend = ROOT.TLegend(0.12,0.93,0.85,0.99)
        LegendSettings(self.Legend)
        self.isPion = False
        self.isElectron = False
        self.isPhoton = False
        self.isPiZero = False
        self.isTau = False
        self.isPN = False
        self.isOthers = False
        self.Ncolumn = 0
        self.isHadronic = False
        self.isHadronicR = []
        self.isBrem = False
        self.isConv = False
        self.isDecay = False
        self.isIon = False
        self.isN = 0
        self.gammaStored = []

    def markerColorByType(self, pdg):


        if abs(pdg)==211:
            if self.isPion == False:
                self.Legend.AddEntry(self.Links[-1], 'charged #pi^{#pm}', 'l')
                self.isPion = True
                self.Ncolumn += 1
            return ROOT.kBlack

        elif abs(pdg)==11:
            if self.isElectron == False:
                self.Legend.AddEntry(self.Links[-1], 'electron', 'l')
                self.isElectron = True
                self.Ncolumn += 1
            return ROOT.kAzure

        elif abs(pdg)==22:

            if self.isPhoton == False:
                self.Legend.AddEntry(self.Links[-1], 'photon', 'l')
                self.isPhoton = True
                self.Ncolumn += 1
            return ROOT.kOrange

        elif abs(pdg)==111:
            if self.isPiZero == False:
                self.Legend.AddEntry(self.Links[-1], 'neutral #pi^{0}', 'l')
                self.isPiZero = True
                self.Ncolumn += 1
            return ROOT.kMagenta

        elif abs(pdg)==15:
            if self.isTau == False:
                self.Legend.AddEntry(self.Links[-1], '#tau', 'l')
                self.isTau = True
                self.Ncolumn += 1
            return ROOT.kGreen

        elif abs(pdg)==2112 or abs(pdg)==2212:

            if self.isPN == False:
                self.Legend.AddEntry(self.Links[-1], 'proton / neutron', 'l')
                self.isPN = True
                self.Ncolumn += 1
            return 46

        else:
            if self.isOthers == False:
                self.Legend.AddEntry(self.Links[-1], 'others', 'l')
                self.isOthers = True
                self.Ncolumn += 1
#            print 'Abnormal particles !', abs(pdg)
            return ROOT.kGray


    def addPoint(self, pdg, pt, ptype, R, pcounter, gcounter, gamma_pt, gamma_eta, gamma_phi):

        pname = 'photon_' + str(pcounter)
        istep = 0
        line = {}

        isExistXvalue = []
        isExistYvalue = []
        max_x = []
        max_y = []

        save_R = R[0]

        self.isN = pcounter

        for ipdg, ipt, iptype, iR in zip(pdg, pt, ptype, R):

            isOverlap = False

            for key, value in self.particleDict.iteritems():
                for step, ivalue in value.iteritems():
                    if ivalue['pt'] == ipt and  ivalue['pdg'] == ipdg and ivalue['ptype'] == iptype:
                        isExistXvalue.append(ivalue['x1'])
                        isExistYvalue.append(ivalue['y1'])
                        isOverlap = True
                        save_R = ivalue['save_R']
                        
            print 'Evt', gcounter, ', photon #', pcounter, ' : PDG = ', ipdg, ', pT = ', '{0:.1f}'.format(ipt), ', Type = ', iptype, 'R = ', '{0:.1f}'.format(iR), 'previous R = ', '{0:.1f}'.format(save_R),  ', Overlap = ', isOverlap


#            print isExistXvalue
#            print isExistYvalue
#            import pdb; pdb.set_trace()

#            print ipdg, ipt, iptype, '=> Found overlap ', isOverlap

            if isOverlap == False:
                self.Links.append(ROOT.TGraph())   

                _x0_ = -1
                _y0_ = -1
                _x1_ = -1
                _y1_ = -1

                if len(isExistYvalue)==0:
                    self.Links[-1].SetPoint(0, istep, pcounter)
                    self.Links[-1].SetPoint(1, istep + 1, pcounter)
                    _x0_ = istep
                    _y0_ = pcounter
                    _x1_ = istep + 1
                    _y1_ = pcounter

                else:
                    self.Links[-1].SetPoint(0, max(isExistXvalue), isExistYvalue[isExistXvalue.index(max(isExistXvalue))])
                    self.Links[-1].SetPoint(1, max(isExistXvalue)+1, pcounter)

                    _x0_ = max(isExistXvalue)
                    _y0_ = isExistYvalue[isExistXvalue.index(max(isExistXvalue))]
                    _x1_ = max(isExistXvalue) + 1
                    _y1_ = pcounter

                    isExistXvalue.append(max(isExistXvalue)+1)
                    isExistYvalue.append(pcounter)


                max_x.append(_x1_)
                max_y.append(_y1_)

                color = self.markerColorByType(ipdg)
                self.Links[-1].SetLineWidth(2)
                self.Links[-1].SetMarkerStyle(20)
                self.Links[-1].SetMarkerSize(1)
                self.Links[-1].SetLineColor(color)


                ename = 'step_' + str(istep)
                line[ename] = {'pt':ipt,
                                'pdg':ipdg,
                                'ptype':iptype,
                                'R':iR,
                               'save_R':save_R,
                                'x0':_x0_,
                                'x1':_x1_,
                                'y0':_y0_,
                                'y1':_y1_}



                _str_ = "unknown"
                if iptype == 0:
                    _str_ = 'Primary' #+ '{0:.1f}'.format(iR)
                elif iptype == 121:
                    _str_ = '#color[2]{Had.}' #+ '{0:.1f}'.format(iR)
                    self.isHadronic = True
                    self.isHadronicR.append(save_R)
                elif iptype == 201:
#                    _str_ = '#color[3]{Decay}'
                    _str_ = 'Decay'
                    self.isDecay = True
                elif iptype == 14:
                    _str_ = 'Conv.'
                    self.isConv = True
                elif iptype == 3:
                    _str_ = 'Brems'
                    self.isBrem = True
                elif iptype == 2:
                    _str_ = 'Ionization'
                    self.isIon = True
                else:
                    print 'iptype = ', iptype

                self.Points.append(ROOT.TLatex(_x0_-0.2, _y0_ - 0.5, _str_))
                self.Points[-1].SetTextFont(42)
                self.Points[-1].SetTextSize(0.03)



                istep+=1
                save_R = iR

        self.particleDict[pname] = line


#        print 'max_x', max_x, 'max_y', max_y
        if len(max_x) >= 1:
            self.lastPoints.append(ROOT.TEllipse(max(max_x), max(max_y), 0.07,0.2))
            self.lastPoints[-1].SetFillStyle(1)
            self.lastPoints[-1].SetFillColor(ROOT.kYellow)

            ptetaphi = '{0:.1f}'.format(gamma_pt) + ' GeV, (#eta, #phi) = ' + '{0:.1f}'.format(gamma_eta) + ', ' + '{0:.1f}'.format(gamma_phi)

            self.lastPointsText.append(ROOT.TLatex(max(max_x) + 0.2, max(max_y)-0.2, ptetaphi))
            self.lastPointsText[-1].SetTextFont(42)
            self.lastPointsText[-1].SetTextSize(0.04)

            self.gammaStored.append([gamma_pt, gamma_eta, gamma_phi])

    def returnGamma(self):
        return self.gammaStored

    def viewEtaPhi(self, name):
        
        self.etaPhiView = ROOT.TCanvas('CanVas_' + name, 'CanVas_' + name, 1200, 500)
        self.etaPhiView.cd()

        frame = self.etaPhiView.DrawFrame(-1, -1, 10, 10)
        frame.GetXaxis().SetTitle("# of process")
#        frame.GetYaxis().SetTitle("# photon")
        self.etaPhiView.Draw()
        self.etaPhiView.cd()    
        

        for link in self.Links:
            link.Draw("Lpsame")            

        for point in self.Points:
            point.Draw("")            

        for point in self.lastPoints:
            point.Draw("")            

        for point in self.lastPointsText:
            point.Draw("")            

        self.Legend.SetNColumns(self.Ncolumn)
        self.Legend.Draw("")

        label = ROOT.TLatex(8.8, 10.5, 'event : ' + name)
        label.SetTextFont(42)
        label.Draw()

        label2 = ROOT.TLatex(7.5, 8.6, '#sum p_{T}^{#gamma, iso} : ' + '{0:.1f}'.format(self.iso) + ' GeV');
        label2.SetTextFont(42)
        label2.Draw()
        
        self.etaPhiView.Update()
        self.etaPhiView.SaveAs('EventDisplay/display_' + name + '.pdf')
        self.etaPhiView.SaveAs('EventDisplay/display_' + name + '.gif')
        
