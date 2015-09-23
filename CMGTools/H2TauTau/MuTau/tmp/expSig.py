from ROOT import TFile, TH3F, gStyle, TH1F, TCanvas, gROOT, TGraph, kRed, TLegend
from officialStyle import officialStyle
import string

def LegendSettings(leg):
    leg.SetBorderSize(0)
    leg.SetFillColor(10)
    leg.SetLineColor(0)
    leg.SetFillStyle(0)
    leg.SetTextSize(0.035)
    leg.SetTextFont(42)


officialStyle(gStyle)
#gStyle.SetOptTitle(0)

graph = TGraph()
graph.SetPoint(0, 10, 2.65257)
graph.SetPoint(1, 19.7, 3.561)
graph.SetPoint(2, 50, 5.23294)

graph2 = TGraph()
graph2.SetPoint(0, 19.7, 2.21722)
graph2.SetMarkerStyle(20)
graph2.SetMarkerColor(kRed)
graph2.SetLineColor(kRed)

graph.SetMarkerStyle(20)
graph.GetXaxis().SetTitle('Luminosity (/fb)')
graph.GetYaxis().SetTitle('Expected Significance')
graph.GetYaxis().SetRangeUser(0, 6)
graph.Draw("alp")
graph2.Draw("psame")


leg = TLegend(0.7,0.3,0.3,0.5)
LegendSettings(leg)
leg.AddEntry(graph, "13TeV", "lp")
leg.AddEntry(graph2, "8TeV", "lp")
leg.Draw()
