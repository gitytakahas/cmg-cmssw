import numpy
from ROOT import TH1F, TGraph, gStyle, TLegend, gSystem, TCanvas, kBlue, kRed, TLatex

gStyle.SetOptTitle(0)

pt_mu = numpy.ndarray([6.])
sig_mu = numpy.ndarray([6.])
sig_comb_mu = numpy.ndarray([6.])

pt_e = numpy.ndarray([7.])
sig_e = numpy.ndarray([7.])
sig_comb_e = numpy.ndarray([7.])

def LegendSettings(leg):
    leg.SetBorderSize(0)
    leg.SetFillColor(0)
    leg.SetLineColor(0)
    leg.SetFillStyle(0)
    leg.SetTextSize(0.04)
    leg.SetTextFont(42)



for ipt in range(len(pt_mu)):
    pt_mu[ipt] = 21. + ipt*3

for ipt in range(len(pt_e)):
    pt_e[ipt] = 24. + ipt*3

sig_mu[0] = 0.50
sig_mu[1] = 0.52
sig_mu[2] = 0.55
sig_mu[3] = 0.58
sig_mu[4] = 0.62
sig_mu[5] = 0.66


sig_comb_mu[0] = 0.5
sig_comb_mu[1] = 0.5
sig_comb_mu[2] = 0.5
sig_comb_mu[3] = 0.5
sig_comb_mu[4] = 0.5
sig_comb_mu[5] = 0.5

# done for mt channel!

sig_e[0] = 0.73
sig_e[1] = 0.75
sig_e[2] = 0.77
sig_e[3] = 0.8
sig_e[4] = 0.83
sig_e[5] = 0.85
sig_e[6] = 0.86


sig_comb_e[0] = 0.73
sig_comb_e[1] = 0.73
sig_comb_e[2] = 0.73
sig_comb_e[3] = 0.73
sig_comb_e[4] = 0.73
sig_comb_e[5] = 0.73
sig_comb_e[6] = 0.73


canvas = TCanvas('c','c',640,640)
canvas.SetLeftMargin(0.14);
canvas.SetRightMargin(0.06);
canvas.SetTopMargin(0.075);
canvas.SetBottomMargin(0.12);
canvas.SetBorderSize(2);
canvas.Draw()

h_mt = TGraph(6, pt_mu, sig_mu)
h_mt.SetMarkerStyle(20)
h_mt.SetLineStyle(2)
h_mt.SetLineWidth(2)
h_mt.SetMarkerColor(kRed)
h_mt.SetLineColor(kRed)

h_mt.GetXaxis().SetLabelSize(0.04)
h_mt.GetYaxis().SetLabelSize(0.04)

h_mt.GetXaxis().SetTitleSize(0.05)
h_mt.GetXaxis().SetTitleOffset(1.2)
h_mt.GetXaxis().SetNdivisions(508)
h_mt.GetXaxis().SetTitle('muon p_{T} (GeV)')

h_mt.GetYaxis().SetTitleSize(0.05)
h_mt.GetYaxis().SetTitleOffset(1.2)
h_mt.GetYaxis().SetNdivisions(509)
h_mt.GetYaxis().SetTitle('expected uncertainty on #mu-value')

h_mt.SetMaximum(1.)
h_mt.SetMinimum(0.)
h_mt.Draw("apl")


h_mt_comb = TGraph(6, pt_mu, sig_comb_mu)
h_mt_comb.SetMarkerStyle(20)
h_mt_comb.SetLineStyle(2)
h_mt_comb.SetMarkerColor(kBlue)
h_mt_comb.SetLineColor(kBlue)

h_mt_comb.SetLineWidth(2)
h_mt_comb.Draw("plsame")

#leg = TLegend(0.56,0.2,0.86,0.38)
leg = TLegend(0.6,0.2,0.9,0.4)
LegendSettings(leg)
leg.AddEntry(h_mt,'single lepton','lp')
leg.AddEntry(h_mt_comb,'combined','lp')
leg.Draw()

tex = TLatex(21., 0.25, "#mu#tau")
tex.SetTextSize(0.07)
tex.SetLineWidth(2)
tex.Draw()


####################################################

ecanvas = TCanvas('ce','ce',640,640)
ecanvas.SetLeftMargin(0.14);
ecanvas.SetRightMargin(0.06);
ecanvas.SetTopMargin(0.075);
ecanvas.SetBottomMargin(0.12);
ecanvas.SetBorderSize(2);
ecanvas.Draw()

h_et = TGraph(6, pt_e, sig_e)
h_et.SetMarkerStyle(20)
h_et.SetLineStyle(2)
h_et.SetLineWidth(2)
h_et.SetMarkerColor(kRed)
h_et.SetLineColor(kRed)

h_et.GetXaxis().SetLabelSize(0.04)
h_et.GetYaxis().SetLabelSize(0.04)

h_et.GetXaxis().SetTitleSize(0.05)
h_et.GetXaxis().SetTitleOffset(1.2)
h_et.GetXaxis().SetNdivisions(508)
h_et.GetXaxis().SetTitle('electron p_{T} (GeV)')

h_et.GetYaxis().SetTitleSize(0.05)
h_et.GetYaxis().SetTitleOffset(1.2)
h_et.GetYaxis().SetNdivisions(509)
h_et.GetYaxis().SetTitle('expected uncertainty on #mu-value')

h_et.SetMaximum(1)
h_et.SetMinimum(0.)
h_et.Draw("apl")


h_et_comb = TGraph(6, pt_e, sig_comb_e)
h_et_comb.SetMarkerStyle(20)
h_et_comb.SetLineStyle(2)
h_et_comb.SetMarkerColor(kBlue)
h_et_comb.SetLineColor(kBlue)

h_et_comb.SetLineWidth(2)
h_et_comb.Draw("plsame")



eleg = TLegend(0.6,0.2,0.9,0.4)
LegendSettings(eleg)
eleg.AddEntry(h_et,'single lepton','lp')
eleg.AddEntry(h_et_comb,'combined','lp')
eleg.Draw()

etex = TLatex(24., 0.25, "e#tau")
etex.SetTextSize(0.07)
etex.SetLineWidth(2)
etex.Draw()


canvas.SaveAs('mu_value_mt.eps')
ecanvas.SaveAs('mu_value_et.eps')
