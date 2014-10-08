import ROOT, copy

#filename = 'Fisher.root'
#filename = 'BDTG_f3train.root'
#filename = 'Fisher_newMVA.root'
#filename = 'BDTG_newMVA.root'
#filename = 'BDTG_newTauID.root'
#filename = 'Fisher_newTauID.root'

#filename = 'BDTG_1709.root'
#filename = 'Fisher_1709.root'
filename = 'Fisher_1809.root'

file_in = ROOT.TFile.Open(filename, 'read')
file_in.cd()

names = {}

if filename.find('Fisher')!=-1:
  names = {
    'FisherWZ'		:  'WZ',
    'FisherZZ'		:  'ZZ',
    'Fishertt1l'	:  'tt1l',
    'Fishertt2l'	:  'tt2l',
    'FisherttW'		:  'ttW',
    'FisherttZ'		:  'ttZ',
    'FishertH_YtMinus'	:  'tH_YtMinus125',
    'FisherttH'		:  'ttH',
    'Fisherreducible'	:  'reducible',
    'Fisherdata'	:  'data_obs',
    'FishersumMC'	:  'sumMC',
    }
elif filename.find('BDTG')!=-1:
  names = {
    'BDTGWZ'		:  'WZ',
    'BDTGZZ'		:  'ZZ',
    'BDTGtt1l'		:  'tt1l',
    'BDTGtt2l'		:  'tt2l',
    'BDTGttW'		:  'ttW',
    'BDTGttZ'		:  'ttZ',
    'BDTGtH_YtMinus'	:  'tH_YtMinus125',
    'BDTGttH'		:  'ttH',
    'BDTGreducible'	:  'reducible',
    'BDTGdata'		:  'data_obs',
    'BDTGsumMC'		:  'sumMC',
    }
  

  
hists = []

for key in file_in.GetListOfKeys() :
  hist = key.ReadObj()
  if hist.GetName() in names.keys() :
    if names[hist.GetName()] in [hh.GetName() for hh in hists] : continue
    hist.SetName(names[hist.GetName()])

    if hist.GetName() == 'tH_YtMinus125':
      print 'add trigger efficiency for the signal process', hist.GetName()
      hist.Scale(0.919)

    hist.SetMarkerStyle(9)
    hist.SetMarkerSize(1)
    hist.SetMarkerColor(ROOT.kBlack)
    hist.SetLineColor(ROOT.kBlack)
    hists.append(hist)

file_out = ROOT.TFile.Open('htt_th.inputs-sm-8TeV.root','recreate')
file_out.cd()
file_out.mkdir('emt')
file_out.cd('emt')
for hist in hists :
  hist.Write()

hist_data = copy.deepcopy(hists[0])
for a in range(1, hist_data.GetXaxis().GetNbins()+1):
  hist_data.SetBinContent(a, 0)
  hist_data.SetBinError(a, 0)

hist_data.SetName('data_obs')
hist_data.Write()
  
file_out.cd()
file_out.mkdir('mmt')
file_out.cd('mmt')
## dummy for the moment
for hist in hists :
  hist.Scale(0.00000001)
  hist.Write()

hist_data = copy.deepcopy(hists[0])
hist_w = copy.deepcopy(hists[0])
hist_dy = copy.deepcopy(hists[0])
hist_ww = copy.deepcopy(hists[0])
for a in range(1, hist_data.GetXaxis().GetNbins()+1):
  hist_data.SetBinContent(a, 0)
  hist_data.SetBinError(a, 0)
  hist_w.SetBinContent(a, 0)
  hist_w.SetBinError(a, 0)
  hist_dy.SetBinContent(a, 0)
  hist_dy.SetBinError(a, 0)
  hist_ww.SetBinContent(a, 0)
  hist_ww.SetBinError(a, 0)

hist_data.SetName('data_obs')
hist_data.Write()

hist_w.SetName('W')
hist_w.Write()

hist_dy.SetName('DY')
hist_dy.Write()

hist_ww.SetName('WW')
hist_ww.Write()

file_out.Close()

