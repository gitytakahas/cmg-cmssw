import ROOT, os, numpy, copy
#from officialStyle import officialStyle
from ROOT import TLegend, TCanvas, TFile, TTree, TH1F, TColor, kMagenta, kOrange, kRed, kBlue, kGray, kBlack
from CMGTools.RootTools.DataMC.DataMCPlot import DataMCPlot
from CMGTools.H2TauTau.proto.plotter.officialStyle import officialStyle
import math

ROOT.gROOT.SetBatch(True)
officialStyle(ROOT.gStyle)
#ROOT.gStyle.SetOptTitle(1)
#ROOT.gStyle.SetPadLeftMargin(0.18)
#ROOT.gStyle.SetPadBottomMargin(0.15)

col_qcd = TColor.GetColor(250,202,255)
col_tt  = TColor.GetColor(155,152,204)
col_ttv  = TColor.GetColor(155,182,204)
col_ewk = TColor.GetColor(222,90,106)
col_zll = TColor.GetColor(100,182,232)
col_red = TColor.GetColor(248,206,104)

nbin=30

basic='l1_pt > 30 && met > 30'

variables = {
    'MR': {'var':'MR', 'nbin':nbin, 'xtitle':'M_{R} (GeV)', 'xmin':0, 'xmax':1000, 'sel':basic + ' && njets40!=0 && MR > 350'},
    'Rsq': {'var':'Rsq', 'nbin':nbin, 'xtitle':'Rsq', 'xmin':0, 'xmax':1, 'sel':basic + ' && njets40!=0 && MR > 350'},
    'l1_gen_pdgId': {'var':'abs(l1_gen_pdgId)', 'nbin':25, 'xtitle':'l1 gen pdgID', 'xmin':0, 'xmax':25, 'sel':basic + ' && njets40!=0 && MR > 350'},
    'l2_gen_pdgId': {'var':'abs(l2_gen_pdgId)', 'nbin':25, 'xtitle':'l2 gen pdgID', 'xmin':0, 'xmax':25, 'sel':basic + ' && njets40!=0 && MR > 350'},
    'HT_jet30': {'var':'HT_jet30', 'nbin':nbin, 'xtitle':'H_{T} (jet p_{T} > 30) (GeV)', 'xmin':0, 'xmax':1000, 'sel':basic},
#    'HT_jet20': {'nbin':nbin, 'xtitle':'H_{T} (jet p_{T} > 20) (GeV)', 'xmin':0, 'xmax':1000, 'sel':basic},
#    'njets40': {'nbin':10, 'xtitle':'Number of jets (p_{T} > 40) (GeV)', 'xmin':0, 'xmax':10, 'sel':basic},
#    'pfmet': {'nbin':nbin, 'xtitle':'missing E_{T} (GeV)', 'xmin':0, 'xmax':250, 'sel':basic},
#    'met': {'nbin':nbin, 'xtitle':'MVA missing E_{T} (GeV)', 'xmin':0, 'xmax':250, 'sel':basic},
#    'pthiggs': {'nbin':nbin, 'xtitle':'Higgs p_{T} (GeV)', 'xmin':0, 'xmax':250, 'sel':basic},
#    'diTau_pt': {'nbin':nbin, 'xtitle':'diTau p_{T} (GeV)', 'xmin':0, 'xmax':150, 'sel':basic},
#    'mt': {'nbin':nbin, 'xtitle':'M_{T} (GeV)', 'xmin':0, 'xmax':200, 'sel':basic},
#    'visMass': {'nbin':nbin, 'xtitle':'visible Mass (GeV)', 'xmin':0, 'xmax':400, 'sel':basic},
#    'svfitMass': {'nbin':nbin, 'xtitle':'SVfit Mass (GeV)', 'xmin':0, 'xmax':700, 'sel':basic},
#    'l1_pt': {'nbin':nbin, 'xtitle':'tau pT (GeV)', 'xmin':0, 'xmax':150, 'sel':basic},
#    'l1_decayMode': {'nbin':12, 'xtitle':'tau decaymode', 'xmin':0, 'xmax':12, 'sel':basic},
#    'l1_eta': {'nbin':nbin, 'xtitle':'tau #eta', 'xmin':-2.3, 'xmax':2.3, 'sel':basic},
#    'l1_phi': {'nbin':nbin, 'xtitle':'tau #phi', 'xmin':-math.pi, 'xmax':math.pi, 'sel':basic},
#    'l2_pt': {'nbin':nbin, 'xtitle':'muon pT (GeV)', 'xmin':0, 'xmax':150, 'sel':basic},
#    'l2_eta': {'nbin':nbin, 'xtitle':'muon #eta', 'xmin':-2.3, 'xmax':2.3, 'sel':basic},
#    'l2_phi': {'nbin':nbin, 'xtitle':'muon #phi', 'xmin':-math.pi, 'xmax':math.pi, 'sel':basic},
#    'jet1_pt': {'nbin':nbin, 'xtitle':'leading jet pT (GeV)', 'xmin':0, 'xmax':300, 'sel':basic + ' && nJets20!=0 '},
#    'jet1_eta': {'nbin':nbin, 'xtitle':'leading jet #eta', 'xmin':-2.3, 'xmax':2.3, 'sel':basic + ' && nJets20!=0 '},
#    'jet1_phi': {'nbin':nbin, 'xtitle':'leading jet #phi', 'xmin':-math.pi, 'xmax':math.pi, 'sel':basic + ' && nJets20!=0 '},
#    'nJets': {'nbin':10, 'xtitle':'Number of jets (pT > 30 GeV)', 'xmin':0, 'xmax':10, 'sel':basic},
#    'nJets20': {'nbin':10, 'xtitle':'Number of jets (pT > 20 GeV)', 'xmin':0, 'xmax':10, 'sel':basic},
}

