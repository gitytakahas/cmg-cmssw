import os, numpy, math, copy, math, sys
from array import array
from ROOT import TLegend, TCanvas, TColor, kMagenta, kOrange, kRed, kBlue, kGray, kBlack, gROOT, gStyle, TFile, TH1F, TH2F, TLatex, TLine, TGraphAsymmErrors, Double
from officialStyle import officialStyle

gROOT.SetBatch(True)
officialStyle(gStyle)
gStyle.SetOptTitle(0)
gStyle.SetOptStat(0)
#gStyle.SetPadRightMargin (0.3)

gStyle.SetPadLeftMargin  (0.2)

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
    ensureDir('plots_isolation_roc')
    canvas.SaveAs(name.replace(' ','').replace('&&','')+'.pdf')
    canvas.SaveAs(name.replace(' ','').replace('&&','')+'.gif')


def returnFileName(runtype, vkey):
    rfile = '../analysis_' + runtype + '/Myroot_dynamic95.root'

    if vkey.find('run1')!=-1:
#        rfile = '../analysis_' + runtype + '/Myroot_standard.root'                    
        rfile = '../analysis_' + runtype + '/Myroot_run1.root'                    
    
    return rfile


def makeEffPlotsVars(tree, varx, vary, sel, nbinx, xmin, xmax, nbiny, ymin, ymax, xtitle, ytitle, leglabel = None, header='', addon='', option='pt', marker=20):
   
#    binning = [20,30,40,50,60,70,80,90,100,120,150,200,300]
    binning = [20,40,60,80,100,150,300]
    vbinning = [0,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,30]

    if option=='pt':
#        _hist_ = TH2F('h_effp_' + addon, 'h_effp' + addon, len(binning)-1, array('d',binning), nbiny, ymin, ymax)
        _hist_ = TH1F('h_effp_' + addon, 'h_effp' + addon, len(binning)-1, array('d',binning))
        _ahist_ = TH1F('ah_effp_' + addon, 'ah_effp' + addon, len(binning)-1, array('d',binning))
    elif option=='eta':
#        _hist_ = TH2F('h_effp_' + addon, 'h_effp' + addon, nbinx, xmin, xmax, nbiny, ymin, ymax)
        _hist_ = TH1F('h_effp_' + addon, 'h_effp' + addon, nbinx, xmin, xmax)
        _ahist_ = TH1F('ah_effp_' + addon, 'ah_effp' + addon, nbinx, xmin, xmax)
    elif option=='nvtx':
#        _hist_ = TH2F('h_effp_' + addon, 'h_effp' + addon, len(vbinning)-1, array('d',vbinning), nbiny, ymin, ymax)
        _hist_ = TH1F('h_effp_' + addon, 'h_effp' + addon, len(vbinning)-1, array('d',vbinning))
        _ahist_ = TH1F('ah_effp_' + addon, 'ah_effp' + addon, len(vbinning)-1, array('d',vbinning))


#    dname = vary + ':' + varx + ' >> ' + _hist_.GetName()
#    tree.Draw(varx, sel)

    tree.Draw(varx + ' >> ' + _hist_.GetName(), sel)
    tree.Draw(varx + ' >> ' + _ahist_.GetName(), sel + ' && ' + vary)
    
    g_efficiency = TGraphAsymmErrors()
    g_efficiency.BayesDivide(_ahist_, _hist_)
    g_efficiency.GetXaxis().SetTitle(xtitle)
    g_efficiency.GetYaxis().SetTitle(ytitle)
    g_efficiency.GetYaxis().SetNdivisions(507)
    g_efficiency.SetLineWidth(3)
    g_efficiency.SetName(header)    
    g_efficiency.SetMinimum(0.)
    g_efficiency.GetYaxis().SetTitleOffset(1.65)
    g_efficiency.SetMarkerStyle(marker)
    g_efficiency.SetMarkerSize(2)

    return copy.deepcopy(g_efficiency)



def makeEffPlotsVars2(tree, varx, vary, sel, nbinx, xmin, xmax, nbiny, ymin, ymax, xtitle, ytitle, leglabel = None, header='', addon='', option='pt', marker=20):
   
