from officialStyle import officialStyle
from basic import *
from array import array
from ROOT import TLine, TH1F, TH1D, TF1
import math

gROOT.SetBatch(True)
officialStyle(gStyle)
gStyle.SetOptTitle(0)
set_palette("color")

gStyle.SetPadLeftMargin(0.17)
gStyle.SetPadRightMargin(0.12)


def FindEdge(hS, threshold):

    maxBin = hS.GetNbinsX()

    if hS.Integral() == 0.:
        print 'ROC curve creator, hist', hS.GetName(), 'has zero entries'
        return

    effsS = [hS.Integral(0, nBin)/hS.Integral(0, maxBin+1) for nBin in range(0, maxBin + 1) ]

    FindBin = -1

    for ii, ieff in enumerate(effsS):
        if ieff > threshold and FindBin==-1:
            FindBin = hS.GetBinCenter(ii+1)


#  rocCurve = TGraph(maxBin, numpy.asarray(effsS), numpy.asarray(rejB))

    if FindBin == -1: print '!!! Find bin failed !!!'
    return FindBin
  



def createProfile(hist, threshold):

    _hist1d_ = TH1D(hist.GetName()+'_px', hist.GetName()+'_px', hist.GetXaxis().GetNbins(), hist.GetXaxis().GetXmin(), hist.GetXaxis().GetXmax())


    for xbin in range(1, hist.GetXaxis().GetNbins()+1):
        hh = hist.ProjectionY("proj" + str(xbin), xbin, xbin)

        if hh.GetEntries() == 0: continue

        val = FindEdge(hh, threshold)
        err = math.sqrt(threshold*(1-threshold)/hh.GetEntries())

        _hist1d_.SetBinContent(xbin, val)

        upper_edge = FindEdge(hh, threshold+err)
        lower_edge = FindEdge(hh, threshold-err)
        print hh.GetEntries(), 'val = ', val, 'err = ', err, 'upper / lower = ', upper_edge, lower_edge
        errbar = (upper_edge + lower_edge)/2. - val
        _hist1d_.SetBinError(xbin, errbar)

    return _hist1d_


def makeEffPlotsVars(tree, varx, vary, sel, nbiny, ymin, ymax, xtitle, ytitle, leglabel = None, header='', ispt = 'pt', threshold = 1):
   
    c = TCanvas()
    hname = 'h_effp_' + header

    if ispt == 'pt':
        # this is for 95% envelope
#        _hist_ = TH2F(hname, hname, 41,0.5,20, nbiny, ymin, ymax)

        # this is for 90% envelope
        _hist_ = TH2F(hname, hname, 31,0.5,20, nbiny, ymin, ymax)
    elif ispt == 'ptsp':
        _hist_ = TH2F(hname, hname, 50,0,2, nbiny, ymin, ymax)
    elif ispt == 'eta':
        _hist_ = TH2F(hname, hname, 20,-2.5,2.5, nbiny, ymin, ymax)

    dname = vary + ':' + varx + ' >> ' + _hist_.GetName()
    tree.Draw(dname, sel)

    hist = _hist_.ProfileX()

    print '='*60
    print header, '# of entries = ', hist.GetEntries()
    print '='*60

    hist_edge = createProfile(_hist_, threshold)
    hist_edge.GetXaxis().SetTitle(xtitle)
    hist_edge.GetYaxis().SetTitle(ytitle)
    hist_edge.GetYaxis().SetNdivisions(507)
    hist_edge.SetLineWidth(3)
    hist_edge.GetYaxis().SetTitleOffset(1.5)


    func = TF1("func", "[0]/x^[1]",hist.GetXaxis().GetXmin(), hist.GetXaxis().GetXmax())
    func_low = TF1("func_low", "[0]/x^[1]")

    if ispt != 'eta':
        func.SetParameter(0, 0.03)
        func.SetParameter(0, 0.2)

        hist_edge.Fit("func","", "",0.5, hist.GetXaxis().GetXmax())
        _f_ = hist_edge.GetFunction("func")
        _f_.SetLineColor(1)
        _f_.SetLineStyle(2)

    hist_edge.Draw("pl")
    hist_edge.SetLineColor(kRed)
    hist_edge.SetMarkerColor(kRed)
    hist_edge.SetMinimum(0.)
#    hist_edge.SetMaximum(hist_edge.GetMaximum()*1.5)
    hist_edge.SetMaximum(min(0.5,hist_edge.GetMaximum()*1.5))
    hist.Draw("same")

    if ispt != 'eta':
        _f_.Draw('same')
    
        func_low.SetParameter(0, func.GetParameter(0))
        func_low.SetParameter(1, func.GetParameter(1))
        func_low.SetParameter(2, func.GetParameter(2))
        func_low.SetLineColor(1)
        func_low.SetLineStyle(2)    
        func_low.Draw('same')
    
    
    if header.find('eff')==-1:
        _hist_.SetMarkerColor(38)
        _hist_.SetMarkerSize(0.3)
        _hist_.Draw("colzsame")
        hist.Draw('lepsame')
        hist_edge.Draw("plsame")

    hist_edge.Draw("axissame")




    line = TLine(hist.GetXaxis().GetXmin(), 0.2, hist.GetXaxis().GetXmax(), 0.2)
    line.SetLineStyle(2)
    line.SetLineColor(kMagenta)
#    line.Draw()

    leg = TLegend(0.1,0.93,0.5,0.99)
    LegendSettings(leg,1)

    if leglabel != None:
        if leglabel=='1p0pi0': leglabel = '#pi'
        elif leglabel == '1p1pi0': leglabel = '#pi#pi^{0}s'
        elif leglabel == '3p0pi0': leglabel = '#pi#pi#pi'

        leg.AddEntry(hist, leglabel, "")
        leg.Draw()

