from officialStyle import officialStyle
from basic import *
from array import array
from ROOT import Double, THStack, TH1D
import copy

#gROOT.SetBatch(True)
officialStyle(gStyle)
gStyle.SetOptTitle(0)
set_palette("color")

gStyle.SetPadLeftMargin(0.18)
gStyle.SetPadRightMargin(0.1)


basic = 'event_tau_niso !=0'

isHadBase = basic + '&& event_isHad == 1 && event_isEarlyShower==0'
isHad = basic + '&& event_isHad == 1 && event_isEarlyShower==0 && event_isConv==0'
isPrim = basic + '&& event_isHad == 0 && event_isEarlyShower==1 && event_isConv==0'
isConv = basic + '&& event_isConv==1 && event_isHad == 0 && event_isEarlyShower==0'
isConvHad = basic + '&& event_isConv==1 && event_isHad == 1 && event_isEarlyShower==0'

inc = '((' + isHad + ') || (' + isPrim +  ') || (' + isConv +  ') || (' + isConvHad +  '))'

print inc

def createProfile(hist, ispt='pt'):

    if ispt=='pt':
        binning = [20,40,60,80,100,120,140,160,180,200,250,300,350,500]
        _hist1d_ = TH1D(hist.GetName()+'_px', hist.GetName()+'_px', len(binning)-1, array('d',binning)) 
    else:
        _hist1d_ = TH1D(hist.GetName()+'_px', hist.GetName()+'_px', hist.GetXaxis().GetNbins(), hist.GetXaxis().GetXmin(), hist.GetXaxis().GetXmax())


    for xbin in range(1, hist.GetXaxis().GetNbins()+1):
        hh = hist.ProjectionY("proj" + str(xbin), xbin, xbin)

        if hh.GetEntries() == 0: continue

        _hist1d_.SetBinContent(xbin, hh.GetMean())
        _hist1d_.SetBinError(xbin, hh.GetMeanError())

    return _hist1d_

def makeEffPlotsVars(tree, varx, vary, sel, nbiny, ymin, ymax, xtitle, ytitle, leglabel = None, header='', ispt = 'pt'):
   
    c = TCanvas()

    hname = 'h_effp_' + header

    if ispt == 'pt':
        binning = [20,40,60,80,100,120,140,160,180,200,250,300,350,500]
        _hist_ = TH2F(hname, hname, len(binning)-1, array('d',binning), nbiny, ymin, ymax)
    elif ispt == 'eta':
        _hist_ = TH2F(hname, hname, 20,-2.5,2.5, nbiny, ymin, ymax)

    dname = vary + ':' + varx + ' >> ' + _hist_.GetName()
    tree.Draw(dname, sel)

    total = Double(tree.GetEntries(inc + '&&' + sel))
    frac = Double(tree.GetEntries(inc + '&&' + sel + '&&' + vary))

    if ispt=='pt':
        print '='*60
        print hname, 'fraction = ', Double(frac/total)

    hist = createProfile(_hist_, ispt)
#    hist = _hist_.ProfileX()
#    hist.Sumw2()

 #   hist.GetXaxis().SetTitle(xtitle)
 #   hist.GetYaxis().SetTitle(ytitle)
#    hist.GetYaxis().SetNdivisions(507)
 #   hist.SetLineWidth(3)
 #   hist.GetYaxis().SetTitleOffset(1.3)
    hist.SetMinimum(0.)

#     leg = TLegend(0.1,0.93,0.5,0.99)
#     LegendSettings(leg,1)

#     if leglabel != None:
#         if leglabel=='1p0pi0': leglabel = '#pi'
#         elif leglabel == '1p1pi0': leglabel = '#pi#pi^{0}s'
#         elif leglabel == '3p0pi0': leglabel = '#pi#pi#pi'

#         leg.AddEntry(hist, leglabel, "")
#         leg.Draw()


# #    save(c, 'plots_fraction/' + header)


    return copy.deepcopy(hist)


def overlay(hists, header, xtitle, ytitle):


    canvas = TCanvas()
    leg = TLegend(0.22,0.67,0.5,0.9)
    LegendSettings(leg, 1)

    col = [1,2,4,6, 8]

    hs = []

    for ii, hist in enumerate(hists):

        if ii==0: continue

        hist.SetLineColor(col[ii])
        hist.SetFillStyle(3004)
        hist.SetFillColor(col[ii])
        hist.SetLineWidth(2)
        hist.SetMarkerSize(0)

#        hist.Sumw2()

        for ibin in range(1, hist.GetXaxis().GetNbins()+1):
            hist.SetBinError(ibin, 0.)

        hs.append(copy.deepcopy(hist))
#        hs.Add(copy.deepcopy(hist))


    h1 = hs[0]
    h2 = hs[1] + hs[0]
    h3 = hs[2] + hs[1] + hs[0]

    h_cmb = [h3, h2, h1]

    h4 = None
    
    if header.find('1prong1pi0')!=-1:
        h4 = hs[3] + hs[2] + hs[1] + hs[0]
        h_cmb = [h4, h3, h2, h1]
    
    for ii, hh in enumerate(h_cmb):
        hh.GetXaxis().SetTitle(xtitle)
        hh.GetYaxis().SetTitle(ytitle)
        hh.GetYaxis().SetTitleOffset(1.3)
        hh.SetMaximum(h_cmb[0].GetMaximum()*1.7)
        hh.SetMinimum(0)
        hh.SetLineWidth(2)
        hh.GetYaxis().SetNdivisions(507)
        if ii==0: hh.Draw('')
        else: hh.Draw('same')