#    binning = [20,30,40,50,60,70,80,90,100,120,150,200,300]
    binning = [20,40,60,80,100,150,300]
    vbinning = [0,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,30]

    if option=='pt':
        _hist_ = TH2F('h_effp_' + addon, 'h_effp' + addon, len(binning)-1, array('d',binning), nbiny, ymin, ymax)
    elif option=='eta':
        _hist_ = TH2F('h_effp_' + addon, 'h_effp' + addon, nbinx, xmin, xmax, nbiny, ymin, ymax)
    elif option=='nvtx':
        _hist_ = TH2F('h_effp_' + addon, 'h_effp' + addon, len(vbinning)-1, array('d',vbinning), nbiny, ymin, ymax)

    dname = vary + ':' + varx + ' >> ' + _hist_.GetName()
    tree.Draw(dname, sel)

    hist = _hist_.ProfileX()
    hist.GetXaxis().SetTitle(xtitle)
    hist.GetYaxis().SetTitle(ytitle)
    hist.GetYaxis().SetNdivisions(507)
    hist.SetLineWidth(3)
    hist.SetName(header)    
    hist.SetMinimum(0.)
    hist.GetYaxis().SetTitleOffset(1.65)
    hist.SetMarkerStyle(marker)
    hist.SetMarkerSize(2)

    return copy.deepcopy(hist)
    



def overlay(hists, header, addon):

#    canvas = TCanvas('c','c',900,500)
    canvas = TCanvas()
    leg = TLegend(0.25,0.7,0.5,0.9)
#    LegendSettings(leg,len(hists))
    LegendSettings(leg, 1)

    col = [1,2,4,6,8,9,12]

    ymax = -1
    ymin = 100

    for ii, hist in enumerate(hists):
        hist.SetLineColor(col[ii])
        hist.SetMarkerColor(col[ii])
        hist.SetLineWidth(2)
        hist.SetMarkerSize(1)


        for ip in range(hist.GetN()):
            x = Double(-1)
            y = Double(-1)
            hist.GetPoint(ip, x, y)

            if ymin > y:
                ymin = y
            if ymax < y:
                ymax = y

#
#        if ymax < hist.GetMaximum():
#            ymax = hist.GetMaximum()
#        if ymin > hist.GetMinimum():
#            ymin = hist.GetMinimum()

        if ii==0:
            hist.Draw("Azp")
        else:
            
            hist.Draw("pzsame")
 
        leg.AddEntry(hist, hist.GetName(), 'lep')


    for hist in hists:
        hist.SetMaximum(ymax*2)
#        hist.SetMinimum(ymin*0.5)

    leg.Draw()

    tex = TLatex( hists[-1].GetXaxis().GetXmin() + 0.7*(hists[-1].GetXaxis().GetXmax() - hists[-1].GetXaxis().GetXmin()), ymax*1.8, addon)

    tex.SetTextFont(42)
    tex.SetTextSize(0.04)
    tex.Draw()

    tex2 = TLatex( hists[-1].GetXaxis().GetXmin() + 0.7*(hists[-1].GetXaxis().GetXmax() - hists[-1].GetXaxis().GetXmin()), ymax*1.7, 'Loose')

    tex2.SetTextFont(42)
    tex2.SetTextSize(0.03)
    tex2.Draw()

    
    save(canvas, 'plots_isolation_roc/' + header)

    

if __name__ == '__main__':


#    basic_sel = 'tau_pt > 20 && abs(tau_eta) < 2.3'
    basic_sel = '1'

    basic = 'tau_pt > 20 && abs(tau_eta) < 2.3 && '
