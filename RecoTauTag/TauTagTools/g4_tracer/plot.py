from officialStyle import officialStyle
from basic import *
from array import array
#from ROOT import 

gROOT.SetBatch(True)
officialStyle(gStyle)
gStyle.SetOptTitle(0)
set_palette("color")

gStyle.SetPadLeftMargin(0.17)
gStyle.SetPadRightMargin(0.12)

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

def makeCompareVars(tree, var, sel, nbin, xmin, xmax, xtitle, ytitle, scale, header='', anal = False):
   
    c = TCanvas()
    hist = TH1F('h_comp', 'h_comp', nbin, xmin, xmax)
    hist.GetXaxis().SetTitle(xtitle)
    hist.GetYaxis().SetTitle(ytitle)
    hist.GetYaxis().SetNdivisions(507)
    hist.GetYaxis().SetTitleOffset(1.3)
#    hist.SetLineColor(kRed)
    hist.Sumw2()

    tree.Project(hist.GetName(), var, sel)
#    overflow(hist)

    if scale and hist.GetSumOfWeights()!=0:
#        hist.Scale(1./hist.GetEntries())
        hist.Scale(1./hist.GetSumOfWeights())

    hist.SetLineWidth(3)
#    hist.SetLineStyle(2)
    hist.SetMarkerSize(0)
    hist.SetMaximum(hist.GetMaximum()*1.2)
    hist.SetMinimum(0)


    hist.Draw('h')
        
    leg = TLegend(0.16,0.93,0.91,0.99)
    LegendSettings(leg,2)

    save(c, 'plots/plot_' + header)


    if anal == True:
        print 'analyze', header
        
        for ibin in range(1, hist.GetXaxis().GetNbins()):
            if hist.GetBinContent(ibin) > 0:
                print header, ibin-1, '{0:.1f}'.format(100*hist.GetBinContent(ibin))

    

def makeCompareVars2(tree, var, sel1, sel2, nbin, xmin, xmax, xtitle, ytitle, scale):
   
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
    hist.SetLineWidth(2)
#    hist.SetLineStyle(2)
    hist.SetMarkerSize(0)
    hist.SetMaximum(hist.GetMaximum()*1.2)
    hist.SetMinimum(0)

    hist2.SetLineWidth(3)
#    hist2.SetLineStyle(2)
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
        

        
    leg = TLegend(0.5,0.73,0.9,0.9)
    LegendSettings(leg,1)

    leg.AddEntry(hist, 'Had. Inelastic', "l")
    leg.AddEntry(hist2, 'Early shower', "l")
    leg.Draw()

    save(c, 'plots/compare_' + var)


def makeCompareVars3(tree, var, sel1, sel2, sel3, nbin, xmin, xmax, xtitle, ytitle, scale):
   
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

    hist3 = TH1F('h2_comp3', 'h2_comp3', nbin, xmin, xmax)
    hist3.GetXaxis().SetTitle(xtitle)
    hist3.GetYaxis().SetTitle(ytitle)
    hist3.GetYaxis().SetNdivisions(507)
    hist3.SetLineColor(kBlack)
    hist3.Sumw2()


    tree.Project(hist.GetName(), var, sel1)
    tree.Project(hist2.GetName(), var, sel2)
    tree.Project(hist3.GetName(), var, sel3)

#    print var, sel1, hist.GetEntries()
#    print var, sel2, hist2.GetEntries()

    overflow(hist)
    overflow(hist2)
    overflow(hist3)

    if scale and hist.GetSumOfWeights()!=0:
        hist.Scale(1./hist.GetEntries())

    if scale and hist2.GetSumOfWeights()!=0:
        hist2.Scale(1./hist2.GetEntries())

    if scale and hist3.GetSumOfWeights()!=0:
        hist3.Scale(1./hist3.GetEntries())


#    import pdb; pdb.set_trace()
    hist.SetLineWidth(2)
#    hist.SetLineStyle(2)
    hist.SetMarkerSize(0)
    hist.SetMaximum(hist.GetMaximum()*1.2)
    hist.SetMinimum(0)

    hist2.SetLineWidth(3)
#    hist2.SetLineStyle(2)
    hist2.SetMarkerSize(0)
    hist2.SetMaximum(hist2.GetMaximum()*1.2)
    hist2.SetMinimum(0)

    hist3.SetLineWidth(3)
