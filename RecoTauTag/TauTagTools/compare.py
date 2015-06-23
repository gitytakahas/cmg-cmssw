import os, numpy, math, copy, math
from array import array
from ROOT import TLegend, TCanvas, TColor, kMagenta, kOrange, kRed, kBlue, kGray, kBlack, gROOT, gStyle, TFile, TH1F, TH2F, TLatex, TLine
from officialStyle import officialStyle

gROOT.SetBatch(True)
officialStyle(gStyle)
gStyle.SetOptTitle(0)
gStyle.SetOptStat(0)
gStyle.SetPadLeftMargin(0.19)

col_qcd = TColor.GetColor(250,202,255)
col_tt  = TColor.GetColor(155,152,204)
col_ewk = TColor.GetColor(222,90,106)
col_zll = TColor.GetColor(100,182,232)
col_ztt = TColor.GetColor(248,206,104)

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
    ensureDir('plots')
    canvas.SaveAs(name.replace(' ','').replace('&&','')+'.pdf')
    canvas.SaveAs(name.replace(' ','').replace('&&','')+'.gif')



def makeEffPlotsVars(tree, varx, vary, sel, nbinx, xmin, xmax, nbiny, ymin, ymax, xtitle, ytitle, leglabel = None, header='', addon=''):
   
    c = TCanvas()

#    binning = [0,20,40,60,80,100,120,140,160,180,200,220,250,300,350,400]
#    binning = [5, 20,21,22,23,24
#    _hist_ = TH2F('h_effp_' + addon, 'h_effp' + addon, len(binning)-1, array('d',binning), nbiny, ymin, ymax)

    _hist_ = TH2F('h_effp_' + addon, 'h_effp' + addon, nbinx, xmin, xmax, nbiny, ymin, ymax)
    dname = vary + ':' + varx + ' >> ' + _hist_.GetName()
    tree.Draw(dname, sel)

    hist = _hist_.ProfileX()

    hist.GetXaxis().SetTitle(xtitle)
    hist.GetYaxis().SetTitle(ytitle)
    hist.GetYaxis().SetNdivisions(507)
    hist.SetLineWidth(3)

    hist.Draw("")
    hist.SetMinimum(0.)
#    hist.SetMaximum(hist.GetMaximum()*1.5)
#    hist.SetTitle(title)
#    hist.SetTitleSize(0.02)

    if header.find('eff')==-1:
        _hist_.SetMarkerColor(38)
        _hist_.SetMarkerSize(0.3)
        _hist_.Draw("colsame")
        hist.Draw('lepsame')

    hist.Draw("axissame")

    leg = TLegend(0.08,0.93,0.5,0.99)
    LegendSettings(leg, 1)

#    tex = TLatex(0.8*hist.GetXaxis().GetXmax(), hist.GetMaximum()*1.6, title)

#    tex.SetTextFont(42)
#    tex.SetTextSize(0.045)
#    tex.Draw()


    if leglabel != None:
        leg.AddEntry(hist, leglabel.replace('pi0','#pi^{0}'), "")
        leg.Draw()

    leg2 = TLegend(0.8,0.93,0.9,0.99)
    LegendSettings(leg2, 1)
    leg2.AddEntry(hist, 'VBF', "")
    leg2.Draw()

#    save(c, 'plots/' + header)

    return copy.deepcopy(hist)
    


def makeCompareVars(hists, xtitle, ytitle, scale ,savestr, ncolumn, addon = ''):
   
    c = TCanvas()

#    col = [1, 1, 2, 4, 8, 6, 30, 40, 50]
    col = [1, 2, 4, 4, 8, 6, 30, 40, 50]

    for ii, hist in enumerate(hists):
        hist.GetXaxis().SetTitle(xtitle)
        hist.GetYaxis().SetTitle(ytitle)
        hist.GetYaxis().SetNdivisions(505)
        hist.GetXaxis().SetNdivisions(505)
#        hist.GetXaxis().SetLabelSize(0.14)
#        hist.SetLineWidth(3)

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
        hist.SetMinimum(0.)

#        print hist.GetName(), hist.GetSumOfWeights(), hist.GetEntries()

        if scale and hist.GetSumOfWeights()!=0:
#            hist.Scale(1./abs(hist.GetSumOfWeights()))
            hist.Scale(1./abs(hist.Integral(0, hist.GetXaxis().GetNbins()+1)))
            hist.SetMaximum(hist.GetMaximum()*1.2)

    ymax = max([ihist.GetMaximum() for ihist in hists])
    ymin = min([ihist.GetMinimum() for ihist in hists])

#    print hists[-1].GetName(), ymax

#    leg = TLegend(0.6,0.7,0.9,0.9)
    leg = TLegend(0.2,0.93,0.6,0.99)
    LegendSettings(leg, ncolumn)

    for ii, hist in enumerate(hists):
        hist.SetMaximum(ymax*1.2)
#        hist.SetMinimum(ymin*1.2)
        hist.SetMinimum(0.)

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

    hists[-1].Draw("axissame")
    leg.Draw()

    tex = TLatex( hists[-1].GetXaxis().GetXmin() + 0.75*(hists[-1].GetXaxis().GetXmax() - hists[-1].GetXaxis().GetXmin()), ymax*1.1, addon.replace('pi0','#pi^{0}'))

    tex.SetTextFont(42)
    tex.SetTextSize(0.045)
    tex.Draw()

    leg2 = TLegend(0.8,0.93,0.9,0.99)
    LegendSettings(leg2, 1)
    leg2.AddEntry(hists[-1], 'VBF', "")
    leg2.Draw()

#    line = TLine(hists[-1].GetXaxis().GetXmin(),0,hists[-1].GetXaxis().GetXmax(),0)
#    line.SetLineStyle(2)
#    line.Draw()

    save(c, 'plots/' + savestr)


def overlay(hists, header, addon):

#    print 'enters overlay function --------------------'

    canvas = TCanvas()
    leg = TLegend(0.2,0.93,0.8,0.99)
    LegendSettings(leg,len(hists))

    col = [1,2,4,6]

#    print hists

    ymax = -1
    for ii, hist in enumerate(hists):
        hist.SetLineColor(col[ii])
        hist.SetMarkerColor(col[ii])
        hist.SetLineWidth(3-ii)

        if ymax < hist.GetMaximum():
            ymax = hist.GetMaximum()

        if ii==0:
            hist.Draw("ep")
        else:
            hist.SetMarkerSize(0)
#            for ibin in range(1, hist.GetXaxis().GetNbins()+1):
#                hist.SetBinError(ibin, 0.)
            hist.Draw("epsame")

#        print hist.GetName()

        if hist.GetName().find('signal')!=-1:
            leg.AddEntry(hist, 'signal', 'lep')
#            leg.AddEntry(hist, 'Dynamic', 'lep')
#            leg.AddEntry(hist, 'Old', 'lep')
        else:
            leg.AddEntry(hist, 'background', 'lep')
#            leg.AddEntry(hist, 'Standard (run-1)', 'lep')
#            leg.AddEntry(hist, 'bugfix', 'lep')

    for hist in hists:
        hist.SetMaximum(ymax*1.4)

#    leg.AddEntry(hists[0], 'Had.', 'f')

    leg.Draw()

    leg2 = TLegend(0.8,0.93,0.9,0.99)
    LegendSettings(leg2, 1)
    leg2.AddEntry(hists[-1], 'VBF', "")
    leg2.Draw()

    tex = TLatex( hists[-1].GetXaxis().GetXmin() + 0.75*(hists[-1].GetXaxis().GetXmax() - hists[-1].GetXaxis().GetXmin()), ymax*1.3, addon.replace('pi0','#pi^{0}'))

    tex.SetTextFont(42)
    tex.SetTextSize(0.045)
    tex.Draw()

    
    save(canvas, 'plots/' + header)

#    print 'end overlay function --------------------'

    

if __name__ == '__main__':



    hdict = {
        'signal':{'file':'analysis_eff/Myroot_dynamic95.root','label':'signal'},
        'background':{'file':'analysis_fake/Myroot_dynamic95.root','label':'background'},
        }

#    criteria_all = 'photon_dm_rough !=-1 && photon_niso < 2'
    criteria_all = 'photon_dm_rough !=-1'
    criteria_sig_all = criteria_all + ' && photon_isIsolation==0'
    criteria_sig_in = criteria_all + ' && photon_isIsolation==0 && photon_isOutside==0'
    criteria_sig_out = criteria_all + ' && photon_isIsolation==0 && photon_isOutside==1'
    criteria_iso_all = criteria_all + ' && photon_isIsolation==1'
    criteria_iso_in = criteria_all + ' && photon_isIsolation==1 && photon_isOutside==0'
    criteria_iso_out = criteria_all + ' && photon_isIsolation==1 && photon_isOutside==1'