#    basic = '1 && '

    var_dbeta = basic + '(tau_ciso + max(0, (tau_niso-0.468*tau_puiso))) < 2.5'
    var_dbeta_run1 = basic + '(tau_ciso + max(0, (tau_niso-0.468*tau_puiso))) < 2.5'

    var_dbeta_ptouter = basic + '(tau_ciso + max(0, (tau_niso-0.468*tau_puiso))) < 2.5 && (tau_photonsumpt_outside/tau_pt) < 0.1'
    var_ciso = basic + 'tau_ciso < 2.5'
    var_nw = basic + 'tau_niso_weighted < 2.5'
    var_cmb = basic + '(tau_ciso + tau_niso_weighted) < 2.5'
    var_cmb_ptouter = basic + '((tau_ciso + tau_niso_weighted) < 2.5 && (tau_photonsumpt_outside/tau_pt) < 0.1)'
    var_cmb_ptouter_k = basic + '((tau_ciso + max(0, (tau_niso_weighted-0.22*tau_pt+2))) < 2.5 && (tau_photonsumpt_outside/tau_pt) < 0.1)'
    var_inc_ptouter_k = basic + '((tau_dm_rough!=2 && (tau_ciso + tau_niso_weighted) < 2.5 && (tau_photonsumpt_outside/tau_pt) < 0.1) || (tau_dm_rough==2 && (tau_ciso + max(0, (tau_niso_weighted-0.22*tau_pt+2))) < 2.5 && (tau_photonsumpt_outside/tau_pt) < 0.1))'

    hdict1 = {
        'cIso_run1':{'tree':'per_tau','var':var_ciso, 'nbin':2, 'xmin':-0.5, 'xmax':1.5, 'sel':basic_sel, 'name':'run1_ciso','label':'run1, cIso'},
        'cIso_dynamic':{'tree':'per_tau','var':var_ciso, 'nbin':2, 'xmin':-0.5, 'xmax':1.5, 'sel':basic_sel, 'name':'dynamic_ciso','label':'dynamic, cIso'},
        }

    hdict2 = {
        'nIso_weight_run1':{'tree':'per_tau','var':var_nw, 'nbin':2, 'xmin':-0.5, 'xmax':1.5, 'sel':basic_sel, 'name':'run1_nw','label':'run1, nIso^{weight}'},
        'nIso_weight_dynamic':{'tree':'per_tau','var':var_nw, 'nbin':2, 'xmin':-0.5, 'xmax':1.5, 'sel':basic_sel, 'name':'dynamic_nw','label':'dynamic, nIso^{weight}'},
        }

    hdict3 = {
        'cmb_run1':{'tree':'per_tau','var':var_cmb, 'nbin':2, 'xmin':-0.5, 'xmax':1.5, 'sel':basic_sel, 'name':'run1_cmb','label':'run1, cmb'},
        'cmb_run1_pt':{'tree':'per_tau','var':var_cmb_ptouter, 'nbin':2, 'xmin':-0.5, 'xmax':1.5, 'sel':basic_sel, 'name':'run1_cmb_ptouter','label':'run1, cmb, p_{T}^{outer}'},
        'cmb_dynamic':{'tree':'per_tau','var':var_cmb, 'nbin':2, 'xmin':-0.5, 'xmax':1.5, 'sel':basic_sel, 'name':'dynamic_cmb','label':'dynamic, cmb'},
        'cmb_dynamic_pt':{'tree':'per_tau','var':var_cmb_ptouter, 'nbin':2, 'xmin':-0.5, 'xmax':1.5, 'sel':basic_sel, 'name':'dynamic_cmb_ptouter','label':'dynamic, cmb, p_{T}^{outer}'},
        }
 
    hdict4 = {
        'dbeta_a_run1':{'tree':'per_tau','var':var_dbeta, 'nbin':2, 'xmin':-0.5, 'xmax':1.5, 'sel':basic_sel, 'name':'run1_dbeta','label':'run1, #Delta#beta', 'marker':20},
        'dbeta_b_dynamic':{'tree':'per_tau','var':var_dbeta, 'nbin':2, 'xmin':-0.5, 'xmax':1.5, 'sel':basic_sel, 'name':'dynamic_dbeta','label':'Dynamic, #Delta#beta', 'marker':34},
        'dbeta_c_dynamic_ptouter':{'tree':'per_tau','var':var_dbeta_ptouter, 'nbin':2, 'xmin':-0.5, 'xmax':1.5, 'sel':basic_sel, 'name':'dynamic_dbeta_ptouter','label':'Dynamic, #Delta#beta, p_{T}^{strip}', 'marker':21},
#        'wdbeta_dynamic':{'tree':'per_tau','var':var_cmb, 'nbin':2, 'xmin':-0.5, 'xmax':1.5, 'sel':basic_sel, 'name':'wdynamic_dbeta','label':'D, nIso^{w}'},
#        'wdbeta_dynamic_ptouter':{'tree':'per_tau','var':var_cmb_ptouter, 'nbin':2, 'xmin':-0.5, 'xmax':1.5, 'sel':basic_sel, 'name':'wdynamic_dbeta_ptouter','label':'D, nIso^{w}, p_{T}^{strip}'},
        'wdbeta_dynamic_ptouter_k':{'tree':'per_tau','var':var_inc_ptouter_k, 'nbin':2, 'xmin':-0.5, 'xmax':1.5, 'sel':basic_sel, 'name':'wdynamic_dbeta_ptouter_k','label':'Dynamic, nIso^{weight}, p_{T}^{strip}', 'marker':23},
        }


