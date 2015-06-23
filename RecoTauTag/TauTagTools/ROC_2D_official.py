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

def RV(val):
  return '{0:.3f}'.format(val)

def rocCurve(hS, hB, efS, efB, title):
  ''' Create a ROC TGraph from two input histograms.'''

  maxBin = hS.GetNbinsX()

  if hS.Integral() == 0.:
    print 'ROC curve creator, hist', hS.GetName(), 'has zero entries'
    return

  effsS = [efS*hS.Integral(0, nBin)/hS.Integral(0, maxBin+1) for nBin in range(0, maxBin + 1) if hS.Integral(0, nBin)!=0]
  rejB = [efB*hB.Integral(0, nBin)/hB.Integral(0, maxBin+1) for nBin in range(0, maxBin + 1) if hB.Integral(0, nBin)!=0]
  rocCurve = TGraph(maxBin, numpy.asarray(effsS), numpy.asarray(rejB))

  rocCurve.SetName(title)

  ### 
  print title.replace('_',' & '), ' & no cut & ', RV(efS), '(', RV(1.), ')', '&', RV(efB), '(', RV(1.), ') &', RV(1.), ' \\\\'

  previous_eff = efS
  previous_bkg = efB

  eff20 = -1.
  bkg20 = -1.

  for ieff in [0.25, 0.2, 0.15]:
#    _eff_ = 0.
#    _bkg_ = 0.
  
    flag = False
    
    for ibin in range(0, maxBin+1):
      if hS.GetBinCenter(ibin) > ieff and flag == False:
        _eff_ = efS*hS.Integral(0, ibin)/hS.Integral(0, maxBin+1)
        _bkg_ = efB*hB.Integral(0, ibin)/hB.Integral(0, maxBin+1)
        flag = True

        ratio = 1.
        if (1-_eff_/previous_eff)==0:
          print '!!!!!!', _eff_, previous_eff
        else:
          ratio = Double((1-(_bkg_/previous_bkg))/(1-(_eff_/previous_eff)))
        
        print title.replace('_',' & '), ' & ', ieff, ' & ', RV(_eff_), '(', RV(_eff_/previous_eff), ')', '&', RV(_bkg_), '(', RV(_bkg_/previous_bkg), ') &', RV(ratio), ' \\\\'

        previous_eff = _eff_
        previous_bkg = _bkg_

        if ieff==0.2:
          eff20 = _eff_
          bkg20 = _bkg_
      
  roc20 = TGraph(1, numpy.asarray([eff20]), numpy.asarray([bkg20]))

  return rocCurve, roc20

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
    ensureDir('plots_roc_2D')
    canvas.SaveAs(name.replace(' ','').replace('&&','')+'.pdf')
    canvas.SaveAs(name.replace(' ','').replace('&&','')+'.gif')


def makeCompareVars(hists, xtitle, ytitle, scale ,savestr, ncolumn, addon = ''):
   
  c = TCanvas()
  c.SetLogy()
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


    if scale and hist.GetSumOfWeights()!=0:
      hist.Scale(1./abs(hist.GetSumOfWeights()))
      hist.SetMaximum(hist.GetMaximum()*1.2)
#      hist.SetMinimum(0)

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

    save(c, 'plots_roc_2D/' + savestr)


def overlay(hists, header):

    canvas = TCanvas()
    leg = TLegend(0.2,0.93,0.85,1.0)
    lname = header.replace('pi0','#pi^{0}')
#    LegendSettings(leg,len(hists))

    ndiv = len(hists)/3
#    print '# of division = ', ndiv
    LegendSettings(leg, ndiv)

    legleg = TLegend(0.2,0.85,0.4,0.92)
    LegendSettings(legleg, 1)


    col = [1, 2, 4, 8, 6, 30, 40, 50, 60]

    frame = TH2F('frame_' + header, 'frame_' + header, 10,0.,1.,10,0,0.1)
#    frame = TH2F('frame_' + header, 'frame_' + header, 10,0.,0.45,10,0,0.075)
    frame.GetXaxis().SetTitle('Signal eff.')
    frame.GetYaxis().SetTitle('Background eff.')
    frame.GetYaxis().SetNdivisions(506)
    frame.Draw()

    x_min = Double(1000.)
    y_min = Double(1000.)
    x_max = Double(-1000.)
    y_max = Double(-1000.)


    for ii, pack in enumerate(hists):
      hist_, label = pack
      hist = hist_[0]
      wp = hist_[1]

#      hist, label = pack

      lcolor = 6
      if hist.GetName().find('dynamic95')!=-1:
        lcolor = 2
      if hist.GetName().find('standard')!=-1:
        lcolor = 4

