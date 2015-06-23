import os, numpy, math, copy, math
from array import array
from ROOT import TLegend, TCanvas, TColor, kMagenta, kOrange, kRed, kBlue, kGray, kBlack, gROOT, gStyle, TFile, TH1F, TH2F, TLatex, TLine
from officialStyle import officialStyle

gROOT.SetBatch(True)
officialStyle(gStyle)
gStyle.SetOptTitle(0)
gStyle.SetOptStat(0)

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
    ensureDir('plots_energyscale')
    canvas.SaveAs(name.replace(' ','').replace('&&','')+'.pdf')
    canvas.SaveAs(name.replace(' ','').replace('&&','')+'.gif')


def RV(val):
  return '{0:.2f}'.format(val)


def makeEffPlotsVars(tree, varx, vary, sel, nbinx, xmin, xmax, nbiny, ymin, ymax, xtitle, ytitle, leglabel = None, header='', addon='', option='pt'):
   
    c = TCanvas()

#    binning = [0,20,40,60,80,100,120,140,160,180,200,220,250,300,350,400]
    binning = [20,30,40,50,60,70,80,90,100,120,150,200,300]
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
        leg.AddEntry(hist, leglabel.replace('1pi0',' + #pi^{0}'), "")
        leg.Draw()

    leg2 = TLegend(0.8,0.93,0.9,0.99)
    LegendSettings(leg2, 1)
    leg2.AddEntry(hist, 'VBF', "")
    leg2.Draw()

    save(c, 'plots_energyscale/' + header)

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
            hist.Scale(1./abs(hist.GetSumOfWeights()))
            hist.SetMaximum(hist.GetMaximum()*1.2)

    ymax = max([ihist.GetMaximum() for ihist in hists])
    ymin = min([ihist.GetMinimum() for ihist in hists])

#    print hists[-1].GetName(), ymax

    leg = TLegend(0.55,0.6,0.8,0.8)
#    leg = TLegend(0.2,0.93,0.6,0.99)
    LegendSettings(leg, 1)

    for ii, hist in enumerate(hists):
        hist.SetMaximum(ymax*1.2)
#        hist.SetMinimum(ymin*1.2)
        hist.SetMinimum(0.)

        if ii==0:
            hist.Draw('hep')

        else:
            hist.Draw('hepsame')

        lname = hist.GetTitle()
        lname2 = ' (Mean =' + RV(hist.GetMean()) + ', RMS =' + RV(hist.GetRMS()) + ')'
        leg.AddEntry(hist, lname, "l")
        leg.AddEntry(hist, lname2, "")


    hists[-1].Draw("axissame")
    leg.Draw()

    tex = TLatex( hists[-1].GetXaxis().GetXmin() + 0.75*(hists[-1].GetXaxis().GetXmax() - hists[-1].GetXaxis().GetXmin()), ymax*1.1, addon.replace('1pi0',' + #pi^{0}'))

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

    save(c, 'plots_energyscale/' + savestr)


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
 
        if hist.GetName().find('dynamic')!=-1:
            leg.AddEntry(hist, 'Dynamic', 'lep')
#            leg.AddEntry(hist, 'Old', 'lep')
        else:
            leg.AddEntry(hist, 'Standard', 'lep')
#            leg.AddEntry(hist, 'bugfix', 'lep')

    for hist in hists:
        hist.SetMaximum(ymax*1.4)

#    leg.AddEntry(hists[0], 'Had.', 'f')

    leg.Draw()

    leg2 = TLegend(0.8,0.93,0.9,0.99)
    LegendSettings(leg2, 1)
    leg2.AddEntry(hists[-1], 'VBF', "")
    leg2.Draw()

    tex = TLatex( hists[-1].GetXaxis().GetXmin() + 0.75*(hists[-1].GetXaxis().GetXmax() - hists[-1].GetXaxis().GetXmin()), ymax*1.3, addon.replace('1pi0',' + #pi^{0}'))

    tex.SetTextFont(42)
    tex.SetTextSize(0.045)
    tex.Draw()

    
    save(canvas, 'plots_energyscale/' + header)

