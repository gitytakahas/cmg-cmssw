import os, numpy, math, copy, math
from ROOT import TLegend, TCanvas, TColor, kMagenta, kOrange, kRed, kBlue, kGray, kBlack, gROOT, gStyle, TFile, TH1F, TH2F, Double
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
#    canvas.SaveAs(name.replace(' ','').replace('&&','')+'.pdf')
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
            hist.Draw('hep')
        else:
            hist.Draw('hepsame')
        
        leg.AddEntry(hist, hist.GetTitle(), "l")


    leg.Draw()
    save(c, 'plots/ME_' + savestr)


def makeCorrelationVars( xtitle, ytitle, scale ,savestr, ncolumn):
   
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
            hist.Draw('hep')
        else:
            hist.Draw('hepsame')
        
        leg.AddEntry(hist, hist.GetTitle(), "l")


    leg.Draw()
    save(c, 'plots/ME_' + savestr)

    

if __name__ == '__main__':

    rfile = {
        'CP_even':{'sample':'sample_20150205/Higgs0PGGH125/H2TauTauTreeProducerTauMu/H2TauTauTreeProducerTauMu_tree.root', 'leg':'CP even (JHU)', 'col':kBlue},
#        'CP_odd':{'sample':'sample_20150205/Higgs0MGGH125/H2TauTauTreeProducerTauMu/H2TauTauTreeProducerTauMu_tree.root', 'leg':'CP odd (JHU)', 'col':kRed},
#        'VBF':{'sample':'/data1/ytakahas/H2tautau_data/sample_20140329/20140329_nominal/HiggsVBF125/H2TauTauTreeProducerTauMu/H2TauTauTreeProducerTauMu_tree.root', 'leg':'VBF', 'col':kRed},
        }


#    seldict = {
#        'inclusive': '',
#        'inclusive_jetpt': 'outgoing1_pt > 20 && outgoing2_pt > 20',
#        'inclusive_jetpt_eta': 'abs(outgoing1_eta) < 5. && abs(outgoing2_eta) < 5. && outgoing1_pt > 20 && outgoing2_pt > 20',
#        'inclusive_jetpt_eta_dR':'abs(outgoing1_eta) < 5. && abs(outgoing2_eta) < 5. && outgoing1_pt > 20 && outgoing2_pt > 20 && outgoing_dR > 0.6',
#        'inclusive_jetpt_eta_dR_mjj':'abs(outgoing1_eta) < 5. && abs(outgoing2_eta) < 5. && outgoing1_pt > 20 && outgoing2_pt > 20 && outgoing_dR > 0.6 && outgoing_mjj > 200',
#        'inclusive_jetpt_eta_dR_mjj_vpt':'abs(outgoing1_eta) < 5. && abs(outgoing2_eta) < 5. && outgoing1_pt > 20 && outgoing2_pt > 20 && outgoing_dR > 0.6 && outgoing_mjj > 200 && genhiggspt > 70',
#        }


    cat_Inc = cat_Inc + ' && jet1_pt > 50 && jet2_pt > 50'

    print 'common selection = ', cat_Inc

    seldict = {
#        'njets': '',
        'inc': cat_Inc + ' && nJets >= 2',
#        'njets': cat_Inc + ' && nJets>=2',
        'njets_nbjets': cat_Inc + ' && nJets>=2 && nBJets == 0',
        'njets_nbjets_dr': cat_Inc + ' && nJets>=2 && nBJets == 0 && sqrt(VBF_deta**2 + VBF_jdphi**2) > 0.6',
#        'njets_nbjets_ncentral': cat_Inc + ' && nJets>=2 && nBJets == 0 && VBF_nCentral==0',
        'njets_nbjets_dr_mjj': cat_Inc + ' && nJets>=2 && nBJets == 0 && sqrt(VBF_deta**2 + VBF_jdphi**2) > 0.6 && VBF_mjj > 200',
        'njets_nbjets_dr_mjj_pthiggs': cat_Inc + ' && nJets>=2 && nBJets == 0 && sqrt(VBF_deta**2 + VBF_jdphi**2) > 0.6 && VBF_mjj > 200 && pthiggs > 70',
        }

