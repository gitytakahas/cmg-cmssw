import os, numpy, math, copy, math, sys
from array import array
from ROOT import TLegend, TCanvas, TColor, kMagenta, kOrange, kRed, kBlue, kGray, kYellow, kBlack, gROOT, gStyle, TFile, TH1F, TH2F, TLatex, TLine, TH1D, TGraph, Double, TF1
from officialStyle import officialStyle

gROOT.SetBatch(True)
officialStyle(gStyle)
gStyle.SetOptTitle(0)
gStyle.SetOptStat(111111111)

threshold = 0.9

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
    ensureDir('plots_3p')
    canvas.SaveAs(name.replace(' ','').replace('&&','').replace(',Dynamic','')+'.pdf')
    canvas.SaveAs(name.replace(' ','').replace('&&','').replace(',Dynamic','')+'.gif')


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

        if hh.GetEntries() < 10: continue

        val = FindEdge(hh, threshold)
        err = math.sqrt(threshold*(1-threshold)/hh.GetEntries())
        upper_edge = FindEdge(hh, threshold+err)
        lower_edge = FindEdge(hh, threshold-err)

        if val==-1 or upper_edge==-1 or lower_edge == -1:
            continue

        print hh.GetEntries(), 'val = ', val, 'err = ', err, 'upper / lower = ', upper_edge, lower_edge
        _hist1d_.SetBinContent(xbin, val)
        errbar = (upper_edge + lower_edge)/2. - val
        _hist1d_.SetBinError(xbin, errbar)

    return _hist1d_



def Scan(tree, varx, vary, sel, nbinx, xmin, xmax, xtitle, leglabel = None, header='', addon=''):


    c = TCanvas()
    hist = TH2F('h_effp_' + addon, 'h_effp' + addon, 20,0,600,nbinx, xmin, xmax)

    dname = varx + ':tau_genpt >> ' + hist.GetName()
    tree.Draw(dname, sel)

    leg = TLegend(0.08,0.93,0.5,0.99)
    LegendSettings(leg, 1)

    hist_edge = createProfile(hist, threshold)
    hist_edge.GetXaxis().SetTitle(xtitle)
    hist_edge.GetYaxis().SetTitle("nIso_weight to achieve 90% eff.")
    hist_edge.GetYaxis().SetNdivisions(507)
    hist_edge.SetLineWidth(3)
    hist_edge.GetYaxis().SetTitleOffset(1.3)

    func = TF1("func", "[0]*x+[1]",hist.GetXaxis().GetXmin(), hist.GetXaxis().GetXmax())
    func_low = TF1("func_low", "[0]*x")


    func.SetParameter(0, 0.2)

    hist_edge.Fit("func","", "",hist.GetXaxis().GetXmin(), hist.GetXaxis().GetXmax())
    hist_edge.Draw("pl")
    hist_edge.SetLineColor(kRed)
    hist_edge.SetMarkerColor(kRed)
    hist_edge.SetMinimum(0.)
    hist_edge.SetMaximum(hist_edge.GetMaximum()*1.5)

    _f_ = hist_edge.GetFunction("func")
    _f_.SetLineColor(1)
    _f_.SetLineStyle(2)
    _f_.Draw("same")
#    import pdb; pdb.set_trace()
    print 'chi2 = ', _f_.GetChisquare()/_f_.GetNDF()

    hist.Draw("colzsame")
    hist_edge.Draw("plsame")
    func_low.SetParameter(0, func.GetParameter(0))
    func_low.SetLineColor(1)
    func_low.SetLineStyle(2)    
    func_low.Draw('same')
    

#    hist_edge.Draw("axissame")





#    value = []
#    
#    flag =  False
# 
#    for k in range(0, 1000):
#        cutoff = 2. + k*0.1
#        bin_high = hist.FindBin(cutoff)
#        eff = hist.Integral(0, bin_high-1)/hist.Integral(0, hist.GetNbinsX()+1)
#        value.append([Double(k*0.1), eff])
#
#    gr = TGraph()
#
#    for ii, ivalue in enumerate(value):
#
#        x,y = ivalue
#        gr.SetPoint(ii, x, y)
#
#    gr.SetMarkerSize(0.5)
#    gr.GetXaxis().SetRangeUser(-2,100)
#    gr.GetYaxis().SetRangeUser(0,1)
#    gr.GetXaxis().SetTitle('parameter : k')
#    gr.GetYaxis().SetTitle('efficiency')
#    gr.Draw("apl")
#
#    leg2 = TLegend(0.8,0.93,0.9,0.99)
#    LegendSettings(leg2, 1)
#    leg2.AddEntry(gr, runtype, "")
#    leg2.Draw()
#
#    leg = TLegend(0.08,0.93,0.5,0.99)
#    LegendSettings(leg, 1)
#    leg.AddEntry(gr, addon.replace('pi0','#pi^{0}'), "")
#    leg.Draw()
#
    save(c, 'plots_3p/' + header)


    
    

if __name__ == '__main__':

    filename = 'Myroot_mssm.root'

    hdict = {
        'dynamic':{'file':filename,'label':'Dynamic'},
        }

    ddict = {
             '3p':'tau_dm_rough==2'
             }

    region = {'All eta':'1'}

    valdict = {
        'nIso_weight_ciso_outer':{'tree':'per_tau',
                                  'var':'tau_niso_weighted', 
                                  'nbin':1000, 'xmin':0., 'xmax':100, 
                                  'title':'nIso weighted', 
                                  'sel':'tau_dm!=-1 && tau_pt > 20 && abs(tau_eta) < 2.3 && tau_ciso < 2 && (tau_photonsumpt_outside/tau_pt) < 0.2*tau_pt',
                                  'name':'nIso_weight_ciso_outer'},
        }

    

    for vkey, ivar in valdict.iteritems():
        for rkey, rval in region.iteritems():
            for dkey, dm in ddict.iteritems():

                hists = []

                for key, val in sorted(hdict.iteritems()):
                
                    tfile = TFile(val['file'])
                    tree = tfile.Get(ivar['tree'])
                    
                    Scan(tree, 'tau_niso_weighted', ivar['var'], ivar['sel'] + ' && ' + dm + '&&' + rval, ivar['nbin'], ivar['xmin'], ivar['xmax'], 'gen tau pT^{vis} (GeV)', ivar['title'], rkey + '_' + dkey + ', ' + val['label'], dkey + ', ' +rkey)




