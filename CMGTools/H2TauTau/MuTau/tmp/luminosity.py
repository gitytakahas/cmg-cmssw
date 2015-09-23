import numpy
from ROOT import TH1F, TGraph, gStyle, TLegend, gSystem, TCanvas, kBlue, kRed, TLatex

gStyle.SetOptTitle(0)

pt_mu = numpy.ndarray([6.])
sig_mu = numpy.ndarray([6.])
sig_comb_mu = numpy.ndarray([6.])
sig_lum_mu = numpy.ndarray([6.])

pt_e = numpy.ndarray([7.])
sig_e = numpy.ndarray([7.])
sig_comb_e = numpy.ndarray([7.])
sig_lum_e = numpy.ndarray([7.])

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

sig_mu[0] = 2.267
sig_mu[1] = 2.187
sig_mu[2] = 2.067
sig_mu[3] = 1.950
sig_mu[4] = 1.835
sig_mu[5] = 1.727



sig_comb_mu[0] = 2.265
sig_comb_mu[1] = 2.277
sig_comb_mu[2] = 2.286
sig_comb_mu[3] = 2.288
sig_comb_mu[4] = 2.289
sig_comb_mu[5] = 2.289

# done for mt channel!

sig_e[0] = 1.483
sig_e[1] = 1.454
sig_e[2] = 1.415
sig_e[3] = 1.359
sig_e[4] = 1.321
sig_e[5] = 1.283
sig_e[6] = 1.279


sig_comb_e[0] = 1.483
sig_comb_e[1] = 1.485
sig_comb_e[2] = 1.487
sig_comb_e[3] = 1.489
sig_comb_e[4] = 1.490
sig_comb_e[5] = 1.495
sig_comb_e[6] = 1.495




for ipt in range(len(pt_mu)):
    sig_lum_mu[ipt] = ((sig_comb_mu[ipt]/sig_mu[ipt])**2 - 1.)*100.
    print sig_lum_mu[ipt]
    
for ipt in range(len(pt_e)):
    sig_lum_e[ipt] = ((sig_comb_e[ipt]/sig_e[ipt])**2 - 1.)*100.
    print sig_lum_e[ipt]


canvas = TCanvas('c','c',640,640)
canvas.SetLeftMargin(0.14);
canvas.SetRightMargin(0.06);
canvas.SetTopMargin(0.075);
canvas.SetBottomMargin(0.12);
canvas.SetBorderSize(2);
canvas.Draw()

h_mt = TGraph(6, pt_mu, sig_lum_mu)
h_mt.SetMarkerStyle(20)
h_mt.SetLineStyle(2)
h_mt.SetLineWidth(2)

h_mt.GetXaxis().SetLabelSize(0.04)
h_mt.GetYaxis().SetLabelSize(0.04)

h_mt.GetXaxis().SetTitleSize(0.05)
h_mt.GetXaxis().SetTitleOffset(1.2)
h_mt.GetXaxis().SetNdivisions(508)
h_mt.GetXaxis().SetTitle('muon p_{T} (GeV)')

h_mt.GetYaxis().SetTitleSize(0.05)
h_mt.GetYaxis().SetTitleOffset(1.2)
h_mt.GetYaxis().SetNdivisions(509)
h_mt.GetYaxis().SetTitle('gain in effective luminosity (%)')

h_mt.SetMaximum(100)
h_mt.SetMinimum(-10)
h_mt.Draw("apl")


tex = TLatex(21., 80, "#mu#tau")
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

h_et = TGraph(6, pt_e, sig_lum_e)
h_et.SetMarkerStyle(20)
h_et.SetLineStyle(2)
h_et.SetLineWidth(2)

h_et.GetXaxis().SetLabelSize(0.04)
h_et.GetYaxis().SetLabelSize(0.04)

h_et.GetXaxis().SetTitleSize(0.05)
h_et.GetXaxis().SetTitleOffset(1.2)
h_et.GetXaxis().SetNdivisions(508)
h_et.GetXaxis().SetTitle('electron p_{T} (GeV)')

h_et.GetYaxis().SetTitleSize(0.05)
h_et.GetYaxis().SetTitleOffset(1.2)
h_et.GetYaxis().SetNdivisions(509)
h_et.GetYaxis().SetTitle('gain in effective luminosity (%)')

h_et.SetMaximum(100)
h_et.SetMinimum(-10)
h_et.Draw("apl")


etex = TLatex(24., 80, "e#tau")
etex.SetTextSize(0.07)
etex.SetLineWidth(2)
etex.Draw()

canvas.SaveAs('luminosity_gain_mt.eps')
ecanvas.SaveAs('luminosity_gain_et.eps')
