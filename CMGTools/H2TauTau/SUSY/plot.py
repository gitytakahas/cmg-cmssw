import ROOT, os, numpy, copy
#from officialStyle import officialStyle
from ROOT import TLegend, TCanvas, TFile, TTree, TH1F, TColor, kMagenta, kOrange, kRed, kBlue, kGray, kBlack
from CMGTools.RootTools.DataMC.DataMCPlot import DataMCPlot
from CMGTools.H2TauTau.proto.plotter.officialStyle import officialStyle

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

variables = {
    'HT_jet30': {'nbin':nbin, 'xtitle':'H_{T} (GeV)', 'xmin':0, 'xmax':400, 'sel':'1'},
    'pfmet': {'nbin':nbin, 'xtitle':'missing E_{T} (GeV)', 'xmin':0, 'xmax':150, 'sel':'1'},
    'diTau_pt': {'nbin':nbin, 'xtitle':'Higgs p_{T} (GeV)', 'xmin':0, 'xmax':150, 'sel':'1'},
    'MR': {'nbin':nbin, 'xtitle':'M_{R} (GeV)', 'xmin':0, 'xmax':1000, 'sel':'MR!=-1'},
    'Rsq': {'nbin':nbin, 'xtitle':'Rsq', 'xmin':0, 'xmax':1, 'sel':'MR!=-1'},
    'mt': {'nbin':nbin, 'xtitle':'M_{T} (GeV)', 'xmin':0, 'xmax':200, 'sel':'1'},
}

prefix='sample_201507/'

selections = {
    'ttbar':{'sel':'pid==2', 'col':col_qcd, 'order':1, 'data':'TTJetsFullLept'},
    'Wjet':{'sel':'pid==3', 'col':col_zll, 'order':2, 'data':'WJets'},
    'DY':{'sel':'pid==1', 'col':col_ewk, 'order':3, 'data':'DYJets'},
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

            tree.Project(hist.GetName(), ivar, sel)


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
