import os, numpy, math, copy, math, sys
from array import array
from ROOT import TLegend, TCanvas, TColor, kMagenta, kOrange, kRed, kBlue, kGray, kBlack, gROOT, gStyle, TFile, TH1F, TH2F, TLatex, TLine, TH1D
from officialStyle import officialStyle

gROOT.SetBatch(True)
officialStyle(gStyle)
gStyle.SetOptTitle(0)
gStyle.SetOptStat(0)
gStyle.SetPadRightMargin (0.13)

argvs = sys.argv
argc = len(argvs)

if argc != 2:
    print 'Please specify the runtype : python nIso.py <VBF, MSSM>'
    sys.exit(0)

runtype = argvs[1]

#runtype = 'VBF'
#runtype = 'MSSM'

binning = []

if runtype=='VBF':
#    binning = [20,30,40,50,60,70,80,90,100,120,150,300]
    binning = [20,40,60,80,100,300]
elif runtype == 'MSSM':
    binning = [20,60,100,150,200,300,600]


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
    ensureDir('plots_correction')
#    canvas.SaveAs(name.replace(' ','').replace('&&','')+'.pdf')
    canvas.SaveAs(name.replace(' ','').replace('&&','')+'.gif')


def FindEdge(hS, threshold=0.9):

    print threshold

    maxBin = hS.GetNbinsX()

    if hS.Integral() == 0.:
        print 'ROC curve creator, hist', hS.GetName(), 'has zero entries'
        return

#    effsS = [hS.Integral(0, nBin)/hS.Integral(0, maxBin+1) for nBin in range(0, maxBin + 1) ]
    effsS = [hS.Integral(0, nBin)/hS.GetSumOfWeights() for nBin in range(0, maxBin + 1) ]

    FindBin = -1

    for ii, ieff in enumerate(effsS):
        if ieff > threshold and FindBin==-1:
            FindBin = hS.GetBinCenter(ii+1)

    if FindBin == -1: print '!!! Find bin failed !!!'
    return FindBin
  


def createProfile(hist, threshold):

    print 'threshold =', threshold

    _hist1d_ = TH1D(hist.GetName()+'_px', hist.GetName()+'_px',len(binning)-1, array('d',binning))

    for xbin in range(1, hist.GetXaxis().GetNbins()+1):
        hh = hist.ProjectionY("proj" + str(xbin), xbin, xbin)

        if hh.GetEntries() == 0: continue

        val = FindEdge(hh, threshold)
        err = math.sqrt(threshold*(1-threshold)/hh.GetEntries())

        _hist1d_.SetBinContent(xbin, val)

        upper_edge = FindEdge(hh, threshold+err)
        lower_edge = FindEdge(hh, threshold-err)

        if upper_edge==-1 or lower_edge==-1: 
            print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
            continue

        errbar = (upper_edge + lower_edge)/2. - val
        _hist1d_.SetBinError(xbin, errbar)

    return _hist1d_



def makeEffPlotsVars(tree, varx, vary, sel, nbinx, xmin, xmax, nbiny, ymin, ymax, xtitle, ytitle, leglabel = None, header='', addon='', xx='pt'):
   
    c = TCanvas()

    _hist_ = TH2F('h_effp_' + addon, 'h_effp' + addon, len(binning)-1, array('d',binning), nbiny, ymin, ymax)

    dname = vary + ':' + varx + ' >> ' + _hist_.GetName()
    tree.Draw(dname, sel)

    hist = _hist_.ProfileX()

#    hist.Draw("lep")

    leg = TLegend(0.08,0.93,0.5,0.99)
    LegendSettings(leg, 1)

    if leglabel != None:
        leg.AddEntry(_hist_, leglabel.replace('pi0','#pi^{0}'), "")
        leg.Draw()

    leg2 = TLegend(0.8,0.93,0.9,0.99)
    LegendSettings(leg2, 1)
    leg2.AddEntry(_hist_, runtype, "")
    leg2.Draw()

    #### 90% envelope

    hist_edge = createProfile(_hist_, 0.85)
    hist_edge.GetYaxis().SetNdivisions(507)
    hist_edge.SetLineWidth(3)
    hist_edge.GetYaxis().SetTitleOffset(1.5)
    hist_edge.SetMaximum(hist_edge.GetMaximum()*2)
    hist_edge.SetMinimum(0)

    hist_edge.GetXaxis().SetTitle(xtitle)
    hist_edge.GetYaxis().SetTitle(ytitle)
    hist_edge.GetYaxis().SetNdivisions(507)


    hist_edge.Draw("pl")
    _hist_.Draw("colzsame")
#    _hist_.ProfileX().Draw("lepsame")
#    hist.Draw("axissame")
    hist_edge.Draw("plsame")


    save(c, 'plots_correction/' + header)


    
    

if __name__ == '__main__':

    filename = 'Myroot_dynamic95.root'
    
    if runtype == 'MSSM':
        filename = 'Myroot_mssm.root'


    hdict = {
        'dynamic':{'file':filename,'label':'Dynamic'},
        }

    ddict = {'1p0pi0':'tau_dm_rough==0', '1p1pi0':'tau_dm_rough==1', '2p':'(tau_dm==5 || tau_dm==6)', '3p':'tau_dm_rough==2'}
#    ddict = {'2p':'(tau_dm==5 || tau_dm==6)'}
#    ddict = {'1p0pi0':'tau_dm_rough==0'}
    
#    region = {'barrel':'abs(tau_eta) < 1.479', 'endcap':'abs(tau_eta) > 1.479', 'All eta':'1'}
    region = {'barrel':'abs(tau_eta) < 1.479', 'endcap':'abs(tau_eta) > 1.479'}
#    region = {'endcap':'abs(tau_eta) > 1.479'}
    
    valdict = {
        'nIso_weight_ciso_outer':{'tree':'per_tau',
                                  'var':'tau_niso_weighted', 
                                  'nbin':1000, 'xmin':0., 'xmax':50, 
                                  'title':'nIso weighted', 
                                  'sel':'tau_dm!=-1 && tau_ciso < 2 && (tau_photonsumpt_outside/tau_pt) < 0.2*tau_pt',
#                                  'sel':'tau_dm!=-1', 
                                  'name':'nIso_weight_ciso_outer'},
        }



    for vkey, ivar in valdict.iteritems():
        for rkey, rval in region.iteritems():
            for dkey, dm in ddict.iteritems():

                hists = []

                for key, val in sorted(hdict.iteritems()):
                
                    tfile = TFile(val['file'])
                    tree = tfile.Get(ivar['tree'])
                
                    makeEffPlotsVars(tree, 'tau_pt', ivar['var'], ivar['sel'] + ' && ' + dm + '&&' + rval, 20, 0, 300, ivar['nbin'], ivar['xmin'], ivar['xmax'], 'Tau pT (GeV)', ivar['title'], rkey + '_' + dkey + ', ' + val['label'], rkey + '_' + vkey + '_' + dkey + '_' + key + '_' + runtype, rkey + '_' + vkey + '_' + dkey + '_' + key + '_puiso', 'pt')