#        'dphi':{'nbin':nbin, 'xtitle':'#Delta#phi(jj)', 'xmin':-math.pi, 'xmax':math.pi},
#        'mjj':{'nbin':nbin, 'xtitle':'mjj', 'xmin':0, 'xmax':1000},
#        'deta':{'nbin':nbin, 'xtitle':'#Delta#eta', 'xmin':0, 'xmax':10},
#        'id_1':{'nbin':30, 'xtitle':'jet1 pdgId', 'xmin':-5, 'xmax':25},
#        'id_2':{'nbin':30, 'xtitle':'jet2 pdgId', 'xmin':-5, 'xmax':25},
#        'jetpt_1':{'nbin':30, 'xtitle':'jet1 pT', 'xmin':0, 'xmax':200},
#        'jetpt_2':{'nbin':30, 'xtitle':'jet2 pT', 'xmin':0, 'xmax':200},
#        'jeteta_1':{'nbin':30, 'xtitle':'jet1 #eta', 'xmin':-10, 'xmax':10},
#        'jeteta_2':{'nbin':30, 'xtitle':'jet2 #eta', 'xmin':-10, 'xmax':10},
#        'jetphi_1':{'nbin':30, 'xtitle':'jet1 #phi', 'xmin':-3.14, 'xmax':3.14},
#        'jetphi_2':{'nbin':30, 'xtitle':'jet2 #phi', 'xmin':-3.14, 'xmax':3.14},


    vardict = {
#        'njets':{'var':'nJets', 'nbin':10, 'xmin':0, 'xmax':10, 'title':"# of jets"},
#        'nbjets':{'var':'nBJets', 'nbin':5, 'xmin':0, 'xmax':5, 'title':"# of bjets"},
#        'nCentral':{'var':'VBF_nCentral', 'nbin':5, 'xmin':0, 'xmax':5, 'title':"# of central jets"},
#        'mjj':{'var':'VBF_mjj', 'nbin':30, 'xmin':0, 'xmax':2000, 'title':"mjj"},
#        'deta':{'var':'VBF_deta', 'nbin':30, 'xmin':-7.5, 'xmax':7.5, 'title':"#Delta#eta (jj)"},
        'dphi':{'var':'VBF_jdphi', 'nbin':25, 'xmin':-math.pi, 'xmax':math.pi, 'title':"#Delta#phi(jj)"},
#        'isME':{'var':'jet1_isME && jet2_isME', 'nbin':25, 'xmin':-math.pi, 'xmax':math.pi, 'title':"#Delta#phi(jj)"},
#        'deta':{'var':'outgoing_deta', 'nbin':50, 'xmin':0, 'xmax':10, 'title':"#Delta#eta"},
#        'mjj':{'var':'outgoing_mjj', 'nbin':50, 'xmin':0, 'xmax':1000, 'title':"mjj"},
#        'dR':{'var':'outgoing_dR', 'nbin':50, 'xmin':0, 'xmax':9, 'title':"dR"},
#        'genhiggspt':{'var':'genhiggspt', 'nbin':30, 'xmin':0, 'xmax':200, 'title':"gen p_{T}^{Higgs}"},
#        'id_1':{'var':'outgoing1_pdgId', 'nbin':30, 'xmin':-5, 'xmax':25, 'title':"jet1 pdgId"},
#        'id_2':{'var':'outgoing2_pdgId', 'nbin':30, 'xmin':-5, 'xmax':25, 'title':"jet2 pdgId"},
#        'm_1':{'var':'outgoing1_m', 'nbin':50, 'xmin':-0.5, 'xmax':0.5, 'title':"parton1 mass"},
#        'm_2':{'var':'outgoing2_m', 'nbin':50, 'xmin':-0.5, 'xmax':0.5, 'title':"parton2 mass"},
#        'jetpt_1':{'var':'outgoing1_pt', 'nbin':30, 'xmin':0, 'xmax':200, 'title':"jet1 pT"},
#        'jetpt_2':{'var':'outgoing2_pt', 'nbin':30, 'xmin':0, 'xmax':200, 'title':"jet2 pT"},
#        'jeteta_1':{'var':'outgoing1_eta', 'nbin':30, 'xmin':-10, 'xmax':10, 'title':"jet1 #eta"},
#        'jeteta_2':{'var':'outgoing2_eta', 'nbin':30, 'xmin':-10, 'xmax':10, 'title':"jet2 #eta"},
#        'jetphi_1':{'var':'outgoing1_phi', 'nbin':30, 'xmin':-math.pi, 'xmax':math.pi, 'title':"jet1 #phi"},
#        'jetphi_2':{'var':'outgoing2_phi', 'nbin':30, 'xmin':-math.pi, 'xmax':math.pi, 'title':"jet2 #phi"},
#        'pthiggs':{'var':'pthiggs', 'nbin':30, 'xmin':0, 'xmax':200, 'title':"p_{T}^{Higgs}"},
        }




    for vkey, ivar in vardict.iteritems():
        for inum, isel in seldict.iteritems():
            
            hists = []
            
            for key, value in rfile.iteritems():

                print 'filename = ', value['sample']

                tfile = TFile(value['sample'])
                tree = tfile.Get('H2TauTauTreeProducerTauMu')
                
                hist = TH1F('h_'+key, 'h_'+key, ivar['nbin'], ivar['xmin'], ivar['xmax'])
                hist.SetLineColor(value['col'])
                hist.Sumw2()
                hist.SetTitle(value['leg'])
                
                tree.Project(hist.GetName(), ivar['var'], isel)
                hists.append(copy.deepcopy(hist))

                print '****', isel
                e1 = Double(tree.GetEntries(isel + '&& jet1_isME==1 && jet2_isME==1'))
                e2 = Double(tree.GetEntries(isel + '&& jet1_isME==1 && jet2_isME!=1'))
                e3 = Double(tree.GetEntries(isel + '&& jet1_isME!=1 && jet2_isME==1'))
                e4 = Double(tree.GetEntries(isel + '&& jet1_isME!=1 && jet2_isME!=1'))
                all = e1+e2+e3+e4