#    if ispt != 'eta':
#        leg2 = TLegend(0.3,0.2,0.9,0.3)
#        LegendSettings(leg2,1)
#        lstr = 'slope : ' + '{0:.5f}'.format(func.GetParameter(0)) + ' #pm ' + '{0:.5f}'.format(func.GetParError(0))
#        lstr2 = 'intercept : ' + '{0:.5f}'.format(func.GetParameter(1)) + ' #pm ' + '{0:.5f}'.format(func.GetParError(1))
#    
#        leg2.AddEntry(_f_, lstr , "")
#        leg2.AddEntry(_f_, lstr2 , "")
#        leg2.Draw()

    save(c, 'plots_gamma/' + header)


    return hist


if __name__ == '__main__':

    tfile = TFile('Myroot_dynamic95.root')
    tree = tfile.Get('per_photon')

    nbin = 1000

    makeEffPlotsVars(tree, 'photon_pt', 'abs(photon_deta)', 'photon_taupt > 20 && abs(photon_taueta) < 2.3 && photon_pt > 0.5 && photon_dm_rough !=-1', nbin, 0., 1, 'p_{T}^{e/#gamma} (GeV)', '#Delta#eta(#tau, e/#gamma)', 'Inclusive, 95% envelope', 'strip_pt_gamma_deta_inclusive_95', 'pt', 0.95)
    makeEffPlotsVars(tree, 'photon_pt', 'abs(photon_dphi)', 'photon_taupt > 20 && abs(photon_taueta) < 2.3 && photon_pt > 0.5 && photon_dm_rough !=-1', nbin, 0., 1, 'p_{T}^{e/#gamma} (GeV)', '#Delta#phi(#tau, e/#gamma)', 'Inclusive, 95% envelope', 'strip_pt_gamma_dphi_inclusive_95', 'pt', 0.95)
#    makeEffPlotsVars(tree, 'photon_pt', 'abs(photon_deta)', 'photon_gendm>=0 && photon_pt > 0.5 && photon_dm_rough !=-1', nbin, 0., 1, 'p_{T}^{#gamma} (GeV)', '#Delta#eta(#tau, #gamma)', 'Inclusive, 90% envelope', 'strip_pt_gamma_deta_inclusive_90', 'pt', 0.9)
#    makeEffPlotsVars(tree, 'photon_pt', 'abs(photon_dphi)', 'photon_gendm>=0 && photon_pt > 0.5 && photon_dm_rough !=-1', nbin, 0., 1, 'p_{T}^{#gamma} (GeV)', '#Delta#phi(#tau, #gamma)', 'Inclusive, 90% envelope', 'strip_pt_gamma_dphi_inclusive_90', 'pt', 0.9)


#    makeEffPlotsVars(tree, 'photon_pt', 'abs(photon_deta)', 'photon_gendm>=0 && photon_pt > 0.5 && abs(photon_eta) < 1.2', nbin, 0., 1, 'p_{T}^{#gamma} (GeV)', '#Delta#eta(#tau, #gamma^{iso.})', '1p1#pi^{0}, |#eta| < 1.2', 'strip_pt_gamma_deta_barrel', 'pt')
#    makeEffPlotsVars(tree, 'photon_pt', 'abs(photon_dphi)', 'photon_gendm>=0 && photon_pt > 0.5 && abs(photon_eta) < 1.2', nbin, 0., 1, 'p_{T}^{#gamma} (GeV)', '#Delta#phi(#tau, #gamma^{iso.})', '1p1#pi^{0}, |#eta| < 1.2', 'strip_pt_gamma_dphi_barrel', 'pt')

#    makeEffPlotsVars(tree, 'photon_pt', 'abs(photon_deta)', 'photon_gendm>=0 && photon_pt > 0.5 && abs(photon_eta) > 1.2 && abs(photon_eta) < 1.7', nbin, 0., 1, 'p_{T}^{#gamma} (GeV)', '#Delta#eta(#tau, #gamma^{iso.})', '1p1#pi^{0}, 1.2 < |#eta| < 1.7', 'strip_pt_gamma_deta_middleeta', 'pt')
#    makeEffPlotsVars(tree, 'photon_pt', 'abs(photon_dphi)', 'photon_gendm>=0 && photon_pt > 0.5 && abs(photon_eta) > 1.2 && abs(photon_eta) < 1.7', nbin, 0., 1, 'p_{T}^{#gamma} (GeV)', '#Delta#phi(#tau, #gamma^{iso.})', '1p1#pi^{0}, 1.2 < |#eta| < 1.7', 'strip_pt_gamma_dphi_middleeta', 'pt')

#    makeEffPlotsVars(tree, 'photon_pt', 'abs(photon_deta)', 'photon_gendm>=0 && photon_pt > 0.5 && abs(photon_eta) > 1.7', nbin, 0., 1, 'p_{T}^{#gamma} (GeV)', '#Delta#eta(#tau, #gamma^{iso.})', '1p1#pi^{0}, 1.7 < |#eta|', 'strip_pt_gamma_deta_endcap', 'pt')
#    makeEffPlotsVars(tree, 'photon_pt', 'abs(photon_dphi)', 'photon_gendm>=0 && photon_pt > 0.5 && abs(photon_eta) > 1.7', nbin, 0., 1, 'p_{T}^{#gamma} (GeV)', '#Delta#phi(#tau, #gamma^{iso.})', '1p1#pi^{0}, 1.7 < |#eta|', 'strip_pt_gamma_dphi_endcap', 'pt')


