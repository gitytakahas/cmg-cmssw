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
    def __init__(self, name):
        self.etaPhiVew = ROOT.TGraph()
        self.etaPhiVew.SetName(name)
        self.Links=[]
        self.Points=[]   
        self.particleDict = {}
        self.isHadronic = False
        self.isHadronicR = []
        self.isBrem = False
        self.isConv = False
        self.isDecay = False
        self.isIon = False

    def markerColorByType(self, pdg):

        if abs(pdg)==211:
            return ROOT.kBlack
        elif abs(pdg)==11:
            return ROOT.kAzure
        elif abs(pdg)==22:
            return ROOT.kOrange
        elif abs(pdg)==111:
            return ROOT.kMagenta
        elif abs(pdg)==15:
            return ROOT.kGreen
        else:
#            print 'Abnormal particles !', abs(pdg)
            return ROOT.kGray


    def addPoint(self, pdg, pt, ptype, R, pcounter, gcounter):

        pname = 'photon_' + str(pcounter)
        istep = 0
        line = {}

        isExistXvalue = []
        isExistYvalue = []

        save_R = 999.

        for ipdg, ipt, iptype, iR in zip(pdg, pt, ptype, R):

            isOverlap = False

            for key, value in self.particleDict.iteritems():
                for step, ivalue in value.iteritems():
                    if ivalue['pt'] == ipt and  ivalue['pdg'] == ipdg and ivalue['ptype'] == iptype:
                        isExistXvalue.append(ivalue['x1'])
                        isExistYvalue.append(ivalue['y1'])
                        isOverlap = True

            print 'Evt', gcounter, ', photon #', pcounter, ' : PDG = ', ipdg, ', pT = ', '{0:.1f}'.format(ipt), ', Type = ', iptype, 'R = ', '{0:.1f}'.format(iR), ', Overlap = ', isOverlap


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






    def viewEtaPhi(self, count):
        
        self.etaPhiView = ROOT.TCanvas('CanVas_' + count, 'CanVas_' + count, 1200, 500)
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
            
        self.etaPhiView.Update()
        self.etaPhiView.SaveAs('EventDisplay/' + self.etaPhiVew.GetName() + '.gif')
        
