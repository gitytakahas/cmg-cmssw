from ROOT import TFile, TTree, gROOT
import os
from Display import *
from officialStyle import officialStyle
import numpy as num

gROOT.SetBatch(True)

file = TFile("Myroot_allDecay.root")
tree = file.Get("tree")
entries = tree.GetEntriesFast()

output = TFile('output_allDecay.root','recreate')
ptree = ROOT.TTree('photon','photon') 
etree = ROOT.TTree('event','event')
dtree = ROOT.TTree('detail','detail')
gtree = ROOT.TTree('iso_gamma_detail','iso_gamma_detail') 

last_seed = num.zeros(1, dtype=int)
last_seed_process = num.zeros(1, dtype=int)
last_seed_pt = num.zeros(1, dtype=float)
last_seed_r = num.zeros(1, dtype=float)
isHad = num.zeros(1, dtype=int)
isNHad = num.zeros(1, dtype=int)
isN = num.zeros(1, dtype=int)
isBrem = num.zeros(1, dtype=int)
isConv = num.zeros(1, dtype=int)
isDecay = num.zeros(1, dtype=int)
isIon = num.zeros(1, dtype=int)
isPrim = num.zeros(1, dtype=int)
isConvOnly = num.zeros(1, dtype=int)
isConvPlusHad = num.zeros(1, dtype=int)
isHad_minR = num.zeros(1, dtype=float)
isConv_minR = num.zeros(1, dtype=float)
counter_global = num.zeros(1, dtype=int)
tau_genpt = num.zeros(1, dtype=float)
tau_geneta = num.zeros(1, dtype=float)
tau_pt = num.zeros(1, dtype=float)
tau_eta = num.zeros(1, dtype=float)

iso_gamma_pt = num.zeros(1, dtype=float)
iso_gamma_eta = num.zeros(1, dtype=float)
iso_gamma_phi = num.zeros(1, dtype=float)
iso_gamma_dR = num.zeros(1, dtype=float)
iso_gamma_isHad = num.zeros(1, dtype=int)
iso_gamma_isPrim = num.zeros(1, dtype=int)
iso_gamma_isConvHad = num.zeros(1, dtype=int)
iso_gamma_isConvOnly = num.zeros(1, dtype=int)

Had_R = num.zeros(1, dtype=float)
Had_R_eta = num.zeros(1, dtype=float)

ptree.Branch('last_seed', last_seed, 'last_seed/I')
ptree.Branch('last_seed_process', last_seed_process, 'last_seed_process/I') 
ptree.Branch('last_seed_pt', last_seed_pt, 'last_seed_pt/D')
ptree.Branch('last_seed_r', last_seed_r, 'last_seed_r/D') 

etree.Branch('isN', isN, 'isN/I')
etree.Branch('isHad', isHad, 'isHad/I')
etree.Branch('isNHad', isNHad, 'isNHad/I')
etree.Branch('isBrem', isBrem, 'isBrem/I')
etree.Branch('isConv', isConv, 'isConv/I')
etree.Branch('isDecay', isDecay, 'isDecay/I')
etree.Branch('isIon', isIon, 'isIon/I') 
etree.Branch('isPrim', isPrim, 'isPrim/I')
etree.Branch('isConvOnly', isConvOnly, 'isConvOnly/I')
etree.Branch('isConvPlusHad', isConvPlusHad, 'isConvPlusHad/I') 
etree.Branch('isHad_minR', isHad_minR, 'isHad_minR/D')
etree.Branch('isConv_minR', isConv_minR, 'isConv_minR/D')
etree.Branch('tau_genpt', tau_genpt, 'tau_genpt/D')
etree.Branch('tau_geneta', tau_geneta, 'tau_geneta/D')
etree.Branch('tau_pt', tau_pt, 'tau_pt/D')
etree.Branch('tau_eta', tau_eta, 'tau_eta/D')
etree.Branch('counter_global', counter_global, 'counter_global/I')

dtree.Branch('Had_R', Had_R, 'Had_R/D')
dtree.Branch('Had_R_eta', Had_R_eta, 'Had_R_eta/D')

gtree.Branch('iso_gamma_pt', iso_gamma_pt, 'iso_gamma_pt/D')
gtree.Branch('iso_gamma_eta', iso_gamma_eta, 'iso_gamma_eta/D')
gtree.Branch('iso_gamma_phi', iso_gamma_phi, 'iso_gamma_phi/D')
gtree.Branch('iso_gamma_dR', iso_gamma_dR, 'iso_gamma_dR/D')
gtree.Branch('iso_gamma_isHad', iso_gamma_isHad, 'iso_gamma_isHad/I')
gtree.Branch('iso_gamma_isPrim', iso_gamma_isPrim, 'iso_gamma_isPrim/I')
gtree.Branch('iso_gamma_isConvOnly', iso_gamma_isConvOnly, 'iso_gamma_isConvOnly/I')
gtree.Branch('iso_gamma_isConvHad', iso_gamma_isConvHad, 'iso_gamma_isConvHad/I')


