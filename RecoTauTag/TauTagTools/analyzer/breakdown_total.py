from officialStyle import officialStyle
from basic import *
from array import array
import ROOT

#gROOT.SetBatch(True)
officialStyle(gStyle)
gStyle.SetOptTitle(0)
set_palette("color")
gStyle.SetPaintTextFormat("2.2f")


if __name__ == '__main__':


    tfile = TFile('Myroot_allDecay.root')
    tree = tfile.Get('per_tau')
        
    hcor = TH2F('hcor', 'hcor', 12,0,12,12,0,12)
#    tree.Draw("tau_dm:tau_gendm >> hcor", 'tau_total_pt!=0 && tau_dm_rough!=-1' )
    tree.Draw("tau_dm:tau_gendm >> hcor", 'tau_dm_rough!=-1' )

    hgcor =  TH2F('hgcor', 'hgcor', 3,0,3,3,0,3)


    cnt_1p = 0
    cnt_1pp = 0
    cnt_3p = 0

    for ii in range(1, hcor.GetYaxis().GetNbins()+1):
        ent = hcor.GetBinContent(1, ii)
        if ii==1: cnt_1p += ent
        elif ii in [2, 3, 4, 5]: cnt_1pp += ent
        elif ii==11 : cnt_3p += ent


    hgcor.SetBinContent(1,1,cnt_1p)
    hgcor.SetBinContent(1,2,cnt_1pp)
    hgcor.SetBinContent(1,3,cnt_3p)


    cnt_1p = 0
    cnt_1pp = 0
    cnt_3p = 0

    for ix in range(2, 4):
        for ii in range(1, hcor.GetYaxis().GetNbins()):
            ent = hcor.GetBinContent(ix, ii)
            if ii==1: cnt_1p += ent
            elif ii in [2, 3, 4, 5]: cnt_1pp += ent
            elif ii==11 : cnt_3p += ent



    hgcor.SetBinContent(2,1,cnt_1p)
    hgcor.SetBinContent(2,2,cnt_1pp)
    hgcor.SetBinContent(2,3,cnt_3p)

    cnt_1p = 0
    cnt_1pp = 0
    cnt_3p = 0

    for ii in range(1, hcor.GetYaxis().GetNbins()):
        total = hcor.GetBinContent(11, ii)
        if ii==1: cnt_1p += hcor.GetBinContent(11, ii)
        elif ii in [2, 3, 4, 5]: cnt_1pp += hcor.GetBinContent(11, ii)
        elif ii==11 : cnt_3p += hcor.GetBinContent(11, ii)


    hgcor.SetBinContent(3,1,cnt_1p)
    hgcor.SetBinContent(3,2,cnt_1pp)
    hgcor.SetBinContent(3,3,cnt_3p)

    hgcor.GetXaxis().SetTitle('Generated #tau_{h} mode')
    hgcor.GetYaxis().SetTitle('Reconstructed #tau_{h} mode')
    hgcor.GetXaxis().SetBinLabel(1, '#pi')
    hgcor.GetXaxis().SetBinLabel(2, '#pi#pi^{0}s')
    hgcor.GetXaxis().SetBinLabel(3, '#pi#pi#pi')
    hgcor.GetYaxis().SetBinLabel(1, '#pi')
    hgcor.GetYaxis().SetBinLabel(2, '#pi#pi^{0}s')
    hgcor.GetYaxis().SetBinLabel(3, '#pi#pi#pi')
    hgcor.SetMarkerSize(2.3)

    ce = TCanvas('correlation')
    hgcor.DrawNormalized("text")
    ce.SaveAs("cor.gif")
    ce.SaveAs("cor.pdf")


    cc = TCanvas('correlation2')
    hgcor.Draw("text")
    cc.SaveAs("cor_abs.gif")
    cc.SaveAs("cor_abs.pdf")

