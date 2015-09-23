import os, numpy, math, copy
from ROOT import TLegend, TCanvas, TColor, kMagenta, kOrange, kRed, kBlue, kGray, kBlack, gROOT, gStyle, TFile, TH1F, TH2F
from officialStyle import officialStyle
from CMGTools.H2TauTau.proto.plotter.categories_TauMu import *
from CMGTools.H2TauTau.proto.plotter.categories_common import *

gROOT.SetBatch(True)
officialStyle(gStyle)
gStyle.SetOptTitle(0)

def overflow(h):
    uflow = h.GetBinContent(0)
    oflow = h.GetBinContent(h.GetXaxis().GetNbins()+1)

    h.SetBinContent(1, uflow + h.GetBinContent(1))
    h.SetBinContent(h.GetXaxis().GetNbins(), oflow + h.GetBinContent(h.GetXaxis().GetNbins()))

    h.SetBinContent(0, 0.)
    h.SetBinContent(h.GetXaxis().GetNbins()+1, 0.)
    

def ensureDir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def LegendSettings(leg, ncolumn):
    leg.SetNColumns(ncolumn)
    leg.SetBorderSize(0)
    leg.SetFillColor(10)
    leg.SetLineColor(0)
    leg.SetFillStyle(0)
    leg.SetTextSize(0.04)
    leg.SetTextFont(42)

def save(canvas, name):
    ensureDir('plots')
    canvas.SaveAs(name.replace(' ','').replace('&&','')+'.pdf')
    canvas.SaveAs(name.replace(' ','').replace('&&','')+'.gif')



def makeCompareVars(hists, xtitle, ytitle, scale ,savestr, ncolumn):
   
    c = TCanvas()

    col = [1, 2, 4, 6, 8, 30, 40, 50]

    for ii, hist in enumerate(hists):
        hist.GetXaxis().SetTitle(xtitle)
        hist.GetYaxis().SetTitle(ytitle)
        hist.GetYaxis().SetNdivisions(505)
        hist.GetXaxis().SetNdivisions(505)
#        hist.GetXaxis().SetLabelSize(0.14)
        hist.SetLineWidth(2)
        hist.SetLineColor(col[ii])
        hist.SetMarkerSize(0)
        hist.SetMinimum(0.)

        if scale and hist.GetSumOfWeights()!=0:
            hist.Scale(1./hist.GetEntries())
            hist.SetMaximum(hist.GetMaximum()*1.2)

    ymax = max([ihist.GetMaximum() for ihist in hists])
#    leg = TLegend(0.6,0.7,0.9,0.9)
    leg = TLegend(0.16,0.93,0.91,0.99)
    LegendSettings(leg, ncolumn)

    for ii, hist in enumerate(hists):
        hist.SetMaximum(ymax*1.2)
        hist.SetMinimum(0.)
        hist.SetLineWidth(3-ii)

        if ii==0:
            hist.Draw('ep')
        else:
            hist.Draw('epsame')
        
        leg.AddEntry(hist, hist.GetTitle(), "l")


    leg.Draw()
    save(c, 'plots/compare' + savestr)


    

if __name__ == '__main__':

    rfile = {
        'CP_even':{'sample':'20150119_nom/Higgs0PGGH125/H2TauTauTreeProducerTauMu/H2TauTauTreeProducerTauMu_tree.root', 'leg':'CP even (JHU)', 'col':kBlue},
        'CP_odd':{'sample':'20150119_nom/Higgs0MGGH125/H2TauTauTreeProducerTauMu/H2TauTauTreeProducerTauMu_tree.root', 'leg':'CP odd (JHU)', 'col':kRed},
        'SM':{'sample':'../20140329_nominal/HiggsGGH125/H2TauTauTreeProducerTauMu/H2TauTauTreeProducerTauMu_tree.root', 'leg':'SM (PY6)', 'col':kBlack},
        }


    seldict = {
        'inc': cat_Inc,
        'njets': cat_Inc + ' && nJets>=2',
        'njets_nbjets': cat_Inc + ' && nJets>=2 && nBJets == 0',
        'njets_nbjets_ncentral': cat_Inc + ' && nJets>=2 && nBJets == 0 && VBF_nCentral==0',
        'njets_nbjets_ncentral_mjj': cat_Inc + ' && nJets>=2 && nBJets == 0 && VBF_nCentral==0 && VBF_mjj > 500',
        'njets_nbjets_ncentral_mjj_deta': cat_Inc + ' && nJets>=2 && nBJets == 0 && VBF_nCentral==0 && VBF_mjj > 500 && abs(VBF_deta) > 3.5',
        }


    vardict = {
        'njets':{'var':'nJets', 'nbin':10, 'xmin':0, 'xmax':10, 'title':"# of jets"},
        'nbjets':{'var':'nBJets', 'nbin':5, 'xmin':0, 'xmax':5, 'title':"# of bjets"},
        'nCentral':{'var':'VBF_nCentral', 'nbin':5, 'xmin':0, 'xmax':5, 'title':"# of central jets"},
        'mjj':{'var':'VBF_mjj', 'nbin':30, 'xmin':0, 'xmax':2000, 'title':"mjj"},
        'deta':{'var':'VBF_deta', 'nbin':30, 'xmin':-7.5, 'xmax':7.5, 'title':"#Delta#eta (jj)"},
        'dphi':{'var':'jet1_phi-jet2_phi', 'nbin':10, 'xmin':-2*math.pi, 'xmax':2*math.pi, 'title':"#Delta#phi (jj)"},
        'pthiggs':{'var':'pthiggs', 'nbin':30, 'xmin':0, 'xmax':200, 'title':"p_{T}^{Higgs}"},
        }


    for vkey, ivar in vardict.iteritems():
        for inum, isel in seldict.iteritems():
            
            hists = []
            
            for key, value in rfile.iteritems():
                tfile = TFile(value['sample'])
                tree = tfile.Get('H2TauTauTreeProducerTauMu')
                
                hist = TH1F('h_'+key, 'h_'+key, ivar['nbin'], ivar['xmin'], ivar['xmax'])
                hist.SetLineColor(value['col'])
                hist.Sumw2()
                hist.SetTitle(value['leg'])
                
                tree.Project(hist.GetName(), ivar['var'], isel)
                hists.append(copy.deepcopy(hist))
            
            makeCompareVars(hists, ivar['title'], 'a.u.', True , 'GGH_dphi_' + inum + '_VAR_' + vkey , len(hists))
    