#    hist3.SetLineStyle(2)
    hist3.SetMarkerSize(0)
    hist3.SetMaximum(hist2.GetMaximum()*1.2)
    hist3.SetMinimum(0)

    if hist.GetMaximum() > hist2.GetMaximum():
        hist.SetMinimum(0)
        hist.Draw('h')
        hist2.Draw('hsame')
        hist3.Draw('hsame')
    else:
        hist2.SetMinimum(0)
        hist2.Draw('h')
        hist.Draw('hsame')
        hist3.Draw('hsame')
        

        
    leg = TLegend(0.5,0.73,0.9,0.9)
    LegendSettings(leg,1)

    leg.AddEntry(hist, 'Had. Inelastic', "l")
    leg.AddEntry(hist2, 'Early shower', "l")
    leg.AddEntry(hist3, 'Conversions', "l")
    leg.Draw()

    save(c, 'plots/compare_' + var)




def makeEffPlotsVars(tree, varx, vary, sel, nbiny, ymin, ymax, xtitle, ytitle, leglabel = None, header='', ispt = 'pt'):
   
    c = TCanvas()
    binning = [0,20,40,60,80,100,120,140,160,180,200,220,250,300,350,400]
    binning_e = [0,20,40,60,80,100,120,140,160,180,200,220,250,300,350,400,600,800,1000,1500]

    if ispt == 'pt':
        _hist_ = TH2F('h_effp', 'h_effp', len(binning)-1, array('d',binning), nbiny, ymin, ymax)
    elif ispt == 'e':
        _hist_ = TH2F('h_effp', 'h_effp', len(binning_e)-1, array('d',binning_e), nbiny, ymin, ymax)
    elif ispt == 'eta':
        _hist_ = TH2F('h_effp', 'h_effp', 20,-2.5,2.5, nbiny, ymin, ymax)
    elif ispt == 'others':
        _hist_ = TH2F('h_effp', 'h_effp', 40,0, 122.3, nbiny, ymin, ymax)

    dname = vary + ':' + varx + ' >> ' + _hist_.GetName()
    tree.Draw(dname, sel)

    hist = _hist_.ProfileX()

    print '='*60
    print header, '# of entries = ', hist.GetEntries()
    print '='*60

    hist.GetXaxis().SetTitle(xtitle)
    hist.GetYaxis().SetTitle(ytitle)
    hist.GetYaxis().SetNdivisions(507)
    hist.SetLineWidth(3)


#    func = ROOT.TF1("func", "[0]*x+[1]",hist.GetXaxis().GetXmin(), hist.GetXaxis().GetXmax())
#    func_low = ROOT.TF1("func_low", "[0]*x+[1]")

#    if ispt != 'eta':
#        hist.Fit("func")
#        _f_ = hist.GetFunction("func")
#        _f_.SetLineColor(1)
#        _f_.SetLineStyle(2)

    hist.Draw("")
    hist.SetMinimum(0.)
    hist.SetMaximum(1)

#    if ispt != 'eta':
#        _f_.Draw('same')
#    
#        func_low.SetParameter(0, func.GetParameter(0))
#        func_low.SetParameter(1, func.GetParameter(1))
#        func_low.SetLineColor(2)
#        func_low.SetLineStyle(2)    
#        func_low.Draw('same')
    
    
    if header.find('eff')==-1:
        _hist_.SetMarkerColor(38)
        _hist_.SetMarkerSize(0.3)
        _hist_.Draw("colzsame")
        hist.Draw('lepsame')

    hist.Draw("axissame")

#    if ispt != 'eta':
#        _f_.Draw('same')


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

    save(c, 'plots/' + header)