#    print 'end overlay function --------------------'

    

if __name__ == '__main__':



    hdict = {
        'dynamic':{'file':'../analysis_eff/Myroot_dynamic95.root','label':'Dynamic'},
#        'dynamic':{'file':'Myroot_standard_old.root','label':'Old'},
#        'standard':{'file':'Myroot_dynamic_TauGun.root','label':'Standard'},
        'standard':{'file':'../analysis_eff/Myroot_standard.root','label':'Standard'},
#        'standard':{'file':'Myroot_standard.root','label':'bugfix'},
#        'standard':{'file':'Myroot_dynamic95.root','label':'sta'}, 
        }

#    ddict = {'1p0pi0':'tau_gendm_rough==0', '1p1pi0':'tau_gendm_rough==1', '3p':'tau_gendm_rough==2', 'Inclusive':'1'}
    ddict = {'1prong':'tau_dm_rough==0', '1p1pi0':'tau_dm_rough==1', '3prong':'tau_dm_rough==2', 'Inclusive':'1'}

    vardict = {
        'ptratio':{'tree':'per_tau','var':'tau_pt/tau_genpt', 'nbin':50, 'xmin':0, 'xmax':2, 'title':'tau p_{T} / tau gen p_{T}^{vis}', 'sel':'tau_dm!=-1 && tau_pt > 20 && abs(tau_eta) < 2.3'},
        }




    for vkey, ivar in vardict.iteritems():
        for dkey, dm in ddict.iteritems():

            hists = []
            for key, val in sorted(hdict.iteritems()):

                tfile = TFile(val['file'])
                tree = tfile.Get(ivar['tree'])

                hist = TH1F('h_' + key + '_' + vkey + '_' + dkey, 
                            'h_' + key + '_' + vkey + '_' + dkey, 
                            ivar['nbin'], ivar['xmin'], ivar['xmax'])
                   
                hist.SetTitle(val['label'])
                hist.Sumw2()
                tree.Draw(ivar['var'] + ' >> ' + hist.GetName(), dm + '&&' + ivar['sel'])

                hists.append(copy.deepcopy(hist))
       
                makeCompareVars(hists, ivar['title'], 'a.u.', True , 'compare_' + vkey + dkey, len(hists), dkey)




    hdict = {
        'dynamic':{'file':'../analysis_fake/Myroot_dynamic95.root','label':'Dynamic'},
        'standard':{'file':'../analysis_fake/Myroot_standard.root','label':'Standard'},
        }

    vardict = {
        'ptratio':{'tree':'per_tau','var':'tau_pt/tau_corjetpt', 'nbin':50, 'xmin':0, 'xmax':2, 'title':'tau p_{T} / corrected jet p_{T}', 'sel':'tau_dm !=-1 && tau_pt > 20 && abs(tau_eta) < 2.3'},
        }




    for vkey, ivar in vardict.iteritems():
        for dkey, dm in ddict.iteritems():

            hists = []
            for key, val in sorted(hdict.iteritems()):

                tfile = TFile(val['file'])
                tree = tfile.Get(ivar['tree'])

                hist = TH1F('h_' + key + '_' + vkey + '_' + dkey, 
                            'h_' + key + '_' + vkey + '_' + dkey, 
                            ivar['nbin'], ivar['xmin'], ivar['xmax'])
                   
                hist.SetTitle(val['label'])
                hist.Sumw2()
                tree.Draw(ivar['var'] + ' >> ' + hist.GetName(), dm + '&&' + ivar['sel'])

                hists.append(copy.deepcopy(hist))
       
                makeCompareVars(hists, ivar['title'], 'a.u.', True , 'compare_jet_' + vkey + dkey, len(hists), dkey)


