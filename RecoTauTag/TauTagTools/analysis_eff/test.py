from officialStyle import officialStyle
from basic import *
from array import array
import ROOT, shelve
import numpy as num

gROOT.SetBatch(True)
officialStyle(gStyle)
gStyle.SetOptTitle(1)
set_palette("color")
#gStyle.SetPaintTextFormat("2.2f")
gStyle.SetPaintTextFormat("2.0f")
gStyle.SetTitleX(0.4)

if __name__ == '__main__':

    file = TFile('output.root', 'recreate')
    tree = ROOT.TTree('tree','tree')

    tau_pt_old = num.zeros(1, dtype=float)
    tau_eta_old = num.zeros(1, dtype=float)
    tau_ciso_old = num.zeros(1, dtype=float)
    tau_nwiso_old = num.zeros(1, dtype=float)

    tau_pt_new = num.zeros(1, dtype=float)
    tau_eta_new = num.zeros(1, dtype=float)
    tau_ciso_new = num.zeros(1, dtype=float)
    tau_nwiso_new = num.zeros(1, dtype=float)

    tree.Branch('tau_pt_old', tau_pt_old, 'tau_pt_old/D')
    tree.Branch('tau_eta_old', tau_eta_old, 'tau_eta_old/D')
    tree.Branch('tau_ciso_old', tau_ciso_old, 'tau_ciso_old/D')
    tree.Branch('tau_nwiso_old', tau_nwiso_old, 'tau_nwiso_old/D')
    
    tree.Branch('tau_pt_new', tau_pt_new, 'tau_pt_new/D')
    tree.Branch('tau_eta_new', tau_eta_new, 'tau_eta_new/D')
    tree.Branch('tau_ciso_new', tau_ciso_new, 'tau_ciso_new/D')
    tree.Branch('tau_nwiso_new', tau_nwiso_new, 'tau_nwiso_new/D')




    hcor = TH2F('hcor', 'hcor', 13,0,13,13,0,13)    
    hgcor =  TH2F('hgcor', 'hgcor', 5,0,5,5,0,5)

    s_dynamic = shelve.open('save_dynamic95.db')
    s_standard = shelve.open('save_run1.db')
#    s_dynamic = shelve.open('save_standard.db')

#    print 'check', s_dynamic, s_standard
    for key, value in s_dynamic.iteritems():

        if not (value['taupt'] > 20 and abs(value['taueta'])<2.3): continue

#        if value['nweight'] > 2: continue

#        print key, value
#        print s_standard
        if s_standard.has_key(key):
            value_standard = s_standard[key]
            
            print 'matching !'
    
#            if value_standard['nweight'] < 2:
            hcor.Fill(value['taudm'], value_standard['taudm'])
#            else:
#                hcor.Fill(value['taudm'], 12)

            if not (value_standard['taupt'] > 20 and abs(value_standard['taueta'])<2.3): continue

            tau_pt_new[0] = value['taupt']
            tau_eta_new[0] = value['taueta']
            tau_ciso_new[0] = value['ciso']
            tau_nwiso_new[0] = value['nweight']

            tau_pt_old[0] = value_standard['taupt']
            tau_eta_old[0] = value_standard['taueta']
            tau_ciso_old[0] = value_standard['ciso']
            tau_nwiso_old[0] = value_standard['nweight']
            tree.Fill()

        else:
            hcor.Fill(value['taudm'], 12)


    for key, value in s_standard.iteritems():

        if not (value['taupt'] > 20 and abs(value['taueta'])<2.3): continue        
