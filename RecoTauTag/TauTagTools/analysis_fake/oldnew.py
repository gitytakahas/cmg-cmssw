import os, numpy, math, copy, math
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
    ensureDir('plots_isolation_newold')
#    canvas.SaveAs(name.replace(' ','').replace('&&','')+'.pdf')
    canvas.SaveAs(name.replace(' ','').replace('&&','')+'.gif')



def makeEffPlotsVars(tree, varx, vary, sel, nbinx, xmin, xmax, nbiny, ymin, ymax, xtitle, ytitle, leglabel = None, header='', addon=''):
   
    c = TCanvas()
    _hist_ = TH2F('h_effp_' + addon, 'h_effp' + addon, nbinx, xmin, xmax, nbiny, ymin, ymax)
    dname = vary + ':' + varx + ' >> ' + _hist_.GetName()
    tree.Draw(dname, sel)

    hist = _hist_.ProfileX()

    hist.GetXaxis().SetTitle(xtitle)
    hist.GetYaxis().SetTitle(ytitle)
    hist.GetYaxis().SetNdivisions(507)
    hist.SetLineWidth(3)

    hist.Draw("")
#    hist.SetMinimum(0.)
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

#    leg2 = TLegend(0.8,0.93,0.9,0.99)
#    LegendSettings(leg2, 1)
#    leg2.AddEntry(hist, 'VBF', "")
#    leg2.Draw()

    save(c, 'plots_isolation_newold/' + header)

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
    leg2.AddEntry(hists[-1], 'QCD', "")
    leg2.Draw()

#    line = TLine(hists[-1].GetXaxis().GetXmin(),0,hists[-1].GetXaxis().GetXmax(),0)
#    line.SetLineStyle(2)
#    line.Draw()

    save(c, 'plots_isolation_newold/' + savestr)


def overlay(hists, header, addon):

#    print 'enters overlay function --------------------'

    canvas = TCanvas()
    leg = TLegend(0.2,0.93,0.6,0.99)
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
        else:
            leg.AddEntry(hist, 'Standard', 'lep')

    for hist in hists:
        hist.SetMaximum(ymax*1.4)

#    leg.AddEntry(hists[0], 'Had.', 'f')

    leg.Draw()

    leg2 = TLegend(0.8,0.93,0.9,0.99)
    LegendSettings(leg2, 1)
    leg2.AddEntry(hists[-1], 'QCD', "")
    leg2.Draw()

    tex = TLatex( hists[-1].GetXaxis().GetXmin() + 0.75*(hists[-1].GetXaxis().GetXmax() - hists[-1].GetXaxis().GetXmin()), ymax*1.3, addon.replace('pi0','#pi^{0}'))

    tex.SetTextFont(42)
    tex.SetTextSize(0.045)
    tex.Draw()

    
    save(canvas, 'plots_isolation_newold/' + header)

#    print 'end overlay function --------------------'

    

if __name__ == '__main__':


    vardict = {
        'ptdiff':{'tree':'tree','varx':'tau_pt_new', 'vary':'tau_pt_old', 'nbin':50, 'xmin':20, 'xmax':150, 'title':'tau p_{T} (new)', 'sel':'1'},
        'deta':{'tree':'tree','varx':'tau_eta_new', 'vary':'tau_eta_old', 'nbin':50, 'xmin':-2.3, 'xmax':2.3, 'title':'tau #eta (new)', 'sel':'1'},
        'dphi':{'tree':'tree','varx':'tau_phi_new', 'vary':'tau_phi_old', 'nbin':50, 'xmin':-3.14, 'xmax':3.14, 'title':'tau #phi (new)', 'sel':'1'},
        'dniso':{'tree':'tree','varx':'tau_niso_new', 'vary':'tau_niso_old', 'nbin':50, 'xmin':0, 'xmax':10, 'title':'tau neutral iso (new)', 'sel':'1'},
        'dciso':{'tree':'tree','varx':'tau_ciso_new', 'vary':'tau_ciso_old', 'nbin':50, 'xmin':0, 'xmax':10, 'title':'tau charged iso (new)', 'sel':'1'},
        'dnwiso':{'tree':'tree','varx':'tau_nwiso_new', 'vary':'tau_nwiso_old', 'nbin':50, 'xmin':0, 'xmax':10, 'title':'tau neutral weight iso (new)', 'sel':'1'},
        }


    tfile = TFile('output.root')
    tree = tfile.Get('tree')


    for key, ivar in vardict.iteritems():
        makeEffPlotsVars(tree, ivar['varx'], ivar['vary'], ivar['sel'], ivar['nbin'], ivar['xmin'], ivar['xmax'], ivar['nbin'], ivar['xmin'], ivar['xmax'], ivar['title'], ivar['title'].replace('new', 'old'), leglabel = None, header=key, addon='')








    pvardict = {
        'ptdiff':{'tree':'tree','var':'tau_pt_new - tau_pt_old', 'nbin':100, 'xmin':0, 'xmax':20, 'title':'tau p_{T} (new - old)', 'sel':'1'},
        'deta':{'tree':'tree','var':'tau_eta_new - tau_eta_old', 'nbin':100, 'xmin':-0.1, 'xmax':0.1, 'title':'tau #eta (new - old)', 'sel':'1'},
        'dphi':{'tree':'tree','var':'tau_phi_new - tau_phi_old', 'nbin':100, 'xmin':-0.1, 'xmax':0.1, 'title':'tau #phi (new - old)', 'sel':'1'},
        'dniso':{'tree':'tree','var':'tau_niso_new - tau_niso_old', 'nbin':100, 'xmin':-5, 'xmax':5, 'title':'tau neutral iso (new - old)', 'sel':'1'},
        'dciso':{'tree':'tree','var':'tau_ciso_new - tau_ciso_old', 'nbin':100, 'xmin':-5, 'xmax':5, 'title':'tau charged iso (new - old)', 'sel':'1'},
        'dnwiso':{'tree':'tree','var':'tau_nwiso_new - tau_nwiso_old', 'nbin':100, 'xmin':-2, 'xmax':2, 'title':'tau neutral weight iso (new - old)', 'sel':'1'},
        }

    for key, ivar in pvardict.iteritems():

        hists = []
        hist = TH1F('h_' + key,
                    'h_' + key, 
                    ivar['nbin'], ivar['xmin'], ivar['xmax'])
                  
        hist.SetTitle('')
        hist.Sumw2()
        tree.Draw(ivar['var'] + ' >> ' + hist.GetName(), ivar['sel'])

        hists.append(copy.deepcopy(hist))
        makeCompareVars(hists, ivar['title'], 'events', False , 'compare_' + key, len(hists))

