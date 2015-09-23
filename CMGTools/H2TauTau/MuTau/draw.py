import os, numpy, math, copy, math
from array import array
from ROOT import TLegend, TCanvas, TColor, kMagenta, kOrange, kRed, kBlue, kGray, kBlack, gROOT, gStyle, TFile, TH1F, TH2F, TLatex, TLine
from officialStyle import officialStyle


def LegendSettings(leg):
    leg.SetBorderSize(0)
    leg.SetFillColor(10)
    leg.SetLineColor(0)
    leg.SetFillStyle(0)
    leg.SetTextSize(0.035)
    leg.SetTextFont(42)


def removeErrorbin(hist, flag=False):
    for ibin in range(1, hist.GetXaxis().GetNbins()+1):
        hist.SetBinError(ibin, 0)

    if flag:
        hist.SetFillColor(hist.GetMarkerColor())

#gROOT.SetBatch(True)
officialStyle(gStyle)
gStyle.SetOptTitle(0)
gStyle.SetOptStat(0)

col_qcd = TColor.GetColor(250,202,255)
col_tt  = TColor.GetColor(155,152,204)
col_ewk = TColor.GetColor(222,90,106)
col_zll = TColor.GetColor(100,182,232)
col_ztt = TColor.GetColor(248,206,104)


file = TFile("muTau_inclusive.root")

h_ggh = file.Get('ggH125')
h_tth = file.Get('TTH125')
h_qqh = file.Get('qqH125')
h_vh = file.Get('VH125')
h_qcd = file.Get('QCD')
h_tt = file.Get('TT')
h_vv = file.Get('VV')
h_w = file.Get('W')
h_ztt = file.Get('ZTT')
h_zj = file.Get('ZJ')
h_zl = file.Get('ZL')
h_zll = file.Get('ZLL')

h_higgs = copy.deepcopy(h_tth)
h_higgs.Add(h_qqh)
h_higgs.Add(h_vh)

h_higgs2 = copy.deepcopy(h_higgs)
h_higgs2.Add(h_ggh)

h_qcd.Add(h_vv)
h_qcd.Add(h_w)
h_qcd.Add(h_zj)
h_qcd.Add(h_zl)
h_qcd.Add(h_zll)

h_tt.Add(h_qcd)

h_ztt.Add(h_qcd)
h_ztt.Add(h_tt)

canvas = TCanvas()

h_ztt.SetMinimum(0)
h_ztt.SetMaximum(h_ztt.GetMaximum()*1.5)
h_ztt.GetXaxis().SetTitle('#Delta#phi(jj) rad')
h_ztt.GetYaxis().SetTitle('Number of events')

removeErrorbin(h_ztt)
removeErrorbin(h_tt)
removeErrorbin(h_qcd)


h_ztt.Draw()
h_tt.Draw("same")
h_qcd.Draw("same")

removeErrorbin(h_higgs, False)
h_higgs.Draw("same")

h_higgs2.SetLineColor(kRed)
h_higgs2.Draw("same")

leg = TLegend(0.7,0.8,0.9,0.9)
LegendSettings(leg)

leg.AddEntry(h_ztt, "Z", "f")
leg.AddEntry(h_tt, "ttbar", "f")
leg.AddEntry(h_qcd, "EWK", "f")
leg.AddEntry(h_higgs, "Higgs", "l")
leg.Draw()