save_gen_pt = -1.
save_gen_eta = -1.
save_pt = -1.
save_eta = -1.
save_phi = -1.

isFlag = False

for jentry in xrange(entries):

    ientry = tree.LoadTree(jentry)
    if ientry < 0: break

    nb = tree.GetEntry(jentry)
    if nb <= 0: continue

#    if jentry > 4000:
#        break


    gcounter = tree.gamma_global_counter
    pcounter = tree.gamma_photon_counter

#    if tree.gamma_nEcal!=1: 
#        print 'Number of cluster is not 1', tree.gamma_nECAL
#        continue

    if len(tree.history_pdgid) ==0: 
        print 'Number of history is 0'
        continue

    if not (tree.gen_dm == 1 and tree.tau_dm == 0): continue


    print 'evtcounter = ', tree.evtcounter
    print '\t photon pT = ', '{0:.2f}'.format(tree.gamma_pt), 
    print 'eta = ', '{0:.2f}'.format(tree.gamma_eta),
    print 'phi = ', '{0:.2f}'.format(tree.gamma_phi)

    if pcounter==0:
        if gcounter!=0 and isFlag==True:

            isHad[0] = display.isHadronic
            isHad_minR[0] = 999.
            isConv_minR[0] = 999.
            isN[0] = display.isN + 1

            nhad = []
            ntau = 0

            for key, value in display.particleDict.iteritems():
                for step, ivalue in value.iteritems():
                    if abs(ivalue['pdg']) == 15:
                        ntau += 1

                    if ivalue['ptype'] == 121:
                        if [ivalue['x0'], ivalue['y0']] not in nhad:
                            nhad.append([ivalue['x0'], ivalue['y0']])
                            Had_R[0] = ivalue['save_R']
                            Had_R_eta[0] = save_gen_eta

                            dtree.Fill()

            isNHad[0] = len(nhad)

#            print 'ntau = ', ntau, display.isDecay

            if display.isHadronic == False and display.isBrem == False and display.isConv == False and display.isDecay == False and display.isIon == False:
                isPrim[0] = 1
            elif ntau==1 and display.isHadronic == False and display.isBrem == False and display.isConv == False and display.isDecay == True and display.isIon == False:
#                print 'ntau = ', ntau
                isPrim[0] = 1
            else:
                isPrim[0] = 0

            if display.isHadronic == False  and display.isIon == False and display.isConv == True:
                isConvOnly[0] = 1
            else:
                isConvOnly[0] = 0
            
            if display.isHadronic == True and display.isConv == True:
                isConvPlusHad[0] = 1
            else:
                isConvPlusHad[0] = 0
            
            isBrem[0] = display.isBrem
            isConv[0] = display.isConv
            isDecay[0] = display.isDecay
            isIon[0] = display.isIon
            tau_genpt[0] = save_gen_pt
            tau_geneta[0] = save_gen_eta
            tau_pt[0] = save_pt
            tau_eta[0] = save_eta
#            counter_global[0] = gcounter-1
            counter_global[0] = save_evtid
                
#            print gcounter, ', isPrimary = ', isPrim[0]

            if display.isHadronic:
                isHad_minR[0] = min(display.isHadronicR)

            if display.isConv:
                isConv_minR[0] = min(display.isConvR)

            etree.Fill()

            _gamma_ = display.returnGamma()
            for igamma in _gamma_:
#                print igamma
                iso_gamma_pt[0] = igamma[0]
                iso_gamma_eta[0] = igamma[1]
                iso_gamma_phi[0] = igamma[2]
                iso_gamma_dR[0] = deltaR(igamma[1], igamma[2], save_eta, save_phi)
                iso_gamma_isHad[0] = display.isHadronic
                iso_gamma_isPrim[0] = isPrim[0]
                iso_gamma_isConvOnly[0] = isConvOnly[0]
                iso_gamma_isConvHad[0] = isConvPlusHad[0]
                gtree.Fill()


#            if gcounter < 1000:
            display.viewEtaPhi(str(save_evtid)) # save to the file

        display = DisplayManager('display', tree.gamma_total_iso, tree.gen_dm, tree.tau_dm)
        isFlag = True
        
    display.addPoint(tree.history_pdgid, tree.history_pt, tree.history_processtype, tree.history_r, pcounter, gcounter, tree.gamma_pt, tree.gamma_eta, tree.gamma_phi)
 
    last_seed[0] = returnPDG(tree.history_pdgid[-1])
    last_seed_process[0] = tree.history_processtype[-1]
    last_seed_pt[0] = tree.history_pt[-1]
    last_seed_r[0] = tree.history_r[-1]
    ptree.Fill()

    save_gen_pt = tree.tau_gen_pt
    save_gen_eta = tree.tau_gen_eta
    save_pt = tree.tau_pt
    save_eta = tree.tau_eta
    save_phi = tree.tau_phi
    save_evtid = tree.evtcounter

output.Write()
output.Close()

