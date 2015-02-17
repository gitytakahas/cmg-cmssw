import os, numpy
from ROOT import TLegend, TCanvas, TColor, kMagenta, kOrange, kRed, kBlue, kGray, kBlack, gROOT, gStyle, TFile, TH1F, TH2F, TF1
from officialStyle import officialStyle

#gROOT.SetBatch(True)
gROOT.SetBatch(False)
officialStyle(gStyle)

gStyle.SetOptTitle(0)

nbin=50

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

def LegendSettings(leg):
    leg.SetBorderSize(0)
    leg.SetFillColor(10)
    leg.SetLineColor(0)
    leg.SetFillStyle(0)
    leg.SetTextSize(0.04)
    leg.SetTextFont(42)

def save(canvas, name):
    ensureDir('plots')
#    canvas.SaveAs(name.replace(' ','').replace('&&','')+'.pdf')
    canvas.SaveAs(name+'.gif')


def makeCompareVars(hist, scale, legname, isfit):
   
    c = TCanvas()

    print isfit

#    if scale and hist.GetSumOfWeights()!=0:
#        hist.Scale(1./hist.GetEntries())

    hist.SetLineWidth(3)
    hist.SetMarkerSize(0)
    hist.SetMaximum(hist.GetMaximum()*1.2)
    hist.SetMinimum(0)
    hist.Draw('ep')
    hist.GetXaxis().SetLabelSize(0.05)
    hist.GetYaxis().SetLabelSize(0.05)
    hist.GetXaxis().SetTitleOffset(1.2)
    hist.GetYaxis().SetTitleOffset(1.1)
    hist.GetYaxis().SetTitleSize(0.045)
    hist.GetYaxis().SetNdivisions(506)
    hist.GetXaxis().SetTitleSize(0.05)

    if isfit:
        func = TF1("func", "[0]*x",0., 1.5)
        func_low = TF1("func_low", "[0]*x",0., 0.5)
        hist.Fit("func","","",0.5, 1.5)
        _f_ = hist.GetFunction("func")
        _f_.SetLineColor(1)
        _f_.SetLineStyle(2)
        _f_.Draw('same')
        
        func_low.SetParameter(0, func.GetParameter(0))
        func_low.SetLineColor(2)
        func_low.SetLineStyle(2)    
        func_low.Draw('same')

#        import pdb;pdb.set_trace()

        print 'Slope = ', func.GetParameter(0), 'findbin = ', hist.FindBin(0.45)
        
        f_int = _f_.Integral(0, 0.5)        
        h_int = hist.Integral(0, hist.FindBin(0.45), "width")

        for ibin in range(1,6):
            print ibin, 'hist = ', hist.GetBinContent(ibin), 'func = ', _f_.Eval(hist.GetBinCenter(ibin)), 'Delta = ', hist.GetBinContent(ibin) - _f_.Eval(hist.GetBinCenter(ibin)) 

        print 'Integral func = ', f_int
        print 'Integral hist = ', h_int
        print 'Delta = ', h_int - f_int

        leg2 = TLegend(0.1,0.73,0.5,0.95)
        LegendSettings(leg2)
        
        lname = "E(Non-PU) = " + '{0:.2f}'.format((h_int - f_int)*10.) + ' GeV'
        leg2.AddEntry(hist, lname, "")
        leg2.Draw()


    leg = TLegend(0.05,0.93,0.5,0.99)
    LegendSettings(leg)

    leg.AddEntry(hist, legname.replace('nwhist_','').replace('whist_',''), "")
    leg.Draw()


    save(c, 'plots/compare_' + legname)


if __name__ == '__main__':

#    tfile = TFile('Myroot_SLHC.root')
    tfile = TFile('Myroot_run2.root')


    vardict = {
        'whist_Total':{'ytitle':'#sum E_{T} / 2#pi#DeltaR', 'xtitle':'#DeltaR from #tau axis'},
        'whist_1p0p0':{'ytitle':'#sum E_{T} / 2#pi#DeltaR', 'xtitle':'#DeltaR from #tau axis'},
        'whist_1p1p0':{'ytitle':'#sum E_{T} / 2#pi#DeltaR', 'xtitle':'#DeltaR from #tau axis'},
        'whist_3p0p0':{'ytitle':'#sum E_{T} / 2#pi#DeltaR', 'xtitle':'#DeltaR from #tau axis'},
        'whist_3p1p0':{'ytitle':'#sum E_{T} / 2#pi#DeltaR', 'xtitle':'#DeltaR from #tau axis'},
        'nwhist_Total':{'ytitle':'#sum E_{T} (GeV)', 'xtitle':'#DeltaR from #tau axis'},
        'nwhist_1p0p0':{'ytitle':'#sum E_{T} (GeV)', 'xtitle':'#DeltaR from #tau axis'},
        'nwhist_1p1p0':{'ytitle':'#sum E_{T} (GeV)', 'xtitle':'#DeltaR from #tau axis'},
        'nwhist_3p0p0':{'ytitle':'#sum E_{T} (GeV)', 'xtitle':'#DeltaR from #tau axis'},
        'nwhist_3p1p0':{'ytitle':'#sum E_{T} (GeV)', 'xtitle':'#DeltaR from #tau axis'}
        }
    
    
    for key, var in vardict.iteritems():

        print key

        h = tfile.Get(key)
    
        h.GetXaxis().SetTitle(var['xtitle'])
        h.GetYaxis().SetTitle(var['ytitle'])

        if key.find('nwhist')!=-1:
            makeCompareVars(h, False, key, True)
        else:
            makeCompareVars(h, False, key, False)