#    hs.SetMaximum(2.*hs.GetMaximum())      
#    leg.AddEntry(hists[0], 'Total', 'f')
    leg.AddEntry(h1, 'Early shower', 'f')
    leg.AddEntry(h2, 'Conversion', 'f')
    leg.AddEntry(h3, 'Nuclear interaction', 'f')

    if header.find('1prong1pi0')!=-1:
        leg.AddEntry(h4, 'Nuclear interaction & Conv.', 'f')

#    print '-'*80
#    print 'Early shower:', hs[0].GetEntries(), h4.GetEntries()
#    print 'Conversion:', hs[1].GetEntries(), h4.GetEntries()
#    print 'Nuclear interaction:', hs[2].GetEntries(), h4.GetEntries()
#    print 'Nuclear interaction + conv:', hs[3].GetEntries(), h4.GetEntries()


    # print '-'*80
    # print header
    # print 'Total', hists[0].GetSumOfWeights()
    # print 'Tail', hists[1].GetSumOfWeights()/hists[0].GetSumOfWeights()
    # print 'Conv', hists[2].GetSumOfWeights()/hists[0].GetSumOfWeights()
    # print 'Nuc.', hists[3].GetSumOfWeights()/hists[0].GetSumOfWeights()
    # print 'Nuc. + Conv', hists[4].GetSumOfWeights()/hists[0].GetSumOfWeights()

#    hs.Draw('hs')
    leg.Draw()
    
    save(canvas, 'plots_fraction/' + header)


if __name__ == '__main__':

    nbin = 1200

    tfile = TFile('Myroot_allDecay.root')
    tree = tfile.Get('etree')

    # neutral Isolation vs tau pT

    vardict = {
        'niso_prob':{'var':inc, 'nbin':2, 'min':-0.5, 'max':1.5, 'title':'eff (nIso > 0 GeV)', 'save':'nIso_nonZero'},
        }

    tvardict = {
        'isHad_prob':{'var':isHad, 'nbin':2, 'min':-0.5, 'max':1.5, 'title':'Prob. of Hadronic scattering', 'save':'had'},
        'isPrim_prob':{'var':isPrim, 'nbin':2, 'min':-0.5, 'max':1.5, 'title':'Prob. of Early shower', 'save':'earlyshower'},
        'isConv_prob':{'var':isConv, 'nbin':2, 'min':-0.5, 'max':1.5, 'title':'Prob. of Conversion', 'save':'conversion'},
        'isConvHad_prob':{'var':isConvHad, 'nbin':2, 'min':-0.5, 'max':1.5, 'title':'Prob. of Nuc. and Conv.', 'save':'Conversion_Had'},
        }

    ddict = {
        'a':{'cut':'event_tau_gen_dm==0', 'label':'1prong', 'name':'1prong'},
        'b':{'cut':'(event_tau_gen_dm==1 || event_tau_gen_dm==2)', 'label':'1prong+#pi^{0}', 'name':'1prong1pi0'},
        'c':{'cut':'event_tau_gen_dm==10', 'label':'3prong', 'name':'3prong'},
        'd':{'cut':'(event_tau_gen_dm!=-1 && event_tau_gen_dm!=5 && event_tau_gen_dm!=6)', 'label':'Inclusive', 'name':'inclusive'}
        }

#    import pdb; pdb.set_trace()

    for dkey, dm in ddict.iteritems():
    
        hist_pt = []
        hist_eta = []
        
        for key, tool in vardict.iteritems():
            hist_pt.append(makeEffPlotsVars(tree, 'event_tau_gen_pt', tool['var'], dm['cut'], tool['nbin'], tool['min'], tool['max'], 'gen. tau p_{T} (GeV)', tool['title'], None, tool['save'] + '_pt_' + dm['name'], 'pt'))
            hist_eta.append(makeEffPlotsVars(tree, 'event_tau_gen_eta', tool['var'], dm['cut'], tool['nbin'], tool['min'], tool['max'], 'gen. tau #eta', tool['title'], None, tool['save'] + '_eta_' + dm['name'], 'eta'))
        
            
        for key, tool in tvardict.iteritems():
            
            if key=='isConvHad_prob' and (dkey=='a' or dkey=='c'): continue

            variable = tool['var']
            if key=='isHad_prob' and (dkey=='a' or dkey=='c'): 
                variable = isHadBase
            
            hist_pt.append(makeEffPlotsVars(tree, 'event_tau_gen_pt', variable, dm['cut'], tool['nbin'], tool['min'], tool['max'], 'gen. tau p_{T} (GeV)', tool['title'], None, tool['save'] + '_pt_' + dm['name'], 'pt'))
            hist_eta.append(makeEffPlotsVars(tree, 'event_tau_gen_eta', variable, dm['cut'], tool['nbin'], tool['min'], tool['max'], 'gen. tau #eta', tool['title'], None, tool['save'] + '_eta_' + dm['name'], 'eta'))
        


        overlay(hist_pt, 'all_pt_' + dm['name'], 'gen tau p_{T}^{vis} (GeV)', 'Probability having nIso > 0')
        overlay(hist_eta, 'all_eta_' + dm['name'], 'gen tau #eta^{vis}', 'Probability having nIso > 0')


