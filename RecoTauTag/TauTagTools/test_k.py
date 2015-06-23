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
    leg = TLegend(0.25,0.6,0.5,0.9)
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
      hist.Draw('lsame')

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

    leg3 = TLegend(0.7,0.7,0.9,0.8)
    LegendSettings(leg3, 1)

    if vkey.find('dbeta')!=-1:
      leg3.AddEntry(hists[-1], '#Delta#beta', '')
    else:
      leg3.AddEntry(hists[-1], 'k-param.', '')

    leg3.Draw()


    if vkey.find('dbeta')!=-1:
      save(canvas, 'test/scan_dbeta_' + header)
    else:
      save(canvas, 'test/scan_k_' + header)


if __name__ == '__main__':


  basic = 'tau_pt > 20 && abs(tau_eta) < 2.3 && '

  var_dbeta = basic + '(tau_ciso + max(0, (tau_niso-ZZZ*tau_puiso))) < YYY && (tau_photonsumpt_outside/tau_pt) < 0.1'
  var_weight = basic + '(tau_photonsumpt_outside/tau_pt) < 0.1 && (tau_ciso + max(0, tau_niso_weighted-ZZZ)) < YYY'


  vardict = {
    'a':{'name':'dbeta_dynamic', 'var':var_dbeta, 'label':'Dynamic #Delta#beta, p_{T}^{strip}'},
    'b':{'name':'weight_dynamic_k', 'var':var_weight, 'label':'Dynamic, nIso^{weight}, p_{T}^{strip}'},
    }


  ddict = {
    '1prong':{'cut':'tau_dm_rough==0'},
    '1prongpi0':{'cut':'tau_dm_rough==1'},
    '3prong':{'cut':'tau_dm_rough==2'},
    }

  isodict = {'loose':'2.',
             'medium':'1.',
             'tight':'0.8'
             }


  efile = TFile('analysis_eff/Myroot_dynamic95.root')
  ffile = TFile('analysis_fake/Myroot_dynamic95.root')
  
  etree = efile.Get('per_tau')
  ftree = ffile.Get('per_tau')


  for dkey, dm in sorted(ddict.iteritems()):    
    for vkey, var in sorted(vardict.iteritems()):                  

      grlist = []
      grspecial = []
      
      for ikey, ival in sorted(isodict.iteritems()):

        eff_den = Double(etree.GetEntries(''))
        fake_den = Double(ftree.GetEntries(''))

        gr = TGraph()
        gr.SetName(ikey)
        
        grs = TGraph()

        if var['name'].find('dbeta')!=-1:
          for ik in range(0,51):
            db = 0.02*ik
            str_num = dm['cut'] + ' && ' + var['var'].replace('YYY', ival).replace('ZZZ', str(db))

            eff_num = Double(etree.GetEntries(str_num))
            fake_num = Double(ftree.GetEntries(str_num))
            eff = eff_num/eff_den
            fake = fake_num/fake_den

            print 'dbeta, dkey=', dkey, 'vkey=', ikey, 'cut = ', str_num, eff, fake
            gr.SetPoint(ik, eff, fake)

            if ik%10==0.:
              grs.SetPoint(ik, eff, fake)

        if var['name'].find('weight')!=-1:
          for ik in range(0,51):
            k = 0.2*ik
            str_num = dm['cut'] + ' && ' + var['var'].replace('YYY', ival).replace('ZZZ', str(k))

            eff_num = Double(etree.GetEntries(str_num))
            fake_num = Double(ftree.GetEntries(str_num))
            eff = eff_num/eff_den
            fake = fake_num/fake_den

            print 'weight, dkey=', dkey, 'vkey=', ikey, 'cut = ', str_num, eff, fake
            gr.SetPoint(ik, eff, fake)

            if ik%10==0.:
              grs.SetPoint(ik, eff, fake)
        
        grlist.append(gr)
        grspecial.append(grs)

      overlay(grlist, grspecial, var['name'], dkey)