#    tcriteria_all = 'tau_dm_rough !=-1 && tau_niso_weighted < 2'
    tcriteria_all = 'tau_dm_rough !=-1'

    pvardict = {
        'photon_pt':{'tree':'per_photon','var':'photon_pt', 'nbin':50, 'xmin':0, 'xmax':20, 'title':'p_{T}^{#gamma} (all)', 'sel':criteria_all},
        'photon_eta':{'tree':'per_photon','var':'photon_eta', 'nbin':50, 'xmin':-2.5, 'xmax':2.5, 'title':'#eta^{#gamma} (all)', 'sel':criteria_all},
#        'photon_phi':{'tree':'per_photon','var':'photon_phi', 'nbin':50, 'xmin':-math.pi, 'xmax':math.pi, 'title':'#phi^{#gamma} (all)', 'sel':criteria_all},

        'photon_pt_sig_all':{'tree':'per_photon','var':'photon_pt', 'nbin':50, 'xmin':0, 'xmax':20, 'title':'p_{T}^{#gamma} (signal, all)', 'sel':criteria_sig_all},
        'photon_eta_sig_all':{'tree':'per_photon','var':'photon_eta', 'nbin':50, 'xmin':-2.5, 'xmax':2.5, 'title':'#eta^{#gamma} (signal, all)', 'sel':criteria_sig_all},
#        'photon_phi_sig_all':{'tree':'per_photon','var':'photon_phi', 'nbin':50, 'xmin':-math.pi, 'xmax':math.pi, 'title':'#phi^{#gamma} (signal, inside)', 'sel':criteria_sig_all},

        'photon_pt_sig_in':{'tree':'per_photon','var':'photon_pt', 'nbin':50, 'xmin':0, 'xmax':20, 'title':'p_{T}^{#gamma} (signal, inside)', 'sel':criteria_sig_in},
        'photon_eta_sig_in':{'tree':'per_photon','var':'photon_eta', 'nbin':50, 'xmin':-2.5, 'xmax':2.5, 'title':'#eta^{#gamma} (signal, inside)', 'sel':criteria_sig_in},
#        'photon_phi_sig_in':{'tree':'per_photon','var':'photon_phi', 'nbin':50, 'xmin':-math.pi, 'xmax':math.pi, 'title':'#phi^{#gamma} (signal, inside)', 'sel':criteria_sig_in},

        'photon_pt_sig_out':{'tree':'per_photon','var':'photon_pt', 'nbin':50, 'xmin':0, 'xmax':20, 'title':'p_{T}^{#gamma} (signal, outside)', 'sel':criteria_sig_out},
        'photon_eta_sig_out':{'tree':'per_photon','var':'photon_eta', 'nbin':50, 'xmin':-2.5, 'xmax':2.5, 'title':'#eta^{#gamma} (signal, outside)', 'sel':criteria_sig_out},
#        'photon_phi_sig_out':{'tree':'per_photon','var':'photon_phi', 'nbin':50, 'xmin':-math.pi, 'xmax':math.pi, 'title':'#phi^{#gamma} (signal, outside)', 'sel':criteria_sig_out},

        'photon_pt_iso_all':{'tree':'per_photon','var':'photon_pt', 'nbin':50, 'xmin':0, 'xmax':20, 'title':'p_{T}^{#gamma} (iso, all)', 'sel':criteria_iso_all},
        'photon_eta_iso_all':{'tree':'per_photon','var':'photon_eta', 'nbin':50, 'xmin':-2.5, 'xmax':2.5, 'title':'#eta^{#gamma} (iso, all)', 'sel':criteria_iso_all},
#        'photon_phi_iso_all':{'tree':'per_photon','var':'photon_phi', 'nbin':50, 'xmin':-math.pi, 'xmax':math.pi, 'title':'#phi^{#gamma} (iso, all)', 'sel':criteria_iso_all},

        'photon_pt_iso_in':{'tree':'per_photon','var':'photon_pt', 'nbin':50, 'xmin':0, 'xmax':20, 'title':'p_{T}^{#gamma} (iso, inside)', 'sel':criteria_iso_in},
        'photon_eta_iso_in':{'tree':'per_photon','var':'photon_eta', 'nbin':50, 'xmin':-2.5, 'xmax':2.5, 'title':'#eta^{#gamma} (iso, inside)', 'sel':criteria_iso_in},
#        'photon_phi_iso_in':{'tree':'per_photon','var':'photon_phi', 'nbin':50, 'xmin':-math.pi, 'xmax':math.pi, 'title':'#phi^{#gamma} (iso, inside)', 'sel':criteria_iso_in},

        'photon_pt_iso_out':{'tree':'per_photon','var':'photon_pt', 'nbin':50, 'xmin':0, 'xmax':20, 'title':'p_{T}^{#gamma} (iso, outside)', 'sel':criteria_iso_out},
        'photon_eta_iso_out':{'tree':'per_photon','var':'photon_eta', 'nbin':50, 'xmin':-2.5, 'xmax':2.5, 'title':'#eta^{#gamma} (iso, outside)', 'sel':criteria_iso_out},
#        'photon_phi_iso_out':{'tree':'per_photon','var':'photon_phi', 'nbin':50, 'xmin':-math.pi, 'xmax':math.pi, 'title':'#phi^{#gamma} (iso, outside)', 'sel':criteria_iso_out},


        'photon_dr':{'tree':'per_photon','var':'photon_dr', 'nbin':50, 'xmin':0, 'xmax':0.5, 'title':'dR(#tau, #gamma) (all)', 'sel':criteria_all},
        'photon_deta':{'tree':'per_photon','var':'photon_deta', 'nbin':50, 'xmin':-0.5, 'xmax':0.5, 'title':'d#eta(#tau, #gamma) (all)', 'sel':criteria_all},
        'photon_dphi':{'tree':'per_photon','var':'photon_dphi', 'nbin':50, 'xmin':-0.5, 'xmax':0.5, 'title':'d#phi(#tau, #gamma) (all)', 'sel':criteria_all},

        'photon_dr_sig_all':{'tree':'per_photon','var':'photon_dr', 'nbin':50, 'xmin':0, 'xmax':0.5, 'title':'dR(#tau, #gamma) (signal, all)', 'sel':criteria_sig_all},
        'photon_deta_sig_all':{'tree':'per_photon','var':'photon_deta', 'nbin':50, 'xmin':-0.5, 'xmax':0.5, 'title':'d#eta(#tau, #gamma) (signal, all)', 'sel':criteria_sig_all},
        'photon_dphi_sig_all':{'tree':'per_photon','var':'photon_dphi', 'nbin':50, 'xmin':-0.5, 'xmax':0.5, 'title':'d#phi(#tau, #gamma) (signal, all)', 'sel':criteria_sig_all},


        'photon_dr_sig_in':{'tree':'per_photon','var':'photon_dr', 'nbin':50, 'xmin':0, 'xmax':0.5, 'title':'dR(#tau, #gamma) (signal, inside)', 'sel':criteria_sig_in},
        'photon_deta_sig_in':{'tree':'per_photon','var':'photon_deta', 'nbin':50, 'xmin':-0.5, 'xmax':0.5, 'title':'d#eta(#tau, #gamma) (signal, inside)', 'sel':criteria_sig_in},
        'photon_dphi_sig_in':{'tree':'per_photon','var':'photon_dphi', 'nbin':50, 'xmin':-0.5, 'xmax':0.5, 'title':'d#phi(#tau, #gamma) (signal, inside)', 'sel':criteria_sig_in},

        'photon_dr_sig_out':{'tree':'per_photon','var':'photon_dr', 'nbin':50, 'xmin':0, 'xmax':0.5, 'title':'dR(#tau, #gamma) (signal, outside)', 'sel':criteria_sig_out},
        'photon_deta_sig_out':{'tree':'per_photon','var':'photon_deta', 'nbin':50, 'xmin':-0.5, 'xmax':0.5, 'title':'d#eta(#tau, #gamma) (signal, outside)', 'sel':criteria_sig_out},
        'photon_dphi_sig_out':{'tree':'per_photon','var':'photon_dphi', 'nbin':50, 'xmin':-0.5, 'xmax':0.5, 'title':'d#phi(#tau, #gamma) (signal, outside)', 'sel':criteria_sig_out},

        'photon_dr_iso_all':{'tree':'per_photon','var':'photon_dr', 'nbin':50, 'xmin':0, 'xmax':0.5, 'title':'dR(#tau, #gamma) (iso, all)', 'sel':criteria_iso_all},
        'photon_deta_iso_all':{'tree':'per_photon','var':'photon_deta', 'nbin':50, 'xmin':-0.5, 'xmax':0.5, 'title':'d#eta(#tau, #gamma) (iso, all)', 'sel':criteria_iso_all},
        'photon_dphi_iso_all':{'tree':'per_photon','var':'photon_dphi', 'nbin':50, 'xmin':-0.5, 'xmax':0.5, 'title':'d#phi(#tau, #gamma) (iso, all)', 'sel':criteria_iso_all},


        'photon_dr_iso_in':{'tree':'per_photon','var':'photon_dr', 'nbin':50, 'xmin':0, 'xmax':0.5, 'title':'dR(#tau, #gamma) (iso, inside)', 'sel':criteria_iso_in},
        'photon_deta_iso_in':{'tree':'per_photon','var':'photon_deta', 'nbin':50, 'xmin':-0.5, 'xmax':0.5, 'title':'d#eta(#tau, #gamma) (iso, inside)', 'sel':criteria_iso_in},
        'photon_dphi_iso_in':{'tree':'per_photon','var':'photon_dphi', 'nbin':50, 'xmin':-0.5, 'xmax':0.5, 'title':'d#phi(#tau, #gamma) (iso, inside)', 'sel':criteria_iso_in},

        'photon_dr_iso_out':{'tree':'per_photon','var':'photon_dr', 'nbin':50, 'xmin':0, 'xmax':0.5, 'title':'dR(#tau, #gamma) (iso, outside)', 'sel':criteria_iso_out},
        'photon_deta_iso_out':{'tree':'per_photon','var':'photon_deta', 'nbin':50, 'xmin':-0.5, 'xmax':0.5, 'title':'d#eta(#tau, #gamma) (iso, outside)', 'sel':criteria_iso_out},
        'photon_dphi_iso_out':{'tree':'per_photon','var':'photon_dphi', 'nbin':50, 'xmin':-0.5, 'xmax':0.5, 'title':'d#phi(#tau, #gamma) (iso, outside)', 'sel':criteria_iso_out},


        'photon_pt_ratio':{'tree':'per_photon','var':'photon_pt/photon_taupt', 'nbin':50, 'xmin':0, 'xmax':1, 'title':'p_{T}^{#gamma}/tau pT (all)', 'sel':criteria_all},
        'photon_pt_ratio_sig_all':{'tree':'per_photon','var':'photon_pt/photon_taupt', 'nbin':50, 'xmin':0, 'xmax':1, 'title':'p_{T}^{#gamma}/tau pT (signal, all)', 'sel':criteria_sig_all},
        'photon_pt_ratio_sig_in':{'tree':'per_photon','var':'photon_pt/photon_taupt', 'nbin':50, 'xmin':0, 'xmax':1, 'title':'p_{T}^{#gamma}/tau pT (signal, inside)', 'sel':criteria_sig_in},
        'photon_pt_ratio_sig_out':{'tree':'per_photon','var':'photon_pt/photon_taupt', 'nbin':50, 'xmin':0, 'xmax':1, 'title':'p_{T}^{#gamma}/tau pT (signal, outside)', 'sel':criteria_sig_out},
        'photon_pt_ratio_iso_all':{'tree':'per_photon','var':'photon_pt/photon_taupt', 'nbin':50, 'xmin':0, 'xmax':1, 'title':'p_{T}^{#gamma}/tau pT (iso, all)', 'sel':criteria_iso_all},
        'photon_pt_ratio_iso_in':{'tree':'per_photon','var':'photon_pt/photon_taupt', 'nbin':50, 'xmin':0, 'xmax':1, 'title':'p_{T}^{#gamma}/tau pT (iso, inside)', 'sel':criteria_iso_in},
        'photon_pt_ratio_iso_out':{'tree':'per_photon','var':'photon_pt/photon_taupt', 'nbin':50, 'xmin':0, 'xmax':1, 'title':'p_{T}^{#gamma}/tau pT (iso, outside)', 'sel':criteria_iso_out},


        'nphoton_isolation':{'tree':'per_tau','var':'tau_nphoton', 'nbin':30, 'xmin':0, 'xmax':30, 'title':'# of isolation PF Gamma (all)', 'sel':tcriteria_all},
        'nphoton_signal':{'tree':'per_tau','var':'tau_nphoton_signal', 'nbin':30, 'xmin':0, 'xmax':30, 'title':'# of signal PF Gamma (all)', 'sel':tcriteria_all},
        'nphoton_signal_1p':{'tree':'per_tau','var':'tau_nphoton_signal', 'nbin':30, 'xmin':0, 'xmax':30, 'title':'# of signal PF Gamma (all, 1p)', 'sel':'tau_dm_rough==0'},
        'nphoton_signal_1p1p0':{'tree':'per_tau','var':'tau_nphoton_signal', 'nbin':30, 'xmin':0, 'xmax':30, 'title':'# of signal PF Gamma (all, 1p1p0)', 'sel':'tau_dm_rough==1'},
        'nphoton_signal_3p':{'tree':'per_tau','var':'tau_nphoton_signal', 'nbin':30, 'xmin':0, 'xmax':30, 'title':'# of signal PF Gamma (all, 3p)', 'sel':'tau_dm_rough==2'},
        'nphoton_all':{'tree':'per_tau','var':'tau_nphoton + tau_nphoton_signal', 'nbin':30, 'xmin':0, 'xmax':30, 'title':'# of signal + iso PF Gamma (all)', 'sel':tcriteria_all},

        'nphoton_inside':{'tree':'per_tau','var':'tau_nphoton_inside', 'nbin':30, 'xmin':0, 'xmax':30, 'title':'# signal PF Gamma (inside)', 'sel':tcriteria_all},
        'nphoton_outside':{'tree':'per_tau','var':'tau_nphoton_outside', 'nbin':30, 'xmin':0, 'xmax':30, 'title':'# signal PF Gamma (outside)', 'sel':tcriteria_all},

        'nphoton_iso_inside':{'tree':'per_tau','var':'tau_nphoton_iso_inside', 'nbin':30, 'xmin':0, 'xmax':30, 'title':'# isolation PF Gamma (inside)', 'sel':tcriteria_all},
        'nphoton_iso_outside':{'tree':'per_tau','var':'tau_nphoton_iso_outside', 'nbin':30, 'xmin':0, 'xmax':30, 'title':'# isolation PF Gamma (outside)', 'sel':tcriteria_all},
        
        'ptsum_sig_all':{'tree':'per_tau','var':'tau_photonsumpt_inside + tau_photonsumpt_outside', 'nbin':30, 'xmin':0, 'xmax':20, 'title':'#sum p_{T} (sig)', 'sel':tcriteria_all},
        'ptsum_sig_all_ratio':{'tree':'per_tau','var':'(tau_photonsumpt_inside + tau_photonsumpt_outside)/tau_pt', 'nbin':30, 'xmin':0, 'xmax':1, 'title':'#sum p_{T} (sig) / tau pT', 'sel':tcriteria_all},

        'ptsum_sig_inside':{'tree':'per_tau','var':'tau_photonsumpt_inside', 'nbin':30, 'xmin':0, 'xmax':20, 'title':'#sum p_{T} (sig, inside)', 'sel':tcriteria_all},
        'ptsum_sig_outside':{'tree':'per_tau','var':'tau_photonsumpt_outside', 'nbin':30, 'xmin':0, 'xmax':20, 'title':'#sum p_{T} (sig, outside)', 'sel':tcriteria_all},
        'ptsum_sig_inside_ratio':{'tree':'per_tau','var':'tau_photonsumpt_inside/tau_pt', 'nbin':30, 'xmin':0, 'xmax':1, 'title':'#sum p_{T} / tau pT (sig, inside)', 'sel':tcriteria_all},
        'ptsum_sig_outside_ratio':{'tree':'per_tau','var':'tau_photonsumpt_outside/tau_pt', 'nbin':30, 'xmin':0, 'xmax':1, 'title':'#sum p_{T} / tau pT (sig, outside)', 'sel':tcriteria_all},

        'ptsum_iso_all':{'tree':'per_tau','var':'tau_photonsumpt_iso_inside + tau_photonsumpt_iso_outside', 'nbin':30, 'xmin':0, 'xmax':20, 'title':'#sum p_{T} (iso)', 'sel':tcriteria_all},
        'ptsum_iso_all_ratio':{'tree':'per_tau','var':'(tau_photonsumpt_iso_inside + tau_photonsumpt_iso_outside)/tau_pt', 'nbin':30, 'xmin':0, 'xmax':1, 'title':'#sum p_{T} (iso) / tau pT', 'sel':tcriteria_all},

        'ptsum_iso_inside':{'tree':'per_tau','var':'tau_photonsumpt_iso_inside', 'nbin':30, 'xmin':0, 'xmax':20, 'title':'#sum p_{T} (iso, inside)', 'sel':tcriteria_all},
        'ptsum_iso_outside':{'tree':'per_tau','var':'tau_photonsumpt_iso_outside', 'nbin':30, 'xmin':0, 'xmax':20, 'title':'#sum p_{T} (iso, outside)', 'sel':tcriteria_all},
        'ptsum_iso_inside_ratio':{'tree':'per_tau','var':'tau_photonsumpt_iso_inside/tau_pt', 'nbin':30, 'xmin':0, 'xmax':1, 'title':'#sum p_{T} / tau pT (iso, inside)', 'sel':tcriteria_all},
        'ptsum_iso_outside_ratio':{'tree':'per_tau','var':'tau_photonsumpt_iso_outside/tau_pt', 'nbin':30, 'xmin':0, 'xmax':1, 'title':'#sum p_{T} / tau pT (iso, outside)', 'sel':tcriteria_all},

        'tau_adR_signal':{'tree':'per_tau','var':'tau_adR_signal', 'nbin':30, 'xmin':-1, 'xmax':1, 'title':'Average dR inside signal cone', 'sel':tcriteria_all},
        'tau_wdR_signal':{'tree':'per_tau','var':'tau_adR_signal', 'nbin':30, 'xmin':-1, 'xmax':1, 'title':'Weighted dR inside signal cone', 'sel':tcriteria_all},
        'tau_adR_iso':{'tree':'per_tau','var':'tau_adR_iso', 'nbin':30, 'xmin':-1, 'xmax':1, 'title':'Average dR in isolation cone', 'sel':tcriteria_all},
        'tau_wdR_iso':{'tree':'per_tau','var':'tau_adR_iso', 'nbin':30, 'xmin':-1, 'xmax':1, 'title':'Weighted dR in isolation cone', 'sel':tcriteria_all},

        }


    for vkey, ivar in pvardict.iteritems():

        hists = []
        hists_eff = []

        for key, val in sorted(hdict.iteritems()):

            tfile = TFile(val['file'])
            tree = tfile.Get(ivar['tree'])
            
            hist = TH1F('h_' + key + '_' + vkey,
                        'h_' + key + '_' + vkey,
                        ivar['nbin'], ivar['xmin'], ivar['xmax'])
            
            hist.SetTitle(val['label'])
            hist.Sumw2()
            tree.Draw(ivar['var'] + ' >> ' + hist.GetName(), ivar['sel'])

            hists.append(copy.deepcopy(hist))

#            def makeEffPlotsVars(tree, varx, vary, sel, nbinx, xmin, xmax, nbiny, ymin, ymax, xtitle, ytitle, leglabel = None, header='', addon=''):

            vname = 'tau_gvertex'
            if ivar['tree']=='per_photon':
                vname = 'photon_gvertex'
            
            yval = ivar['var']
            tname = ivar['title']
            if vkey.find('photon_eta')!=-1 or vkey.find('photon_deta')!=-1 or vkey.find('photon_dphi')!=-1:
                yval = 'abs(' + ivar['var'] + ')'
                tname = '|' + ivar['title'] + '|'

            hists_eff.append(makeEffPlotsVars(tree, vname, yval, ivar['sel'], 25, 5, 30, ivar['nbin'], ivar['xmin'], ivar['xmax'], '# of good vertices', tname, val['label'], '', vkey + '_' + key))
       

        makeCompareVars(hists, ivar['title'], 'a.u.', True , 'compare_' + vkey, len(hists), '')
        overlay(hists_eff, header='nvtx_' + vkey, addon='')
