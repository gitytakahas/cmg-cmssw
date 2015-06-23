import os, numpy, math, copy, math
from ROOT import TLegend, TCanvas, TColor, kMagenta, kOrange, kRed, kBlue, kGray, kBlack, gROOT, gStyle, TFile, TH1F, TH2F, TLatex, TLine, TGraph, Double
from officialStyle import officialStyle

gROOT.SetBatch(True)
officialStyle(gStyle)
gStyle.SetOptTitle(0)
gStyle.SetOptStat(0)

gStyle.SetPadLeftMargin(0.2)
#gStyle.SetStripDecimals(False)
#gStyle.SetNoExponent(False)

col_ztt = TColor.GetColor(248,206,104)


def RV(val):
  return '{0:.3f}'.format(val)

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
    ensureDir('test/')
    canvas.SaveAs(name.replace(' ','').replace('&&','')+'.pdf')
    canvas.SaveAs(name.replace(' ','').replace('&&','')+'.gif')


def overlay(hists, hists2, vkey, header):

    canvas = TCanvas()
    leg = TLegend(0.25,0.75,0.5,0.9)
    LegendSettings(leg, 1)

    col = [1, 2, 4, 8, 6, col_ztt, 40, 50, 60]

    frame = TH2F('frame_' + header, 'frame_' + header, 1000,0.,1.,1000,0,1)
    frame.GetXaxis().SetTitle('Signal eff.')
    frame.GetYaxis().SetTitle('Background eff.')
    frame.GetYaxis().SetNdivisions(506)
    frame.GetYaxis().SetTitleOffset(1.8)
    frame.GetYaxis().SetNoExponent(False)
    frame.Draw()

    x_min = Double(1000.)
    y_min = Double(1000.)
    x_max = Double(-1000.)
    y_max = Double(-1000.)


    for ii, hist in enumerate(hists):

      hist.SetLineColor(col[ii])
      hist.SetMarkerColor(col[ii])
      hist.SetLineWidth(2)

      for ip in range(hist.GetN()):
        x = Double(-1)
        y = Double(-1)
        hist.GetPoint(ip, x, y)

        if x_min > x:
          x_min = x
        if x_max < x:
          x_max = x
        if y_min > y:
          y_min = y
        if y_max < y:
          y_max = y

      
      hist.SetMarkerStyle(20)
      hist.SetMarkerSize(0.5)
      hist.Draw('psame')

      leg.AddEntry(hist, hist.GetName(), 'lp')

    for ii, hist in enumerate(hists2):

      hist.SetMarkerColor(col[ii])
      hist.SetMarkerStyle(28)
      hist.Draw('psame')

    frame.GetXaxis().SetRangeUser(x_min*0.9, x_max*1.1)
    frame.GetYaxis().SetRangeUser(y_min*0.8, y_max*1.3)
    leg.Draw()

    leg2 = TLegend(0.7,0.8,0.9,0.9)
    LegendSettings(leg2, 1)
    leg2.AddEntry(hists[-1], header.replace('pi0',' + #pi^{0}'), '')
    leg2.Draw()

    save(canvas, 'test/scan_2D_' + header + '_gt50')


if __name__ == '__main__':


  basic = 'tau_pt > 50 && abs(tau_eta) < 2.3 && '

  var_weight = basic + '(tau_photonsumpt_outside/tau_pt) < ZZZ && (tau_ciso + tau_niso_weighted) < YYY'


  vardict = {
    'b':{'name':'weight_dynamic_k', 'var':var_weight, 'label':'Dynamic, nIso^{weight}, p_{T}^{strip}'},
    }


  ddict = {
    '1prong':{'cut':'tau_dm_rough==0'},
    '1prongpi0':{'cut':'tau_dm_rough==1'},
    }



  efile_dynamic = TFile('analysis_eff/Myroot_dynamic95.root')
  ffile_dynamic = TFile('analysis_fake/Myroot_dynamic95.root')
  
  etree_dynamic = efile_dynamic.Get('per_tau')
  ftree_dynamic = ffile_dynamic.Get('per_tau')

  eff_den_dynamic = Double(etree_dynamic.GetEntries(''))
  fake_den_dynamic = Double(ftree_dynamic.GetEntries(''))


  efile_run1 = TFile('analysis_eff/Myroot_run1.root')
  ffile_run1 = TFile('analysis_fake/Myroot_run1.root')
  
  etree_run1 = efile_run1.Get('per_tau')
  ftree_run1 = ffile_run1.Get('per_tau')

  eff_den_run1 = Double(etree_run1.GetEntries(''))
  fake_den_run1 = Double(ftree_run1.GetEntries(''))



  for dkey, dm in sorted(ddict.iteritems()):    

    grlist = []

    gr_dynamic = TGraph()
    gr_dynamic.SetName('Dynamic reco.')
    ip_dynamic = 0

    gr_special = []
    grs_dynamic = TGraph()

    for iiso in range(0,41):

      iso = iiso*0.1
        
      for ik in range(0,21):
        k = 0.05*ik
        str_num = dm['cut'] + ' && ' + var_weight.replace('YYY', str(iso)).replace('ZZZ', str(k))
        
        eff_num = Double(etree_dynamic.GetEntries(str_num))
        fake_num = Double(ftree_dynamic.GetEntries(str_num))
        eff = eff_num/eff_den_dynamic
        fake = fake_num/fake_den_dynamic
        
        print 'weight, dkey=', dkey,  'cut = ', str_num, eff, fake
        gr_dynamic.SetPoint(ip_dynamic, eff, fake)
        ip_dynamic += 1

        if k==0.1 and (iso==0.8 or iso==1.5 or iso==2.5):
          grs_dynamic.SetPoint(ip_dynamic, eff, fake)


    grlist.append(gr_dynamic)
    gr_special.append(grs_dynamic)

    gr_run1 = TGraph()
    grs_run1 = TGraph()
    gr_run1.SetName('Run-1 reco.')
    ip_run1 = 0

    for iiso in range(0,41):

      iso = iiso*0.1
        
      for ik in range(0,21):
        k = 0.05*ik
        str_num = dm['cut'] + ' && ' + var_weight.replace('YYY', str(iso)).replace('ZZZ', str(k))
        
        eff_num = Double(etree_run1.GetEntries(str_num))
        fake_num = Double(ftree_run1.GetEntries(str_num))
        eff = eff_num/eff_den_run1
        fake = fake_num/fake_den_run1
        
        print 'weight, dkey=', dkey,  'cut = ', str_num, eff, fake
        gr_run1.SetPoint(ip_run1, eff, fake)
        ip_run1 += 1
        
        if k==0.1 and (iso==0.8 or iso==1.5 or iso==2.5):
          grs_run1.SetPoint(ip_dynamic, eff, fake)

    grlist.append(gr_run1)
    gr_special.append(grs_run1)


    overlay(grlist, gr_special, 'weight', dkey)
