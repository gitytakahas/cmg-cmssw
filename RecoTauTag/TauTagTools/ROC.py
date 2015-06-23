import os, numpy, math, copy, math
from ROOT import TLegend, TCanvas, TColor, kMagenta, kOrange, kRed, kBlue, kGray, kBlack, gROOT, gStyle, TFile, TH1F, TH2F, TLatex, TLine, TGraph, Double
from officialStyle import officialStyle

gROOT.SetBatch(True)
officialStyle(gStyle)
gStyle.SetOptTitle(0)
gStyle.SetOptStat(0)

gStyle.SetPadLeftMargin  (0.15)
#gStyle.SetPadRightMargin (0.07)


col_qcd = TColor.GetColor(250,202,255)
col_tt  = TColor.GetColor(155,152,204)
col_ewk = TColor.GetColor(222,90,106)
col_zll = TColor.GetColor(100,182,232)
col_ztt = TColor.GetColor(248,206,104)

def rocCurve(hS, hB, efS, efB):
  ''' Create a ROC TGraph from two input histograms.'''

  maxBinX = hS.GetNbinsX()
  maxBinY = hS.GetNbinsY()

  if hS.Integral() == 0.:
    print 'ROC curve creator, hist', hS.GetName(), 'has zero entries'
    return

  effsS = []
  rejB = []
  
  for ix in range(0, maxBinX + 1):
    for iy in range(0, maxBinY + 1):

      if hS.Integral(0,ix,0,iy)==0 or hB.Integral(0,ix,0,iy)==0: continue

      eff = efS*hS.Integral(0, ix, 0, iy)/hS.Integral(0, maxBinX+1, 0, maxBinY+1)
      bkg = efB*hB.Integral(0, ix, 0, iy)/hB.Integral(0, maxBinX+1, 0, maxBinY+1)
      
      effsS.append(eff)
      rejB.append(bkg)
  

  rocCurve = TGraph(len(effsS), numpy.asarray(effsS), numpy.asarray(rejB))
  return rocCurve

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

def LegendSettings(leg, ncolumn):
    leg.SetNColumns(ncolumn)
    leg.SetBorderSize(0)
    leg.SetFillColor(10)
    leg.SetLineColor(0)
    leg.SetFillStyle(0)
    leg.SetTextSize(0.03)
    leg.SetTextFont(42)

def save(canvas, name):
    ensureDir('plots_roc')
#    canvas.SaveAs(name.replace(' ','').replace('&&','')+'.pdf')
    canvas.SaveAs(name.replace(' ','').replace('&&','')+'.gif')


def makeCompareVars(hists, xtitle, ytitle, scale ,savestr, ncolumn, addon = ''):
   
  c = TCanvas()
#  c.SetLogy()
  col = [1, 2, 4, 4, 8, 6, 30, 40, 50]

  for ii, pack in enumerate(hists):

    hist, eff = pack

    hist.GetXaxis().SetTitle(xtitle)
    hist.GetYaxis().SetTitle(ytitle)
    hist.GetYaxis().SetNdivisions(505)
    hist.GetXaxis().SetNdivisions(505)

    if hist.GetTitle().find('PY')!=-1:
            
      for ibin in range(1, hist.GetXaxis().GetNbins()+1):
        hist.SetBinError(ibin, 0)

      hist.SetFillStyle(1)
      hist.SetFillColor(col_qcd)
      hist.SetLineColor(col_qcd)
      hist.SetLineWidth(0)
    else:
      hist.SetLineColor(col[ii])
      hist.SetLineWidth(len(hists)+1-ii)

    hist.SetMarkerSize(0)
    hist.SetMinimum(0)
#    hist.SetMinimum(0.1)

    if scale and hist.GetSumOfWeights()!=0:
      hist.Scale(1./abs(hist.GetSumOfWeights()))
      hist.SetMaximum(hist.GetMaximum()*1.2)
      hist.SetMinimum(0)

  ymax = max([ihist[0].GetMaximum() for ihist in hists])
  ymin = min([ihist[0].GetMinimum() for ihist in hists])

  leg = TLegend(0.2,0.93,0.6,0.99)
  LegendSettings(leg, ncolumn)

  for ii, pack in enumerate(hists):
    hist, eff = pack

    hist.SetMaximum(ymax*1.2)

    if ii==0:
      if hist.GetTitle().find('PY')!=-1:
        hist.Draw('h')
      else:
        hist.Draw('hep')

    else:
      if hist.GetTitle().find('PY')!=-1:
        hist.Draw('hsame')
      else:
        hist.Draw('hepsame')

    if hist.GetTitle().find('PY')!=-1:
      leg.AddEntry(hist, hist.GetTitle(), "f")
    else:
      leg.AddEntry(hist, hist.GetTitle(), "l")

    hists[-1][0].Draw("axissame")
    leg.Draw()

    leg2 = TLegend(0.16,0.85,0.4,0.92)
    LegendSettings(leg2, 1)
    leg2.AddEntry(hists[-1][0], addon.replace('_', ', '), "")
    leg2.Draw()

    save(c, 'plots_roc/' + savestr)


