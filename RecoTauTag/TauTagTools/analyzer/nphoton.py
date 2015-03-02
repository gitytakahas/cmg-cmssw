from officialStyle import officialStyle
from basic import *
from array import array
import ROOT

gROOT.SetBatch(True)
officialStyle(gStyle)
gStyle.SetOptTitle(0)
set_palette("color")

def createProfile(hist):

#    import pdb; pdb.set_trace()
    binning = [0,20,40,60,80,100,120,140,160,180,200,220,250,300,350,400]
    hist.Sumw2()    
#    _hist_ = TH2F('h_effp', 'h_effp', len(binning)-1, array('d',binning), nbiny, ymin, ymax)

    _hist1d_ = ROOT.TH1D(hist.GetName()+'_px', hist.GetName()+'_px', len(binning)-1, array('d',binning)) #hist.GetXaxis().GetNbins(), hist.GetXaxis().GetXmin(), hist.GetXaxis().GetXmax())

    for xbin in range(1, hist.GetXaxis().GetNbins()+1):
        hh = hist.ProjectionY("proj" + str(xbin), xbin, xbin)

        if hh.GetEntries() < 10: continue

        _hist1d_.SetBinContent(xbin, hh.GetMean())
        _hist1d_.SetBinError(xbin, hh.GetMeanError())  

        print xbin, hh.GetEntries(), hh.GetMean(), hh.GetRMS()

    return _hist1d_

def makeCompareVars(tree, var, sel1, sel2, nbin, xmin, xmax, xtitle, ytitle, scale):
   
    c = TCanvas()
    hist = TH1F('h_comp', 'h_comp', nbin, xmin, xmax)
    hist.GetXaxis().SetTitle(xtitle)
    hist.GetYaxis().SetTitle(ytitle)
    hist.GetYaxis().SetNdivisions(507)
    hist.SetLineColor(kRed)
    hist.Sumw2()

    hist2 = TH1F('h2_comp2', 'h2_comp2', nbin, xmin, xmax)
    hist2.GetXaxis().SetTitle(xtitle)
    hist2.GetYaxis().SetTitle(ytitle)
    hist2.GetYaxis().SetNdivisions(507)
    hist2.SetLineColor(kBlue)
    hist2.Sumw2()


    tree.Project(hist.GetName(), var, sel1)
    tree.Project(hist2.GetName(), var, sel2)

#    print var, sel1, hist.GetEntries()
#    print var, sel2, hist2.GetEntries()

    overflow(hist)
    overflow(hist2)

    if scale and hist.GetSumOfWeights()!=0:
        hist.Scale(1./hist.GetEntries())

    if scale and hist2.GetSumOfWeights()!=0:
        hist2.Scale(1./hist2.GetEntries())


#    import pdb; pdb.set_trace()
    hist.SetLineWidth(3)
    hist.SetLineStyle(2)
    hist.SetMarkerSize(0)
    hist.SetMaximum(hist.GetMaximum()*1.2)
    hist.SetMinimum(0)

    hist2.SetLineWidth(3)
    hist2.SetLineStyle(2)
    hist2.SetMarkerSize(0)
    hist2.SetMaximum(hist2.GetMaximum()*1.2)
    hist2.SetMinimum(0)

    if hist.GetMaximum() > hist2.GetMaximum():
        hist.SetMinimum(0)
        hist.Draw('h')
        hist2.Draw('hsame')
    else:
        hist2.SetMinimum(0)
        hist2.Draw('h')
        hist.Draw('hsame')
        

        
    leg = TLegend(0.16,0.93,0.91,0.99)
    LegendSettings(leg,2)

    leg.AddEntry(hist, 'gen p_{T} < 100 GeV', "l")
    leg.AddEntry(hist2, 'gen p_{T} > 100 GeV', "l")
    leg.Draw()

    save(c, 'plots/compare_' + var)




def makeCompareVars(tree, var, sel, nbin, xmin, xmax, xtitle, ytitle, scale, header = ''):
   
    c = TCanvas()
    hist = TH1F('h_comp', 'h_comp', nbin, xmin, xmax)
    hist.GetXaxis().SetTitle(xtitle)
    hist.GetYaxis().SetTitle(ytitle)
    hist.GetYaxis().SetNdivisions(507)
#    hist.SetLineColor(kRed)
    hist.Sumw2()

    tree.Project(hist.GetName(), var, sel)

    overflow(hist)

    if scale and hist.GetSumOfWeights()!=0:
        hist.Scale(1./hist.GetEntries())


    hist.SetLineWidth(3)
    hist.SetMarkerSize(0)
    hist.SetMaximum(hist.GetMaximum()*1.2)

    hist.SetMinimum(0)
    hist.Draw('h')

