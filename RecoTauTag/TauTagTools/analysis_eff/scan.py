import os, numpy, math, copy, math, sys
from array import array
from ROOT import TLegend, TCanvas, TColor, kMagenta, kOrange, kRed, kBlue, kGray, kYellow, kBlack, gROOT, gStyle, TFile, TH1F, TH2F, TLatex, TLine, TH1D, TGraph, Double
from officialStyle import officialStyle

gROOT.SetBatch(True)
officialStyle(gStyle)
gStyle.SetOptTitle(0)
gStyle.SetOptStat(111111111)
#gStyle.SetPadRightMargin (0.13)

#threshold = 0.85
threshold = 0.9

argvs = sys.argv
argc = len(argvs)

if argc != 2:
    print 'Please specify the runtype : python nIso.py <VBF, MSSM>'
    sys.exit(0)

runtype = argvs[1]

def ensureDir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def LegendSettings(leg, ncolumn):
    leg.SetNColumns(ncolumn)
    leg.SetBorderSize(0)
    leg.SetFillColor(10)
    leg.SetLineColor(0)
    leg.SetFillStyle(0)
    leg.SetTextSize(0.03)
    leg.SetTextFont(42)

def save(canvas, name):
    ensureDir('plots_scan')
    canvas.SaveAs(name.replace(' ','').replace('&&','').replace(',Dynamic','')+'.pdf')
    canvas.SaveAs(name.replace(' ','').replace('&&','').replace(',Dynamic','')+'.gif')


def Scan(tree, varx, vary, sel, nbinx, xmin, xmax, xtitle, leglabel = None, header='', addon='', xx='pt'):
   
    c = TCanvas()
    hist = TH1F('h_effp_' + addon, 'h_effp' + addon, nbinx, xmin, xmax)

    dname = varx + ' >> ' + hist.GetName()
    tree.Draw(dname, sel)

    leg = TLegend(0.08,0.93,0.5,0.99)
    LegendSettings(leg, 1)

    value = []
    
    flag = False
    eff90 = -1.
    eff_x = -1.

    for k in range(0, 1000):
        cutoff = 2. + k*0.1
        bin_high = hist.FindBin(cutoff)
#        print 'check:', k, bin_high
        eff = hist.Integral(0, bin_high-1)/hist.Integral(0, hist.GetNbinsX()+1)
#        value.append([Double(cutoff), eff])
        value.append([Double(k*0.1), eff])

        if eff > threshold and flag==False:
            eff90 = eff
#            eff_x = cutoff
            eff_x = k*0.1
            flag = True

    gr = TGraph()

    for ii, ivalue in enumerate(value):

        x,y = ivalue
        gr.SetPoint(ii, x, y)

        if x==2:
            print '-'*80
            print '2GeV point =', header, y
        
    gr_eff = TGraph()
    gr_eff.SetPoint(0, eff_x, eff90)

    print header, addon, eff_x, eff90

    gr.SetMarkerSize(0.5)
#    gr.GetXaxis().SetRangeUser(-2,20)
    gr.GetXaxis().SetRangeUser(-2,100)
    gr.GetYaxis().SetRangeUser(0,1)
    gr.GetXaxis().SetTitle('parameter : k')
    gr.GetYaxis().SetTitle('efficiency')
    gr.Draw("apl")

    gr_eff.SetMarkerStyle(28)
    gr_eff.SetMarkerColor(kRed)
    gr_eff.Draw("psame")

    leg2 = TLegend(0.8,0.93,0.9,0.99)
    LegendSettings(leg2, 1)
    leg2.AddEntry(gr, runtype, "")
    leg2.Draw()

    leg = TLegend(0.08,0.93,0.5,0.99)
    LegendSettings(leg, 1)
    leg.AddEntry(gr, addon.replace('pi0','#pi^{0}'), "")
    leg.Draw()

    leg3 = TLegend(0.5,0.2,0.9,0.3)
    LegendSettings(leg3, 1)
    leg3.AddEntry(gr_eff, 'threshold = ' + '{0:.2f}'.format(eff_x) + '@90%'  , "")
    leg3.Draw()

    save(c, 'plots_scan/' + header)


    
    

if __name__ == '__main__':

    filename = 'Myroot_dynamic95.root'
    
    if runtype == 'MSSM':
        filename = 'Myroot_mssm.root'
#        filename = '/afs/cern.ch/user/y/ytakahas/work/TauIsolation_dynamic_ranking_bugfixed_v2/CMSSW_7_2_3/src/RecoTauTag/TauTagTools/analysis_fake/Myroot_dynamic95.root'


    hdict = {
        'dynamic':{'file':filename,'label':'Dynamic'},
        }


#    ddict = {'1p0pi0':'tau_dm_rough==0', '1p1pi0':'tau_dm_rough==1', '2p':'(tau_dm==5 || tau_dm==6)', '3p':'tau_dm_rough==2'}
    ddict = {'1p0pi0':'tau_dm_rough==0', 
             '1p1pi0':'tau_dm_rough==1', 
             '2p0pi0':'tau_dm==5',
             '2p1pi0':'tau_dm==6', 
             '3p':'tau_dm_rough==2'}
#             'Inclusive':'tau_dm_rough!=0'}
#    ddict = {'2p':'(tau_dm==5 || tau_dm==6)'}
#    ddict = {'1p0pi0':'tau_dm_rough==0'}
    
#    region = {'barrel':'abs(tau_eta) < 1.479', 'endcap':'abs(tau_eta) > 1.479', 'All eta':'1'}
#    region = {'barrel':'abs(tau_eta) < 1.479', 'endcap':'abs(tau_eta) > 1.479'}
#    region = {'endcap':'abs(tau_eta) > 1.479'}
    region = {'All eta':'1'}

    valdict = {
        'nIso_weight_ciso_outer':{'tree':'per_tau',
                                  'var':'tau_niso_weighted', 
                                  'nbin':1000, 'xmin':0., 'xmax':100, 
                                  'title':'nIso weighted', 
                                  'sel':'tau_dm!=-1 && tau_pt > 20 && abs(tau_eta) < 2.3 && tau_ciso < 2 && (tau_photonsumpt_outside/tau_pt) < 0.2*tau_pt',
#                                  'sel':'tau_dm!=-1 && (tau_photonsumpt_outside/tau_pt) < 0.2*tau_pt ',
                                  'name':'nIso_weight_ciso_outer'},
        }

    

    for vkey, ivar in valdict.iteritems():
        for rkey, rval in region.iteritems():
            for dkey, dm in ddict.iteritems():

                hists = []

                for key, val in sorted(hdict.iteritems()):
                
                    tfile = TFile(val['file'])
                    tree = tfile.Get(ivar['tree'])
                    
                    Scan(tree, 'tau_niso_weighted', ivar['var'], ivar['sel'] + ' && ' + dm + '&&' + rval, ivar['nbin'], ivar['xmin'], ivar['xmax'], 'Tau pT (GeV)', ivar['title'], rkey + '_' + dkey + ', ' + val['label'], dkey + ', ' +rkey, 'pt')




