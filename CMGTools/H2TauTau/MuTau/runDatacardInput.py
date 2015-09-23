import subprocess
import os
import time
import sys

processes = set()
max_processes = 4

catsSM = []


catsSM = {
#        'Xcat_IncX && mt<30 && Xcat_J0_mediumX':'0jet_medium',
#        'Xcat_IncX && mt<30 && Xcat_J0_highX':'0jet_high',
#        'Xcat_IncX && mt<30 && Xcat_J1_mediumX':'1jet_medium',
#        'Xcat_IncX && mt<30 && Xcat_J1_high_mediumhiggsX':'1jet_high_mediumhiggs',
#        'Xcat_IncX && mt<30 && Xcat_J1_high_lowhiggsX':'1jet_high_lowhiggs',
#        'Xcat_IncX && mt<30 && Xcat_VBF_looseX':'vbf_loose',
        'Xcat_IncX && mt<30 && nJets>=2 && nBJets == 0 && sqrt(VBF_deta**2 + VBF_jdphi**2) > 0.6 && VBF_mjj > 200 && pthiggs > 70':'vbf_tight',
}

base = '/data1/ytakahas/H2tautau_data/sample_20140329'

dirUp = base + '/20140329_tes_Up/'
dirDown = base + '/20140329_tes_Down/'

dirNom = base + '/20140329_nominal/'
dirGGH = base + '/20140329_nominal/'

embedded = True

embOpt = ''
if embedded:
    embOpt = '-E'

#weightOpt = 'weight*tauTriggerOldWeight_' + str(pt2) + '/tauTriggerWeight'
#weightOpt_up = 'weight*tauTriggerOldWeight_' + str(pt2) + '*hqtWeightUp/(hqtWeight*tauTriggerWeight)'
#weightOpt_down = 'weight*tauTriggerOldWeight_' + str(pt2) + '*hqtWeightDown/(hqtWeight*tauTriggerWeight)'

weightOpt = 'weight'
weightOpt_up = 'weight*hqtWeightUp/(hqtWeight)'
weightOpt_down = 'weight*hqtWeightDown/(hqtWeight)'


allArgs = []
for cat in catsSM:
#    args = ['python', 'plot_H2TauTauDataMC_TauMu_All.py', dirNom, 'tauMu_2015_cfg.py', '-C', cat, '-H', 'svfitMass', '-w', weightOpt, '-b', embOpt]
#    args = ['python', 'plot_H2TauTauDataMC_TauMu_All.py', dirNom, 'tauMu_2012_cfg.py', '-C', cat, '-H', 'VBF_jdphi', '-w', weightOpt, '-b', embOpt]
    args = ['python', 'plot_H2TauTauDataMC_TauMu_All.py', dirNom, 'tauMu_2012_cfg.py', '-C', cat, '-H', 'VBF_jdphi', '-w', weightOpt, '-b', '-n', '15', '-M', '3.1415', '-m', '-3.1415']
#    args = ['python', 'plot_H2TauTauDataMC_TauMu_All.py', dirNom, 'tauMu_2012_cfg.py', '-C', cat, '-H', 'svfitMass', '-w', weightOpt, '-b']
#    args = ['python', 'plot_H2TauTauDataMC_TauMu_All.py', dirNom, 'tauMu_2015_cfg.py', '-C', cat, '-H', 'jet1_phi-jet2_phi', '-w', weightOpt, '-b']

    argsUp = ['python', 'plot_H2TauTauMC.py', dirUp, 'tauMu_2012_tesup_cfg.py', '-C', cat, '-H', 'VBF_jdphi', '-w', weightOpt, '-b',  '-n', '15', '-M', '3.1415', '-m', '-3.1415', embOpt, '-f', 'Higgs;Ztt']
    argsDown = ['python', 'plot_H2TauTauMC.py', dirDown, 'tauMu_2012_tesdown_cfg.py', '-C', cat, '-H', 'VBF_jdphi', '-w', weightOpt, '-b',  '-n', '15', '-M', '3.1415', '-m', '-3.1415', embOpt, '-f', 'Higgs;Ztt']