if __name__ == '__main__':

    nbin = 100

    vardict = {
        'isN':{'nbin':20, 'min':0, 'max':20, 'title':'Number of photons'},
        'isNHad':{'nbin':10, 'min':0, 'max':10, 'title':'Number of Had. Inelastic'},
#        'isHad_minR':{'nbin':200, 'min':0, 'max':122.3, 'title':'First Had. Inelastic Radius (cm)'},
        }


    
    tfile = TFile('output_allDecay.root')
    tree = tfile.Get('event')
    
    for key, tool in vardict.iteritems():
        selection = ''

        makeCompareVars(tree, key, '', tool['nbin'], tool['min'], tool['max'], tool['title'], 'a.u.', True, key)


    makeCompareVars(tree, 'tau_pt/tau_genpt', 'isHad==1', 50,0,2, 'tau p_{T} / gen. tau p_{T}', 'a.u.', True, 'isHad')
    makeCompareVars(tree, 'tau_pt/tau_genpt', 'isPrim==1', 50,0,2, 'tau p_{T} / gen. tau p_{T}', 'a.u.', True, 'isPrim')
    makeCompareVars(tree, 'tau_pt/tau_genpt', '', 50,0,2, 'tau p_{T} / gen. tau p_{T}^{vis}', 'a.u.', True, 'inclusive')


    makeEffPlotsVars(tree, 'tau_genpt', 'isHad > 0.5', '', 2, -0.5,1.5, 'gen. tau p_{T} (GeV)', 'Fraction of Had. Inelastic', 'all', 'eff_pt', 'pt')
    makeEffPlotsVars(tree, 'tau_genpt', 'isHad > 0.5', 'abs(tau_geneta) < 1', 2, -0.5,1.5, 'gen. tau p_{T} (GeV)', 'Fraction of Had. Inelastic', 'all', 'eff_pt_etacut', 'pt')
    makeEffPlotsVars(tree, 'tau_geneta', 'isHad > 0.5', '', 2, -0.5,1.5, 'gen. tau #eta', 'Fraction of Had. Inelastic', 'all', 'eff_eta', 'eta')
    makeEffPlotsVars(tree, 'tau_genpt', 'isNHad', '', 10, 0,10, 'gen. tau p_{T} (GeV)', '# of Had. Inelastic', 'all', 'nhad_pt', 'pt')
    makeEffPlotsVars(tree, 'tau_genpt', 'isNHad', 'abs(tau_geneta) < 1', 10, 0,10, 'gen. tau p_{T} (GeV)', '# of Had. Inelastic', 'all', 'nhad_pt_etacut', 'pt')
    makeEffPlotsVars(tree, 'tau_geneta', 'isNHad', '', 10, 0,10, 'gen. tau #eta', '# of Had. Inelastic', 'all', 'nhad_eta', 'eta')

    makeEffPlotsVars(tree, 'isHad_minR', 'tau_pt/tau_genpt', '', 30, 0, 1., 'R_{Had}^{min} (cm)', 'tau p_{T} / gen. tau p_{T}', 'all', 'ratio_pt', 'others')

    tree = tfile.Get('detail')

    dvardict = {
        'Had_R':{'nbin':80, 'min':0, 'max':122.3, 'title':'Had. Inelastic Radius (cm)'},
        }

    for key, tool in dvardict.iteritems():
        selection = ''

        makeCompareVars(tree, key, selection, tool['nbin'], tool['min'], tool['max'], tool['title'], 'a.u.', True, 'Had_R')
        makeCompareVars(tree, key, 'abs(Had_R_eta) < 1.', tool['nbin'], tool['min'], tool['max'], tool['title'], 'a.u.', True, 'Had_R_eta1_')



    tree = tfile.Get('photon')

    pvardict = {
        'last_seed_process':{'nbin':210, 'min':0, 'max':210, 'title':'Last process'},
#        'last_seed_pt':{'nbin':50, 'min':0, 'max':50, 'title':'pT'},
        }

    ptype = {'pion':0, 'electron':1, 'photon':2, 'pn':3, 'others':4}

    for key, tool in pvardict.iteritems():
        for dkey, dm in sorted(ptype.items()):

            selection = 'last_seed == ' + str(dm)
            print selection
            makeCompareVars(tree, key, selection, tool['nbin'], tool['min'], tool['max'], tool['title'], 'a.u', True, dkey + '_', True)


    h = TH1F('h','h',5,0,5)
    tree.Draw('last_seed >> h')
#    h.Scale(1/h.GetEntries())
    
    print 'pion', '{0:.1f}'.format(100*h.GetBinContent(1))
    print 'e', '{0:.1f}'.format(100*h.GetBinContent(2))
    print 'photon', '{0:.1f}'.format(100*h.GetBinContent(3))
    print 'p/n', '{0:.1f}'.format(100*h.GetBinContent(4))
    print 'others', '{0:.1f}'.format(100*h.GetBinContent(5))



    gvardict = {
        'iso_gamma_dR':{'nbin':50, 'min':0, 'max':0.5, 'title':'#DeltaR (reco. #tau, #gamma)'},
        'iso_gamma_pt':{'nbin':50, 'min':0, 'max':10, 'title':'p_{T}^{#gamma, iso} (GeV)'},
        }

    tree = tfile.Get('iso_gamma_detail')

    for key, tool in gvardict.iteritems():
        makeCompareVars3(tree, key, 'iso_gamma_isHad==1 && iso_gamma_isConvHad==0', 'iso_gamma_isPrim==1', 'iso_gamma_isConvOnly==1', tool['nbin'], tool['min'], tool['max'], tool['title'], 'a.u.', True)