#    ddict = {
#        'a':{'cut':'tau_dm_rough==0', 'label':'1prong', 'name':'1prong'},
#        'b':{'cut':'tau_dm_rough==1', 'label':'1prong + #pi^{0}', 'name':'1prongpi0'},
#        'c':{'cut':'tau_dm_rough==2', 'label':'3prong', 'name':'3prong'},
#        'd':{'cut':'tau_dm_rough!=-1', 'label':'Inclusive', 'name':'Inclusive'},
#        }

    ddict = {
        'a':{'cut':'tau_gendm_rough==0', 'label':'1prong', 'name':'1prong'},
        'b':{'cut':'tau_gendm_rough==1', 'label':'1prong + #pi^{0}', 'name':'1prongpi0'},
        'c':{'cut':'tau_gendm_rough==2', 'label':'3prong', 'name':'3prong'},
        'd':{'cut':'tau_gendm_rough!=-1', 'label':'Inclusive', 'name':'Inclusive'},
#        'd':{'cut':'tau_dm!=-1', 'label':'Inclusive', 'name':'Inclusive'},
        }
    
    hdicts = {
#        'cIso':hdict1, 
#        'nIso':hdict2, 
#        'cmb':hdict3, 
        'dbeta':hdict4
        }

    for runtype in ['eff', 'fake']:
#    for runtype in ['eff']:

        title = 'Signal efficiency'
        if runtype=='fake':
            title = 'Fake rate'  

        for dkey, dm in ddict.iteritems():

            for hname, hdict in hdicts.iteritems():

                hists = []
        
                for vkey, ivar in sorted(hdict.iteritems()):
            
                    tfile = TFile(returnFileName(runtype, vkey))
                    tree = tfile.Get('per_tau')

                    xval = 'tau_genpt'
                    xlabel = 'gen tau p_{T}^{vis} (GeV)'
                    
                    if runtype=='fake':
                        xval = 'tau_corjetpt'
                        xlabel = 'corrected jet p_{T} (GeV)'

                    if runtype=='fake':

                        hists.append(makeEffPlotsVars(tree, xval, ivar['var'] + ' && ' + dm['cut'].replace('gendm','dm'), ivar['sel'], 30, 0, 300, ivar['nbin'], ivar['xmin'], ivar['xmax'], xlabel, title, dkey, ivar['label'], vkey + '_' + dkey, 'pt', ivar['marker']))
                    else:
                        hists.append(makeEffPlotsVars(tree, xval, ivar['var'] + ' && ' + dm['cut'] + ' && ' + dm['cut'].replace('gendm','dm'), ivar['sel'] + ' && ' + dm['cut'], 30, 0, 300, ivar['nbin'], ivar['xmin'], ivar['xmax'], xlabel, title, dkey, ivar['label'], vkey + '_' + dkey, 'pt', ivar['marker']))


                overlay(hists, runtype + '_taupt_' + hname + '_' + dm['name'], dm['label'])


#                continue
                hists = []

                for vkey, ivar in sorted(hdict.iteritems()):
                    
                    tfile = TFile(returnFileName(runtype, vkey))
                    tree = tfile.Get('per_tau')
                                       
                    xval = 'tau_geneta'
                    xlabel = 'gen tau #eta^{vis}'
                    
                    if runtype=='fake':
                        xval = 'tau_corjeteta'
                        xlabel = 'corrected jet #eta'

                    if runtype=='fake':
                        hists.append(makeEffPlotsVars(tree, xval, ivar['var'] + ' && ' + dm['cut'].replace('gendm','dm'), ivar['sel'] , 10, -2.5, 2.5, ivar['nbin'], ivar['xmin'], ivar['xmax'], xlabel, title, dkey, ivar['label'], 'taueta_' + vkey + '_' + dkey, 'eta', ivar['marker']))
                    else:
                        hists.append(makeEffPlotsVars(tree, xval, ivar['var'] + ' && ' + dm['cut'] + ' && ' + dm['cut'].replace('gendm','dm'), ivar['sel'] + ' && ' + dm['cut'] , 10, -2.5, 2.5, ivar['nbin'], ivar['xmin'], ivar['xmax'], xlabel, title, dkey, ivar['label'], 'taueta_' + vkey + '_' + dkey, 'eta', ivar['marker']))

                        

            
                overlay(hists, runtype + '_taueta_' + hname + '_' + dm['name'], dm['label'])

#                hists = []
#                
#                for vkey, ivar in sorted(hdict.iteritems()):
#            
#                    tfile = TFile(returnFileName(runtype, vkey))
#                    tree = tfile.Get('per_tau')
#            
#                    if vkey=='wdbeta_dynamic_ptouter_k' and (dkey!='d' and dkey!='c'): continue
#

#                    hists.append(makeEffPlotsVars(tree, 'tau_gvertex', ivar['var'], ivar['sel'] + ' && ' + dm['cut'], 30, 0, 30, ivar['nbin'], ivar['xmin'], ivar['xmax'], '# of good vertices', title, dkey, ivar['label'], 'tau_nvtx_' + vkey + '_' + dkey, 'nvtx', ivar['marker']))
#
#                
#                overlay(hists, runtype + '_nvtx_' + hname + '_' + dm['name'], dm['label'])
