from officialStyle import officialStyle
from basic import *
from array import array
import ROOT

#gROOT.SetBatch(True)
officialStyle(gStyle)
gStyle.SetOptTitle(0)
set_palette("color")
gStyle.SetPaintTextFormat("2.2f")
#gStyle.SetPaintTextFormat("2.0f")

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


    for rtype in ['dynamic95', 'standard', 'run1']:

        tfile = TFile('Myroot_' + rtype + '.root')
        tree = tfile.Get('per_tau')
    
        hname = 'hcor_' + rtype
        hcor = TH2F(hname, hname,  13,-1,12,13,-1,12)
        tree.Draw('tau_dm:tau_gendm >> ' + hname, '&& tau_pt > 20 && abs(tau_eta) < 2.3')

        hgcor =  TH2F('hgcor_' + rtype, 'hgcor_' + rtype, 5,0,5,5,0,5)


        cnt_1p = 0
        cnt_1pp = 0
        cnt_2p = 0
        cnt_3p = 0
        cnt_na = 0

        for ii in range(1, hcor.GetYaxis().GetNbins()):
            total = hcor.GetBinContent(1, ii)
            if ii==1: cnt_1p += hcor.GetBinContent(1, ii)
            elif (ii==2 or ii==3): cnt_1pp += hcor.GetBinContent(1, ii)
            elif (ii==5 or ii==6): cnt_2p += hcor.GetBinContent(1, ii)
            elif ii==11 : cnt_3p += hcor.GetBinContent(1, ii)
            elif ii==-1: cut_na += hcor.GetBinContent(1, ii)
                

        cnt_total = cnt_1p + cnt_1pp + cnt_3p
#        cnt_total = 1

        hgcor.SetBinContent(1,1,cnt_1p/cnt_total)
        hgcor.SetBinContent(1,2,cnt_1pp/cnt_total)
        hgcor.SetBinContent(1,3,cnt_3p/cnt_total)


        cnt_1p = 0
        cnt_1pp = 0
        cnt_3p = 0

        for ix in range(2, 4):
            for ii in range(1, hcor.GetYaxis().GetNbins()):
                total = hcor.GetBinContent(ix, ii)
                if ii==1: cnt_1p += hcor.GetBinContent(ix, ii)
                elif (ii==2 or ii==3): cnt_1pp += hcor.GetBinContent(ix, ii)
                elif ii==11 : cnt_3p += hcor.GetBinContent(ix, ii)


        cnt_total = cnt_1p + cnt_1pp + cnt_3p
#        cnt_total = 1

        hgcor.SetBinContent(2,1,cnt_1p/cnt_total)
        hgcor.SetBinContent(2,2,cnt_1pp/cnt_total)
        hgcor.SetBinContent(2,3,cnt_3p/cnt_total)

        cnt_1p = 0
        cnt_1pp = 0
        cnt_3p = 0

        for ii in range(1, hcor.GetYaxis().GetNbins()):
            total = hcor.GetBinContent(11, ii)
            if ii==1: cnt_1p += hcor.GetBinContent(11, ii)
            elif (ii==2 or ii==3): cnt_1pp += hcor.GetBinContent(11, ii)
            elif ii==11 : cnt_3p += hcor.GetBinContent(11, ii)


        cnt_total = cnt_1p + cnt_1pp + cnt_3p
#        cnt_total = 1

        hgcor.SetBinContent(3,1,cnt_1p/cnt_total)
        hgcor.SetBinContent(3,2,cnt_1pp/cnt_total)
        hgcor.SetBinContent(3,3,cnt_3p/cnt_total)
        
        hgcor.GetXaxis().SetTitle('Generated #tau_{h} mode')
        hgcor.GetYaxis().SetTitle('Reconstructed #tau_{h} mode')
        hgcor.GetXaxis().SetBinLabel(1, '#pi')
        hgcor.GetXaxis().SetBinLabel(2, '#pi#pi^{0}s')
        hgcor.GetXaxis().SetBinLabel(3, '#pi#pi#pi')
        hgcor.GetYaxis().SetBinLabel(1, '#pi')
        hgcor.GetYaxis().SetBinLabel(2, '#pi#pi^{0}s')
        hgcor.GetYaxis().SetBinLabel(3, '#pi#pi#pi')
        hgcor.SetMarkerSize(2.3)

        ce = TCanvas('correlation_' + rtype)
        hgcor.Draw("text")
#        ce.SaveAs('cor_abs_' + rtype + '.gif')
#        ce.SaveAs('cor_abs_' + rtype + '.pdf')
        ce.SaveAs('cor_' + rtype + '.gif')
        ce.SaveAs('cor_' + rtype + '.pdf')