#    leg = TLegend(0.16,0.93,0.91,0.99)
#    LegendSettings(leg,2)

#    leg.AddEntry(hist, 'gen p_{T} < 100 GeV', "l")
#    leg.AddEntry(hist2, 'gen p_{T} > 100 GeV', "l")
#    leg.Draw()

    save(c, 'plots/compare_' + header + var)


    


def makeEffPlotsVars(tree, varx, vary, sel, nbiny, ymin, ymax, xtitle, ytitle, leglabel = None, header=''):
   
    c = TCanvas()
    binning = [0,20,40,60,80,100,120,140,160,180,200,220,250,300,350,400]
    
    _hist_ = TH2F('h_effp', 'h_effp', len(binning)-1, array('d',binning), nbiny, ymin, ymax)
    dname = vary + ':' + varx + ' >> ' + _hist_.GetName()
    tree.Draw(dname, sel)

    print leglabel, header
    hist = createProfile(_hist_)

#    hist = _hist_.ProfileX()

    hist.GetXaxis().SetTitle(xtitle)
    hist.GetYaxis().SetTitle(ytitle)
    hist.GetYaxis().SetNdivisions(507)
    hist.SetLineWidth(3)


    func = ROOT.TF1("func", "[0]*x+[1]",hist.GetXaxis().GetXmin(), hist.GetXaxis().GetXmax())
    func_low = ROOT.TF1("func_low", "[0]*x+[1]")
    hist.Fit("func")
    _f_ = hist.GetFunction("func")
    _f_.SetLineColor(1)
    _f_.SetLineStyle(2)

#    import pdb; pdb.set_trace()
    hist.Draw("")
    hist.SetMinimum(0.)
#    hist.SetMaximum(0.25)

#    _f_.Draw('same')
    
    func_low.SetParameter(0, func.GetParameter(0))
    func_low.SetParameter(1, func.GetParameter(1))
    func_low.SetLineColor(2)
    func_low.SetLineStyle(2)    
    _hist_.Draw("colzsame");
    hist.Draw("same");
    func_low.Draw('same')
    
    
    if header.find('eff')==-1:
        _hist_.SetMarkerColor(38)
        _hist_.SetMarkerSize(0.3)
#        _hist_.Draw("same")
#        _hist_.Draw("colsame")
        hist.Draw('lepsame')

    hist.Draw("axissame")
    _f_.Draw('same')

#    else:
#        hist.Draw('lep')

    leg = TLegend(0.1,0.93,0.5,0.99)
    LegendSettings(leg,1)

    if leglabel != None:
        if leglabel=='1p0pi0': leglabel = '#pi'
        elif leglabel == '1p1pi0': leglabel = '#pi#pi^{0}s'
        elif leglabel == '3p0pi0': leglabel = '#pi#pi#pi'

        leg.AddEntry(hist, leglabel, "")
        leg.Draw()

    leg2 = TLegend(0.3,0.2,0.9,0.3)
    LegendSettings(leg2,1)
    lstr = 'slope : ' + '{0:.5f}'.format(func.GetParameter(0)) + ' #pm ' + '{0:.5f}'.format(func.GetParError(0))
    lstr2 = 'intercept : ' + '{0:.5f}'.format(func.GetParameter(1)) + ' #pm ' + '{0:.5f}'.format(func.GetParError(1))
    
    leg2.AddEntry(_f_, lstr , "")
    leg2.AddEntry(_f_, lstr2 , "")
    leg2.Draw()

    save(c, 'plots/' + header + varx + '_vs_' + vary.replace(' < 2',''))


if __name__ == '__main__':

    nbin = 100

    ddict = {'1p0pi0':0, '1p1pi0':1, '3p0pi0':2, 'Inclusive':-1}
    
    tfile = TFile('Myroot_1prongOnly.root')
    tree = tfile.Get('per_tau')
    
    evardict = {
        'tau_nphoton':{'nbin':20, 'min':0, 'max':20, 'title':'number of #gamma'},
        }

    
        
    for key, tool in evardict.iteritems():
        for dkey, dm in sorted(ddict.items()):

            selection = 'tau_total_pt!=0 &&'

            if dkey=='Inclusive':
                selection += '1'
            else:
                selection += 'tau_dm_rough == tau_gendm_rough && tau_gendm_rough == ' + str(dm)


            makeCompareVars(tree, key, selection, tool['nbin'], tool['min'], tool['max'], 'Number of isolation photon', 'a.u.', True, 'nphoton_' + dkey + '_')

        
