import numpy
from ROOT import TH1F, TGraph, gStyle, TLegend, gSystem, TCanvas, kBlue, kRed, kGreen, TLatex

gStyle.SetOptTitle(0)

pt_mu = numpy.ndarray([6.])
sig_mu = numpy.ndarray([6.])

pt_old_mu = numpy.ndarray([1.])
sig_old_mu = numpy.ndarray([1.])

def LegendSettings(leg):
    leg.SetBorderSize(0)
    leg.SetFillColor(0)
    leg.SetLineColor(0)
    leg.SetFillStyle(0)
    leg.SetTextSize(0.04)
    leg.SetTextFont(42)


pt_old_mu[0] = 35.
sig_old_mu[0] = 1.625

pt_mu[0] = 25.
pt_mu[1] = 30.
pt_mu[2] = 35.
pt_mu[3] = 40.
pt_mu[4] = 50.
pt_mu[5] = 60.

sig_mu[0] = 1.51908
sig_mu[1] = 1.47873
sig_mu[2] = 1.43657
sig_mu[3] = 1.38527
sig_mu[4] = 1.26499
sig_mu[5] = 1.10662


canvas = TCanvas('c','c',640,640)
canvas.SetLeftMargin(0.14);
canvas.SetRightMargin(0.06);
canvas.SetTopMargin(0.075);
canvas.SetBottomMargin(0.12);
canvas.SetBorderSize(2);
canvas.SetFrameLineWidth(2);
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
h_mt.GetXaxis().SetTitle('L1 #tau p_{T} threshold (GeV)')

h_mt.GetYaxis().SetTitleSize(0.05)
h_mt.GetYaxis().SetTitleOffset(1.2)
h_mt.GetYaxis().SetNdivisions(508)
h_mt.GetYaxis().SetTitle('expected significance')

h_mt.SetMaximum(1.8)
h_mt.SetMinimum(0.9)
h_mt.Draw("apl")


h_mt_comb = TGraph(1, pt_old_mu, sig_old_mu)
h_mt_comb.SetMarkerStyle(20)
h_mt_comb.SetLineStyle(2)
h_mt_comb.SetMarkerColor(kBlue)
h_mt_comb.SetLineColor(kBlue)

h_mt_comb.SetLineWidth(2)
h_mt_comb.Draw("plsame")


leg = TLegend(0.6,0.68,0.9,0.86);
LegendSettings(leg)
leg.AddEntry(h_mt,'Run2 turnon','lp')
leg.AddEntry(h_mt_comb,'Run1 turnon','lp')
leg.Draw()

#tex = TLatex(21., 1.34, "#mu#tau")
#tex.SetTextSize(0.07)
#tex.SetLineWidth(2)
#tex.Draw()



canvas.SaveAs('significance_tt.gif')

