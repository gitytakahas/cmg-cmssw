import os, numpy, math, copy, math
from array import array
from ROOT import TLegend, TCanvas, TColor, kMagenta, kOrange, kRed, kBlue, kGray, kBlack, gROOT, gStyle, TFile, TH1F, TH2F, TLatex, TLine
from officialStyle import officialStyle
from collections import OrderedDict

gROOT.SetBatch(True)
officialStyle(gStyle)
gStyle.SetOptTitle(0)
gStyle.SetOptStat(0)

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
    ensureDir('plots_isolation_vbf')
    canvas.SaveAs(name.replace(' ','').replace('&&','')+'.pdf')
    canvas.SaveAs(name.replace(' ','').replace('&&','')+'.gif')

def createProfile(hist):

    _hist1d_ = TH1D(hist.GetName()+'_px', hist.GetName()+'_px', hist.GetXaxis().GetNbins(), hist.GetXaxis().GetXmin(), hist.GetXaxis().GetXmax())


    for xbin in range(1, hist.GetXaxis().GetNbins()+1):
        hh = hist.ProjectionY("proj" + str(xbin), xbin, xbin)

        if hh.GetEntries() < 10: continue

        _hist1d_.SetBinContent(xbin, hh.GetMean())
        _hist1d_.SetBinError(xbin, hh.GetMeanError())

    return _hist1d_

def overlay(hists, header):

#    print 'enters overlay function --------------------'

    canvas = TCanvas()
    leg = TLegend(0.2,0.93,0.8,0.99)
    LegendSettings(leg,len(hists))

    col = [1,2,4,6,8]

    ymax = -1
    for ii, hist in enumerate(hists):
        hist.SetLineColor(col[ii])
        hist.SetMarkerColor(col[ii])
        hist.SetLineWidth(3-ii)

        if ymax < hist.GetMaximum():
            ymax = hist.GetMaximum()

        if ii==0:
            hist.Draw("ep")
        else:
            hist.Draw("epsame")
 
        leg.AddEntry(hist, hist.GetName(), 'lep')

    for hist in hists:
        hist.SetMaximum(ymax*1.4)

    leg.Draw()

    leg2 = TLegend(0.8,0.93,0.9,0.99)
    LegendSettings(leg2, 1)
    leg2.AddEntry(hists[-1], 'VBF', "")
    leg2.Draw()

    save(canvas, 'plots_isolation_vbf/' + header)

#    print 'end overlay function --------------------'

    

if __name__ == '__main__':

    rfile = '../analysis_eff/Myroot_dynamic95.root'

    ddict = {
        'a':{'cut':'tau_dm_rough==0', 'label':'1prong'},
        'b':{'cut':'tau_dm_rough==1', 'label':'1prong+#pi^{0}'}
        }

    ddict_2p = {
        'c':{'cut':'tau_dm==5', 'label':'2prong'},
        'd':{'cut':'tau_dm==6', 'label':'2prong+#pi^{0}'},
        }

    ddict_3p = {
        'e':{'cut':'tau_dm_rough==2', 'label':'3prong'},
        }


    yvardict = {
        'nIso_raw':{'tree':'per_tau','var':'tau_niso_weighted', 'nbin':2000, 'xmin':0., 'xmax':100, 'title':'Neutral weighted Iso. (GeV)', 'sel':'tau_dm!=-1 && tau_pt > 20 && abs(tau_eta) < 2.3', 'name':'VBF_weighted_niso_overlay_eta'},
        }


    tfile = TFile(rfile)
    tree = tfile.Get('per_tau')

    for vkey, ivar in yvardict.iteritems():

        hists = []
        for dkey, dm in ddict.iteritems():


            _hist_ = TH2F('h_effp_' + dkey, 'h_effp_' + dkey, 15,-2.3,2.3, ivar['nbin'], ivar['xmin'], ivar['xmax'])


            dname = ivar['var'] + ':tau_geneta >> ' + _hist_.GetName()
            tree.Draw(dname, ivar['sel'] + '&&' + dm['cut'])

            hist = _hist_.ProfileX()

            hist.GetXaxis().SetTitle('gen tau #eta^{vis} (GeV)')
            hist.GetYaxis().SetTitle(ivar['title'])
            hist.GetYaxis().SetNdivisions(507)
            hist.SetMinimum(0.)
            hist.SetLineWidth(3)
            hist.SetName(dm['label'])
            hists.append(hist)

        overlay(hists, ivar['name'] + '_1prong')


        hists = []
        for dkey, dm in ddict_2p.iteritems():

            _hist_ = TH2F('h_effp_' + dkey, 'h_effp_' + dkey, 15,-2.3,2.3, ivar['nbin'], ivar['xmin'], ivar['xmax'])


            dname = ivar['var'] + ':tau_geneta >> ' + _hist_.GetName()
            tree.Draw(dname, ivar['sel'] + '&&' + dm['cut'])

            hist = _hist_.ProfileX()

            hist.GetXaxis().SetTitle('gen tau #eta^{vis} (GeV)')
            hist.GetYaxis().SetTitle(ivar['title'])
            hist.GetYaxis().SetNdivisions(507)
            hist.SetMinimum(0.)
            hist.SetLineWidth(3)
            hist.SetName(dm['label'])
            hists.append(hist)

        overlay(hists, ivar['name'] + '_2prong')

        hists = []
        for dkey, dm in ddict_3p.iteritems():

            _hist_ = TH2F('h_effp_' + dkey, 'h_effp_' + dkey, 15,-2.3,2.3, ivar['nbin'], ivar['xmin'], ivar['xmax'])


            dname = ivar['var'] + ':tau_geneta >> ' + _hist_.GetName()
            tree.Draw(dname, ivar['sel'] + '&&' + dm['cut'])

            hist = _hist_.ProfileX()

            hist.GetXaxis().SetTitle('gen tau #eta^{vis} (GeV)')
            hist.GetYaxis().SetTitle(ivar['title'])
            hist.GetYaxis().SetNdivisions(507)
            hist.SetMinimum(0.)
            hist.SetLineWidth(3)
            hist.SetName(dm['label'])
            hists.append(hist)

        overlay(hists, ivar['name'] + '_3prong')