prefix='sample_201507/'

selections = {
    'ttbar':{'sel':'pid==2', 'col':col_qcd, 'order':1, 'data':'TTJetsFullLept'},
    'Wjet':{'sel':'pid==3', 'col':col_zll, 'order':2, 'data':'WJets'},
    'DY':{'sel':'pid==1', 'col':col_red, 'order':3, 'data':'DYJets'},
    'Higgs':{'sel':'pid==6', 'col':col_ttv, 'order':4, 'data':'Higgs'},
    'SingleTop':{'sel':'pid==4', 'col':col_tt, 'order':5, 'data':'SingleTop'},
    'Diboson':{'sel':'pid==5', 'col':col_ewk, 'order':6, 'data':'VV'},
    'data':{'sel':'pid==0', 'col':1, 'order':2999, 'data':'data'}
    }

def ensureDir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def SavePlots(hh, name):

    c = TCanvas(name)

    print hh
    hh.DrawStack('HIST')
        
    ensureDir('plots')
    cname =  'plots/' + name + '.gif'

    c.Print(cname)



def makePlotsVars():
    print 'Make plotting variables'
    
    
    tfile = TFile(prefix + 'Myroot.root')
    tree = tfile.Get('H2TauTauTreeProducerTauMu')

    for ivar, var in variables.items():

        h_stack = DataMCPlot('hs_' + ivar)
        h_stack.legendBorders = 0.65, 0.6, 0.85, 0.85
        
        for iprocess, process in selections.items():

            hist = TH1F('h_'+ivar+'_'+iprocess, '', var['nbin'], var['xmin'], var['xmax'])
            hist.GetXaxis().SetTitle(var['xtitle'])
            hist.GetYaxis().SetNdivisions(507)
            hist.Sumw2()

            sel = '(' + var['sel']  + '&&' + process['sel'] + ')*weight2'

            print hist.GetName(), 'var = ', var['var'], ', condition = ', sel
            tree.Draw(var['var'] + ' >> ' + hist.GetName())
#            tree.Project(hist.GetName(), var['var'], sel)


            if iprocess=='data':
                hist.SetMarkerStyle(20)

            else:
                hist.SetFillStyle(1)
                hist.SetLineWidth(2)
                hist.SetFillColor(process['col'])
                hist.SetLineColor(process['col'])
                
           
            h_stack.AddHistogram(hist.GetName(), copy.deepcopy(hist), process['order'])
            h_stack.Hist(hist.GetName()).legendLine = iprocess

            if iprocess=='data':
                h_stack.Hist(hist.GetName()).stack = False

#        import pdb; pdb.set_trace()
        SavePlots(h_stack, ivar)

if __name__ == '__main__':

    makePlotsVars()