#      hist.SetLineColor(col[ii])
#      hist.SetMarkerColor(col[ii])
      hist.SetLineColor(lcolor)
      hist.SetMarkerColor(lcolor)

      hist.SetLineWidth(1)
      hist.SetLineStyle(1)
      hist.SetMarkerSize(1)

      mstyle = 24
      if hist.GetName().find('loose')!=-1:
        mstyle = 25
      if hist.GetName().find('tight')!=-1:
        mstyle = 32

      hist.SetMarkerStyle(mstyle)

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
        hist.Draw("lepsame")
        legleg.AddEntry(hist, lname , "")
      else:
        hist.Draw("lepsame")


      if label.find('Dynamic')!=-1:
        wp.SetMarkerColor(1)
        wp.SetMarkerSize(2)
        wp.SetMarkerStyle(28)
        wp.Draw("psame")





#      print 'check hist name ! ', hist.GetName(), hist.GetTitle(), label
      if hist.GetName().find('loose')!=-1:
#        _label_ = label.split('_')[0]
        leg.AddEntry(hist, label, "l")
 
#    print 'min, max, min, max = ', x_min, x_max, y_min, y_max
    frame.GetXaxis().SetRangeUser(x_min*0.8, x_max*1.2)
    frame.GetYaxis().SetRangeUser(y_min*0.95, y_max*1.05)

    mleg = TLegend(0.2,0.65,0.4,0.85)
    LegendSettings(mleg,1)
    
    g = [0,0,0]
    
    for index, i in enumerate(['loose','medium','tight']):
      g[index] = TGraph()
      g[index].SetPoint(0, 1,1)
      g[index].SetMarkerSize(2)

      ll = ' ' + i

      if i=='loose':
        g[index].SetMarkerStyle(25)
        ll += ' (Iso < 2GeV)'
      if i=='tight':
        g[index].SetMarkerStyle(32)
        ll += ' (Iso < 0.8GeV)'
      if i=='medium':
        g[index].SetMarkerStyle(24)
        ll += ' (Iso < 1GeV)'

      mleg.AddEntry(g[index], ll, 'lp')
    
    mleg.Draw()

    leg.Draw()
    legleg.Draw()

    leg2 = TLegend(0.8,0.93,0.9,0.99)
    LegendSettings(leg2, 1)
    leg2.AddEntry(hist, 'VBF / QCD', "")
    leg2.Draw()

    save(canvas, 'plots_roc_2D/roc_' + header)


if __name__ == '__main__':


  runtype = {
    'dynamic95':{'type':'Dynamic'},
#    'dynamic90':{'type':'dynamic90'},
    'standard':{'type':'Standard (run-1)'},
#    'run1':{'type':'run1'},
    }

  hdict = {
    'Signal':{'file':'analysis_eff/Myroot_XXX.root','label':'Signal', 'sel':'1'},
    'Background':{'file':'analysis_fake/Myroot_XXX.root','label':'Background', 'sel':'1'},
    }
  
  ddict = {'1p0pi0':'tau_dm_rough==0', 
           '1p1pi0':'tau_dm_rough==1', 
           '3p':'tau_dm_rough==2', 
           'Inclusive':'tau_dm_rough!=-1'}

  isodict = {'loose':2.,
             'medium':1.,
             'tight':0.8,
             }

  isodict_vary = {'1p0pi0':'1.8',
                  '1p1pi0':'1.5',
                  '3p':'2'}



  for dkey, dm in ddict.iteritems():    

    roc = []
    for rkey, rval in sorted(runtype.iteritems()):

      for ikey, ival in sorted(isodict.iteritems()):

        hists = []
        for key, val in sorted(hdict.iteritems()):
      
          tfile = TFile(val['file'].replace('XXX', rkey))
          tree = tfile.Get('per_tau')

          histname = 'h_' + key + '_' + dkey + '_' + rkey + '_' + ikey
          hist = TH1F(histname, histname, 100, 0, 1)
      
          hist.SetTitle(val['label'])
          hist.Sumw2()

          den = Double(tree.GetEntries(''))
          num = Double(tree.GetEntries(dm + ' && (tau_ciso + tau_niso_weighted) < ' + str(ival)))
          eff = num/den
          
          tree.Draw('tau_photonsumpt_outside/tau_pt >> ' + hist.GetName(), dm + ' && (tau_ciso + tau_niso_weighted) < ' + str(ival))

          hists.append([copy.deepcopy(hist), eff])


        makeCompareVars(hists, '#sum p_{T}^{#gamma, outside} / tau pT', 'events', True , 'compare_' + dkey + '_' + rkey + '_' + ikey, len(hists), dkey + '_' + rkey + '_' + ikey) 
        roc.append([rocCurve(hists[1][0], hists[0][0], hists[1][1], hists[0][1], rkey + '_' + ikey + '_' + dkey), rval['type']])

    overlay(roc, dkey)