#    argsUp = ['python', 'plot_H2TauTauMC.py', dirUp, 'tauMu_2015_tesup_cfg.py', '-C', cat, '-H', 'VBF_jdphi', '-w', weightOpt, '-b', '-f', 'Higgs;Ztt']
#    argsDown = ['python', 'plot_H2TauTauMC.py', dirDown, 'tauMu_2015_tesdown_cfg.py', '-C', cat, '-H', 'VBF_jdphi', '-w', weightOpt, '-b', '-f', 'Higgs;Ztt']

    argsGGHUp = ['python', 'plot_H2TauTauMC.py', dirGGH, 'tauMu_2012_cfg.py', '-C', cat, '-H', 'VBF_jdphi', '-b',  '-n', '15', '-M', '3.1415', '-m', '-3.1415', '-f', 'HiggsGGH', '-w', weightOpt_up, '-s', 'QCDscale_ggH1inUp']
    argsGGHDown = ['python', 'plot_H2TauTauMC.py', dirGGH, 'tauMu_2012_cfg.py', '-C', cat, '-H', 'VBF_jdphi', '-b',  '-n', '15', '-M', '3.1415', '-m', '-3.1415',  '-f', 'HiggsGGH', '-w', weightOpt_down, '-s', 'QCDscale_ggH1inDown']

    argsZLUp = ['python', 'plot_H2TauTauMC.py', dirNom, 'tauMu_2012_cfg.py', '-C', cat, '-H', 'VBF_jdphi*1.02', '-b',  '-n', '15', '-M', '3.1415', '-m', '-3.1415',  '-f', 'Ztt', '-w', weightOpt, '-s', 'CMS_htt_ZLScale_mutau_8TeVUp']
    argsZLDown = ['python', 'plot_H2TauTauMC.py', dirNom, 'tauMu_2012_cfg.py', '-C', cat, '-H', 'VBF_jdphi*0.98', '-b',  '-n', '15', '-M', '3.1415', '-m', '-3.1415',  '-f', 'Ztt', '-w', weightOpt, '-s', 'CMS_htt_ZLScale_mutau_8TeVDown']

    argsWJetsUp = ['python', 'plot_H2TauTauDataMC_TauMu_All.py', dirNom, 'tauMu_2012_cfg.py', '-C', cat, '-H', 'VBF_jdphi',  '-w', weightOpt, '-b',  '-n', '15', '-M', '3.1415', '-m', '-3.1415',  '-s', 'CMS_htt_WShape_mutau_{cat}_8TeVUp'.format(cat=catsSM[cat])]
    argsWJetsDown = ['python', 'plot_H2TauTauDataMC_TauMu_All.py', dirNom, 'tauMu_2012_cfg.py', '-C', cat, '-H', 'VBF_jdphi',  '-w', weightOpt, '-b',  '-n', '15', '-M', '3.1415', '-m', '-3.1415',  '-s', 'CMS_htt_WShape_mutau_{cat}_8TeVDown'.format(cat=catsSM[cat])]

#    allArgs += [args, argsUp, argsDown, argsGGHUp, argsGGHDown, argsZLUp, argsZLDown, argsWJetsUp, argsWJetsDown]
#    allArgs += [argsWJetsUp, argsWJetsDown]
#    allArgs += [args, argsUp, argsDown, argsGGHUp, argsGGHDown, argsZLUp, argsZLDown]
#    allArgs += [args]
    allArgs += [args, argsUp, argsDown, argsGGHUp, argsGGHDown, argsZLUp, argsZLDown, argsWJetsUp, argsWJetsDown]

#    allArgs += [args]


printOnly = False

if printOnly:
    for args in allArgs:
        for arg in args:
            print arg,
        print 
    

            
else:
    for args in allArgs:
        processes.add(subprocess.Popen(args))
        if len(processes) >= max_processes:
            os.wait()
            processes.difference_update(
                p for p in processes if p.poll() is not None)


#Check if all the child processes were closed
    for p in processes:
        if p.poll() is None:
            p.wait()
            # os.wait()

