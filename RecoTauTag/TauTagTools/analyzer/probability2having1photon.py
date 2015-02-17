from officialStyle import officialStyle
from basic import *
from array import array
import ROOT

gROOT.SetBatch(True)
officialStyle(gStyle)
gStyle.SetOptTitle(0)
set_palette("color")

def createProfile(hist):

    binning = [0,20,40,60,80,100,120,140,160,180,200,220,250,300,350,400]
    hist.Sumw2()    
#    _hist_ = TH2F('h_effp', 'h_effp', len(binning)-1, array('d',binning), nbiny, ymin, ymax)

    _hist1d_ = ROOT.TH1D(hist.GetName()+'_px', hist.GetName()+'_px', hist.GetXaxis().GetNbins(), hist.GetXaxis().GetXmin(), hist.GetXaxis().GetXmax())

    for xbin in range(1, hist.GetXaxis().GetNbins()+1):
        hh = hist.ProjectionY("proj" + str(xbin), xbin, xbin)

        if hh.GetEntries() < 10: continue

        _hist1d_.SetBinContent(xbin, hh.GetMean())
        _hist1d_.SetBinError(xbin, hh.GetMeanError())  

        print xbin, hh.GetEntries(), hh.GetMean(), hh.GetRMS()

    return _hist1d_


def makeEffPlotsVars(tree, varx, vary, sel, nbiny, ymin, ymax, xtitle, ytitle, leglabel = None, header='', ispt = True):
   
    c = TCanvas()
    binning = [0,20,40,60,80,100,120,140,160,180,200,220,250,300,350,400]

    if ispt:
        _hist_ = TH2F('h_effp', 'h_effp', len(binning)-1, array('d',binning), nbiny, ymin, ymax)
    else:
        _hist_ = TH2F('h_effp', 'h_effp', 20,-2.5,2.5, nbiny, ymin, ymax)

    dname = vary + ':' + varx + ' >> ' + _hist_.GetName()
    tree.Draw(dname, sel)

    hist = _hist_.ProfileX()

    print header, '# of entries = ', hist.GetEntries()

    hist.GetXaxis().SetTitle(xtitle)
    hist.GetYaxis().SetTitle(ytitle)
    hist.GetYaxis().SetNdivisions(507)
    hist.SetLineWidth(3)


    func = ROOT.TF1("func", "[0]*x+[1]",hist.GetXaxis().GetXmin(), hist.GetXaxis().GetXmax())
    func_low = ROOT.TF1("func_low", "[0]*x+[1]")

    if ispt:
        hist.Fit("func")
        _f_ = hist.GetFunction("func")
        _f_.SetLineColor(1)
        _f_.SetLineStyle(2)

    hist.Draw("")
    hist.SetMinimum(0.)

    if ispt:
        _f_.Draw('same')
    
        func_low.SetParameter(0, func.GetParameter(0))
        func_low.SetParameter(1, func.GetParameter(1))
        func_low.SetLineColor(2)
        func_low.SetLineStyle(2)    
        func_low.Draw('same')
    
    
    if header.find('eff')==-1:
        _hist_.SetMarkerColor(38)
        _hist_.SetMarkerSize(0.3)
#        _hist_.Draw("colsame")
        hist.Draw('lepsame')

    hist.Draw("axissame")

    if ispt:
        _f_.Draw('same')


    leg = TLegend(0.1,0.93,0.5,0.99)
    LegendSettings(leg,1)

    if leglabel != None:
        if leglabel=='1p0pi0': leglabel = '#pi'
        elif leglabel == '1p1pi0': leglabel = '#pi#pi^{0}s'
        elif leglabel == '3p0pi0': leglabel = '#pi#pi#pi'

        leg.AddEntry(hist, leglabel, "")
        leg.Draw()

    if ispt:
        leg2 = TLegend(0.3,0.2,0.9,0.3)
        LegendSettings(leg2,1)
        lstr = 'slope : ' + '{0:.5f}'.format(func.GetParameter(0)) + ' #pm ' + '{0:.5f}'.format(func.GetParError(0))
        lstr2 = 'intercept : ' + '{0:.5f}'.format(func.GetParameter(1)) + ' #pm ' + '{0:.5f}'.format(func.GetParError(1))
    
        leg2.AddEntry(_f_, lstr , "")
        leg2.AddEntry(_f_, lstr2 , "")
        leg2.Draw()

    save(c, 'plots/' + header)


if __name__ == '__main__':

    nbin = 1000

    ddict = {'1p0pi0':0, '1p1pi0':1, '3p0pi0':2, 'Inclusive':-1}
    
    tfile = TFile('Myroot.root')
    tree = tfile.Get('per_tau')
    
    for dkey, dm in sorted(ddict.items()):

        selection = 'tau_dm_rough == tau_gendm_rough'

        if dkey != 'Inclusive':
            selection += '&& tau_gendm_rough == ' + str(dm)

        print dkey, selection
        makeEffPlotsVars(tree, 'tau_geneta', '(tau_nphoton > 0)', selection, 2, -0.5,1.5, 'gen. tau #eta^{vis}', '#varepsilon (# of photons #geq 1)', dkey, 'eff_eta_ecanvas_' + dkey, False)

#        makeEffPlotsVars(tree, 'tau_genpt', '(tau_nphoton > 0)', selection, 2, -0.5,1.5, 'gen. tau p_{T}^{vis}', '#varepsilon (# of photons #geq 1)', dkey, 'eff_pt_ecanvas_' + dkey, True)
        

#        makeEffPlotsVars(tree, 'tau_geneta', '(tau_nphoton > 0)', selection + ' && tau_nphoton > 0', 2, -0.5,1.5, 'gen. tau #eta^{vis}', '#varepsilon (# of photons #geq 1)', dkey, 'eff_eta_ecanvas_' + dkey, False)

#        makeEffPlotsVars(tree, 'tau_genpt', '(tau_nphoton > 0)', selection + ' && tau_nphoton > 0', 2, -0.5,1.5, 'gen. tau p_{T}^{vis}', '#varepsilon (# of photons #geq 1)', dkey, 'eff_pt_ecanvas_' + dkey, True)
        