#
#                print e1, e2, e3, e4
#
                print inum, 'both = ', Double(e1/all)
                print inum, 'first one match = ', Double(e2/all)
                print inum, 'second one match = ', Double(e3/all)
                print inum, 'one of them = ', Double((e2+e3)/all)
                print inum, 'none = ', Double(e4/all)
            
            makeCompareVars(hists, ivar['title'], 'a.u.', True , 'GGH_' + vkey + '_' + inum + '_' + vkey , len(hists))
    





    for inum, isel in seldict.iteritems():
        for vkey1, ivar1 in vardict.iteritems():
            for vkey2, ivar2 in vardict.iteritems():
                if vkey1==vkey2: continue

                hists = []
                
                for key, value in rfile.iteritems():
                    tfile = TFile(value['sample'])
                    tree = tfile.Get('H2TauTauTreeProducerTauMu')


                    print 'making correlation plots', vkey1, vkey2
                    hist = TH2F('h_'+key + '_' + vkey1 + '_' + vkey2, 'h_'+key + '_' + vkey1 + '_' + vkey2, ivar1['nbin'], ivar1['xmin'], ivar1['xmax'], ivar2['nbin'], ivar2['xmin'], ivar2['xmax'])
                    
#                    hist.SetLineColor(value['col'])
#                    hist.Sumw2()
#                    hist.SetTitle(value['leg'])
            
                    tree.Draw(ivar1['var'] +':'+ ivar2['var'] + ' >> ' + hist.GetName(), isel)
                    hists.append(copy.deepcopy(hist))
            
#            makeCompareVars(hists, ivar['title'], 'a.u.', True , 'GGH_' + vkey + '_' + inum + '_' + vkey , len(hists))
    