#        if value['nweight'] > 2: continue
        
        if s_dynamic.has_key(key):
            pass
        else:
            hcor.Fill(12, value['taudm'])



    cnt_1p = 0
    cnt_1pp = 0
    cnt_2p = 0
    cnt_3p = 0
    cnt_unk = 0

    for ii in range(1, hcor.GetYaxis().GetNbins()+1):
        ent = hcor.GetBinContent(1, ii)
        if ii==1: cnt_1p += ent
        elif ii in [2, 3]: cnt_1pp += ent
        elif ii in [6, 7]: cnt_2p += ent
        elif ii==11 : cnt_3p += ent
        elif ii==13 : cnt_unk += ent


    hgcor.SetBinContent(1,1,cnt_1p)
    hgcor.SetBinContent(1,2,cnt_1pp)
    hgcor.SetBinContent(1,3,cnt_2p)
    hgcor.SetBinContent(1,4,cnt_3p)
    hgcor.SetBinContent(1,5,cnt_unk)


    cnt_1p = 0
    cnt_1pp = 0
    cnt_2p = 0
    cnt_3p = 0
    cnt_unk = 0

    for ix in range(2, 4):
        for ii in range(1, hcor.GetYaxis().GetNbins()+1):
            ent = hcor.GetBinContent(ix, ii)
            if ii==1: cnt_1p += ent
            elif ii in [2, 3]: cnt_1pp += ent
            elif ii in [6, 7]: cnt_2p += ent
            elif ii==11 : cnt_3p += ent
            elif ii==13 : cnt_unk += ent



    hgcor.SetBinContent(2,1,cnt_1p)
    hgcor.SetBinContent(2,2,cnt_1pp)
    hgcor.SetBinContent(2,3,cnt_2p)
    hgcor.SetBinContent(2,4,cnt_3p)
    hgcor.SetBinContent(2,5,cnt_unk)


    cnt_1p = 0
    cnt_1pp = 0
    cnt_2p = 0
    cnt_3p = 0
    cnt_unk = 0

    for ix in range(6, 8):
        for ii in range(1, hcor.GetYaxis().GetNbins()+1):
            ent = hcor.GetBinContent(ix, ii)
            if ii==1: cnt_1p += ent
            elif ii in [2, 3]: cnt_1pp += ent
            elif ii in [6, 7]: cnt_2p += ent
            elif ii==11 : cnt_3p += ent
            elif ii==13 : cnt_unk += ent



    hgcor.SetBinContent(3,1,cnt_1p)
    hgcor.SetBinContent(3,2,cnt_1pp)
    hgcor.SetBinContent(3,3,cnt_2p)
    hgcor.SetBinContent(3,4,cnt_3p)
    hgcor.SetBinContent(3,5,cnt_unk)


    cnt_1p = 0
    cnt_1pp = 0
    cnt_2p = 0
    cnt_3p = 0
    cnt_unk = 0

    for ii in range(1, hcor.GetYaxis().GetNbins()+1):
        if ii==1: cnt_1p += hcor.GetBinContent(11, ii)
        elif ii in [2, 3]: cnt_1pp += hcor.GetBinContent(11, ii)
        elif ii in [6, 7]: cnt_2p += hcor.GetBinContent(11, ii)
        elif ii==11 : cnt_3p += hcor.GetBinContent(11, ii)
        elif ii==13 : cnt_unk += hcor.GetBinContent(11, ii)


    hgcor.SetBinContent(4,1,cnt_1p)
    hgcor.SetBinContent(4,2,cnt_1pp)
    hgcor.SetBinContent(4,3,cnt_2p)
    hgcor.SetBinContent(4,4,cnt_3p)
    hgcor.SetBinContent(4,5,cnt_unk)


    cnt_1p = 0
    cnt_1pp = 0
    cnt_2p = 0
    cnt_3p = 0
    cnt_unk = 0

    for ii in range(1, hcor.GetYaxis().GetNbins()+1):
        if ii==1: cnt_1p += hcor.GetBinContent(13, ii)
        elif ii in [2, 3]: cnt_1pp += hcor.GetBinContent(13, ii)
        elif ii in [6, 7]: cnt_2p += hcor.GetBinContent(13, ii)
        elif ii==11 : cnt_3p += hcor.GetBinContent(13, ii)
        elif ii==13 : cnt_unk += hcor.GetBinContent(13, ii)


    hgcor.SetBinContent(5,1,cnt_1p)
    hgcor.SetBinContent(5,2,cnt_1pp)
    hgcor.SetBinContent(5,3,cnt_2p)
    hgcor.SetBinContent(5,4,cnt_3p)
    hgcor.SetBinContent(5,5,cnt_unk)

    hgcor.GetXaxis().SetTitle('Dynamic reco. : #tau_{h} mode')
    hgcor.GetYaxis().SetTitle('Run-1 reco. : #tau_{h} mode')

#    hgcor.GetXaxis().SetTitle('no pT cut. : #tau_{h} mode')
#    hgcor.GetYaxis().SetTitle('run-1 reco. : #tau_{h} mode')

    hgcor.GetXaxis().SetBinLabel(1, '#pi')
    hgcor.GetXaxis().SetBinLabel(2, '#pi#pi^{0}s')
    hgcor.GetXaxis().SetBinLabel(3, '2#pi#pi^{0}s')
    hgcor.GetXaxis().SetBinLabel(4, '#pi#pi#pi')
    hgcor.GetXaxis().SetBinLabel(5, 'N/A')

    hgcor.GetYaxis().SetBinLabel(1, '#pi')
    hgcor.GetYaxis().SetBinLabel(2, '#pi#pi^{0}s')
    hgcor.GetYaxis().SetBinLabel(3, '2#pi#pi^{0}s')
    hgcor.GetYaxis().SetBinLabel(4, '#pi#pi#pi')
    hgcor.GetYaxis().SetBinLabel(5, 'N/A')

#    title = 'nIso (weight) < 2'
    title = ''

    hgcor.SetTitle(title)
    hgcor.SetMarkerSize(2.3)

    ce = TCanvas('correlation')
    hgcor.Draw("colztext")

    ce.SaveAs("cor.gif")


    c = TCanvas('correlation_raw')
    hcor.Draw("colztext")

    c.SaveAs("cor_raw.gif")
    
    file.Write()
    file.Close()
