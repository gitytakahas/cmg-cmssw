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

def returnFileName(runtype, vkey):
    rfile = '../analysis_' + runtype + '/Myroot_dynamic95.root'

    if vkey.find('run1')!=-1:
#        rfile = '../analysis_' + runtype + '/Myroot_standard.root'                    
        rfile = '../analysis_' + runtype + '/Myroot_run1.root'                    
    
    return rfile

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
    ensureDir('plots_roc_2D/')
    canvas.SaveAs(name.replace(' ','').replace('&&','')+'.pdf')
    canvas.SaveAs(name.replace(' ','').replace('&&','')+'.gif')


def overlay(hists, header):

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
      hist.Draw('plsame')

      leg.AddEntry(hist, hist.GetName(), 'lp')

    frame.GetXaxis().SetRangeUser(x_min*0.9, x_max*1.1)
    frame.GetYaxis().SetRangeUser(y_min*0.8, y_max*1.3)
    leg.Draw()

    leg2 = TLegend(0.7,0.8,0.9,0.9)
    LegendSettings(leg2, 1)
    leg2.AddEntry(hists[-1], header.replace('pi0',' + #pi^{0}'), '')
    leg2.Draw()


    save(canvas, 'plots_roc_2D/performance_' + header)


if __name__ == '__main__':


  basic = 'tau_pt > 20 && abs(tau_eta) < 2.3 && '
#  basic = '1 && '

  var_dbeta = basic + '(tau_ciso + max(0, (tau_niso-0.458*tau_puiso))) < YYY'
  var_dbeta_ptouter = basic + '(tau_ciso + max(0, (tau_niso-0.458*tau_puiso))) < YYY && (tau_photonsumpt_outside/tau_pt) < 0.1'
  var_weight = basic + '(tau_ciso + tau_niso_weighted) < YYY'
  var_weight_ptouter_k = basic + '(tau_photonsumpt_outside/tau_pt) < 0.1 && ((tau_dm_rough!=2 && (tau_ciso + tau_niso_weighted) < YYY) || (tau_dm_rough==2 && (tau_ciso + max(0, (tau_niso_weighted-0.22*tau_pt+2))) < YYY))'


  vardict = {
    'a':{'name':'dbeta_run1', 'tree':'per_tau','var':var_dbeta, 'label':'run1, #Delta#beta'},
    'b':{'name':'dbeta_run1_ptouter', 'tree':'per_tau','var':var_dbeta_ptouter, 'label':'run1, #Delta#beta, p_{T}^{strip}'},
#    'c':{'name':'weight_run1', 'tree':'per_tau','var':var_weight, 'label':'run1, nIso^{weight}'},
#    'd':{'name':'dbeta_dynamic', 'tree':'per_tau','var':var_dbeta, 'label':'Dynamic, #Delta#beta'},
    'e':{'name':'dbeta_dynamic_ptouter', 'tree':'per_tau','var':var_dbeta_ptouter, 'label':'Dynamic #Delta#beta, p_{T}^{strip}'},
    'f':{'name':'dbeta_dynamic_ptouter_0.2', 'tree':'per_tau','var':var_dbeta_ptouter.replace('0.458','0.2'), 'label':'Dynamic #Delta#beta = 0.2, p_{T}^{strip}'},
#    'g':{'name':'weight_dynamic', 'tree':'per_tau','var':var_weight, 'label':'Dynamic, nIso^{weight}'},
    'h':{'name':'weight_dynamic_ptouter_k', 'tree':'per_tau','var':var_weight_ptouter_k, 'label':'Dynamic, nIso^{weight}, p_{T}^{strip}'},
    }


  ddict = {
    '1prong':{'cut':'tau_gendm_rough==0'},
    '1prongpi0':{'cut':'tau_gendm_rough==1'},
    '3prong':{'cut':'tau_gendm_rough==2'},
    'Inclusive':{'cut':'tau_gendm_rough!=-1'}
    }

#  isodict = {'loose':'2.',
#             'medium':'1.',
#             'tight':'0.8'
#             }

  isodict = {'loose':'2.5',
             'medium':'1.5',
             'tight':'0.8'
             }


  for dkey, dm in sorted(ddict.iteritems()):    

    hists = []

    for vkey, var in sorted(vardict.iteritems()):

      wpdict = {'loose':{'eff':-1, 'fake':-1},
                'medium':{'eff':-1, 'fake':-1},
                'tight':{'eff':-1, 'fake':-1}}

      for key in ['eff', 'fake']:

        tfile = TFile(returnFileName(key, var['name']))
        tree = tfile.Get(var['tree'])
                  
        for ikey, ival in sorted(isodict.iteritems()):

          if key=='eff':
            den = Double(tree.GetEntries(dm['cut']))
            str_num = dm['cut'] + ' && tau_pt > 20 && abs(tau_eta) < 2.3 &&' + var['var'].replace('YYY', ival)
          else:
            den = Double(tree.GetEntries(''))
            str_num = dm['cut'].replace('gendm','dm') + ' && tau_pt > 20 && abs(tau_eta) < 2.3 &&' + var['var'].replace('YYY', ival)


          num = Double(tree.GetEntries(str_num))
          eff = num/den
          
          wpdict[ikey][key] = eff

      gr = TGraph()
      gr.SetName(var['label'])
      idx = 0
      for wp, wpval in sorted(wpdict.iteritems()):
        gr.SetPoint(idx, wpdict[wp]['eff'], wpdict[wp]['fake'])
        idx += 1

      hists.append(gr)

    overlay(hists, dkey)