def overlay(hists, header):

    canvas = TCanvas()
    leg = TLegend(0.16,0.93,0.85,1.0)
    lname = header.replace('pi0','#pi^{0}')

    legleg = TLegend(0.2,0.85,0.4,0.92)
    LegendSettings(legleg, 1)
    LegendSettings(leg,len(hists))

    col = [1,2,4,6]

#    frame = TH2F('frame_' + header, 'frame_' + header, 10,0.,1.,10,0,0.1)
    frame = TH2F('frame_' + header, 'frame_' + header, 10,0.,1.,10,0,1.)
    frame.GetXaxis().SetTitle('Signal eff.')
    frame.GetYaxis().SetTitle('Background eff.')
    frame.GetYaxis().SetNdivisions(506)
    frame.Draw()

    x_min = Double(1000.)
    y_min = Double(1000.)
    x_max = Double(-1000.)
    y_max = Double(-1000.)


    for ii, pack in enumerate(hists):
      hist, label = pack

      hist.SetLineColor(col[ii])
      hist.SetMarkerColor(col[ii])
      hist.SetLineWidth(2)
      hist.SetMarkerSize(0.5)

      for ipoint in range(hist.GetN()):
        _x_ = Double(0)
        _y_ = Double(0)
        hist.GetPoint(ipoint, _x_, _y_)
        if x_min > _x_:
          x_min = _x_
        if x_max < _x_:
          x_max = _x_
        if y_min > _y_:
          y_min = _y_
        if y_max < _y_:
          y_max = _y_
      

      if ii==0:
        hist.Draw("psame")
        legleg.AddEntry(hist, lname , "")
      else:
        hist.Draw("psame")


      leg.AddEntry(hist, label, "l")
 
#    print 'min, max, min, max = ', x_min, x_max, y_min, y_max
#    frame.GetXaxis().SetRangeUser(x_min*0.95, x_max*1.05)
#    frame.GetYaxis().SetRangeUser(y_min*0.95, y_max*1.05)


    leg.Draw()
    legleg.Draw()

    save(canvas, 'plots_roc/roc_' + header)


if __name__ == '__main__':


  runtype = {
    'dynamic95':{'type':'dynamic95'},
#    'dynamic90':{'type':'dynamic90'},
    'standard':{'type':'standard'},
    'run1':{'type':'run1'},
    }

  hdict = {
#    'Signal':{'file':'analysis_eff/Myroot_XXX.root','label':'Signal', 'sel':'tau_gendm>=0'},
    'Signal':{'file':'analysis_eff/Myroot_XXX.root','label':'Signal', 'sel':'1'},
    'Background':{'file':'analysis_fake/Myroot_XXX.root','label':'Background', 'sel':'1'},
    }
  
  ddict = {'1p0pi0':'tau_dm_rough==0', '1p1pi0':'tau_dm_rough==1', '3p':'tau_dm_rough==2', 'Inclusive':'tau_dm_rough!=-1'}

  for dkey, dm in ddict.iteritems():    

    roc = []
    for rkey, rval in sorted(runtype.iteritems()):

      hists = []
      for key, val in sorted(hdict.iteritems()):
      
        tfile = TFile(val['file'].replace('XXX', rkey))
        tree = tfile.Get('per_tau')

        histname = 'h_' + key + '_' + dkey + '_' + rkey
        hist = TH2F(histname, histname, 100,0,2,30, 0, 1)
      
        hist.SetTitle(val['label'])
        hist.Sumw2()

        den = Double(tree.GetEntries(''))
        num = Double(tree.GetEntries(dm))

        eff = num/den
        
        print dkey, rkey, key, 'efficiency = ', num, '/', den, ' = ', eff

        tree.Draw('(tau_photonsumpt_outside/tau_pt):(tau_ciso + tau_niso_weighted) >> ' + hist.GetName(), dm)

        hists.append([copy.deepcopy(hist), eff])


      roc.append([rocCurve(hists[1][0], hists[0][0], hists[1][1], hists[0][1]), rkey])
    
    overlay(roc, dkey)
