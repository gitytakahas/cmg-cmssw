from officialStyle import officialStyle
from basic import *
from array import array
import ROOT

gROOT.SetBatch(True)
officialStyle(gStyle)
gStyle.SetOptTitle(0)
set_palette("color")
gStyle.SetPaintTextFormat("2.2f")

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

    leg.AddEntry(hist, 'gen p_{T} < 200 GeV', "l")
    leg.AddEntry(hist2, 'gen p_{T} > 200 GeV', "l")
    leg.Draw()

    save(c, 'plots/compare_' + var)



def makeHist(tree, var, sel, nbin, xmin, xmax, xtitle, ytitle, scale, leglabel = None, header='', printout=False, isText=True):
   
    c = TCanvas()
    hist = TH1F('h_comp', 'h_comp', nbin, xmin, xmax)
    hist.GetXaxis().SetTitle(xtitle)
    hist.GetYaxis().SetTitle(ytitle)
    hist.GetYaxis().SetNdivisions(507)
    hist.SetLineStyle(1)
    hist.SetMarkerStyle(1)
    hist.Sumw2()

    tree.Project(hist.GetName(), var, sel)

#    overflow(hist)

    if scale and hist.GetSumOfWeights()!=0:
        hist.Scale(1./hist.GetEntries())


    hist.SetLineWidth(3)
    hist.SetMarkerSize(2)
    hist.SetMaximum(hist.GetMaximum()*1.2)
    hist.SetMinimum(0)

    if isText:
        hist.Draw('htext')
    else:
        hist.Draw('h')
    leg = TLegend(0.1,0.93,0.5,0.99)
    LegendSettings(leg,1)

    if leglabel != None:
        leg.AddEntry(hist, leglabel.replace("pi0","#pi^{0}"), "")
        leg.Draw()

#    print var, var.find('pdgid')
    _dict = {'211':0, '11':0, '22':0, '-1':0}

    if var.find('pdgid')!=-1:
        for ibin in range(1, hist.GetXaxis().GetNbins()+1):
            if hist.GetBinContent(ibin)!=0:
#                print "PDG ID = ", hist.GetBinCenter(ibin), hist.GetBinContent(ibin)
                _key = str(abs(hist.GetBinCenter(ibin))).replace('.0','')

                print _key, hist.GetBinContent(ibin)
                if _key in ['211', '11', '22']:
                    _dict[_key] += hist.GetBinContent(ibin)
                else:
                    _dict['-1'] += hist.GetBinContent(ibin)

    print header, _dict

    if printout:
        print header, 'primary = ', hist.GetBinContent(2), ', secondary = ', hist.GetBinContent(1)
    save(c, 'junkplots/' + header  + var)

    


def makeEffPlotsVars(tree, varx, vary, sel, nbiny, ymin, ymax, xtitle, ytitle, leglabel = None, header=''):
   
    c = TCanvas()
    binning = [0,20,40,60,80,100,120,140,160,180,200,220,250,300,350,400]
    
    _hist_ = TH2F('h_effp', 'h_effp', len(binning)-1, array('d',binning), nbiny, ymin, ymax)
#    _hist_ = TH2F('h_effp', 'h_effp', 20,-2.5,2.5, nbiny, ymin, ymax)
    dname = vary + ':' + varx + ' >> ' + _hist_.GetName()
    tree.Draw(dname, sel)

    hist = _hist_.ProfileX()

    hist.GetXaxis().SetTitle(xtitle)
    hist.GetYaxis().SetTitle(ytitle)
    hist.GetYaxis().SetNdivisions(507)
    hist.SetLineWidth(3)


    func = ROOT.TF1("func", "[0]*x+[1]",hist.GetXaxis().GetXmin(), hist.GetXaxis().GetXmax())
    func_low = ROOT.TF1("func_low", "[0]*x+[1]")
#    hist.Fit("func")
#    _f_ = hist.GetFunction("func")
#    _f_.SetLineColor(1)
#    _f_.SetLineStyle(2)

#    import pdb; pdb.set_trace()
    hist.Draw("")
    hist.SetMinimum(0.)

#    _f_.Draw('same')
    
#    func_low.SetParameter(0, func.GetParameter(0))
#    func_low.SetParameter(1, func.GetParameter(1))
#    func_low.SetLineColor(2)
#    func_low.SetLineStyle(2)    
#    func_low.Draw('same')
    
    
    if header.find('eff')==-1:
        _hist_.SetMarkerColor(38)
        _hist_.SetMarkerSize(0.3)
#        _hist_.Draw("same")
        _hist_.Draw("colsame")
        hist.Draw('lepsame')

    hist.Draw("axissame")
#    _f_.Draw('same')

#    else:
#        hist.Draw('lep')
    

    leg = TLegend(0.1,0.93,0.5,0.99)
    LegendSettings(leg,1)

    if leglabel != None:
        leg.AddEntry(hist, leglabel.replace("pi0","#pi^{0}"), "")
        leg.Draw()

#    leg2 = TLegend(0.3,0.2,0.9,0.3)
#    LegendSettings(leg2,1)
#    lstr = 'slope : ' + '{0:.5f}'.format(func.GetParameter(0)) + ' #pm ' + '{0:.5f}'.format(func.GetParError(0))
#    lstr2 = 'intercept : ' + '{0:.5f}'.format(func.GetParameter(1)) + ' #pm ' + '{0:.5f}'.format(func.GetParError(1))
    
 #   leg2.AddEntry(_f_, lstr , "")
 #   leg2.AddEntry(_f_, lstr2 , "")
#    leg2.Draw()

    save(c, 'plots/' + header + varx + '_vs_' + vary.replace(' < 2',''))


if __name__ == '__main__':

    nbin = 1000
    tfile = TFile('Myroot.root')
    tree = tfile.Get('tree')

#    ddict = {'1p0pi0':0, '1p1pi0':1, '3p0pi0':2, 'Inclusive':-1}
    ddict = {'1p0pi0':0}
    
    print 'Primary versus Secondary'    
        
    for dkey, dm in sorted(ddict.items()):

        selection = 'tau_dm_rough == gen_dm_rough'

        if dkey != 'Inclusive':
            selection += '&& tau_dm_rough == ' + str(dm)

#        makeHist(tree, 'isPrimary', selection, 2,0,2, 'isPrimary', 'a.u.', True, dkey, 'isprimary_' + dkey + '_', True)
        makeHist(tree, 'seed_pdgid', selection, 5001,-2500.5,2500.5, 'secondary seed', 'a.u.', True, dkey, 'seed_pdgid_' + dkey + '_', False)

#        makeHist(tree, 'pseed_pdgid', selection, 1001,-500.5,500.5, 'parent seed', 'a.u.', True, dkey, 'pseed_pdgid_' + dkey + '_', False)
#        makeHist(tree, 'pseed_R', selection + ' && isPrimary==0 && abs(gamma_eta) <1', 130,0,130, 'last hit point [cm]', 'a.u.', True, dkey, 'R_' + dkey + '_', False, False)
        
#    makeHist(tree, 'isPrimary', 'tau_dm_rough==0 && gen_dm_rough==1', 2,0,2, 'isPrimary', 'a.u.', True, dkey,'canvas_off_')

