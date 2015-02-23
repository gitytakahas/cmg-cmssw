from ROOT import TFile, TTree, gROOT
import os
from Display import *
from officialStyle import officialStyle
import numpy as num

gROOT.SetBatch(True)

file = TFile("Myroot.root")
tree = file.Get("tree")
entries = tree.GetEntriesFast()

output = TFile('output.root','recreate')
ptree = ROOT.TTree('photon','photon') 
etree = ROOT.TTree('event','event') 

last_seed = num.zeros(1, dtype=int)
last_seed_process = num.zeros(1, dtype=int)
last_seed_pt = num.zeros(1, dtype=float)
last_seed_r = num.zeros(1, dtype=float)
isHad = num.zeros(1, dtype=int)
isBrem = num.zeros(1, dtype=int)
isConv = num.zeros(1, dtype=int)
isDecay = num.zeros(1, dtype=int)
isIon = num.zeros(1, dtype=int)
isPrim = num.zeros(1, dtype=int)
isHad_minR = num.zeros(1, dtype=float)

ptree.Branch('last_seed', last_seed, 'last_seed/I')
ptree.Branch('last_seed_process', last_seed_process, 'last_seed_process/I') 
ptree.Branch('last_seed_pt', last_seed_pt, 'last_seed_pt/D')
ptree.Branch('last_seed_r', last_seed_r, 'last_seed_r/D') 
etree.Branch('isHad', isHad, 'isHad/I')
etree.Branch('isBrem', isBrem, 'isBrem/I')
etree.Branch('isConv', isConv, 'isConv/I')
etree.Branch('isDecay', isDecay, 'isDecay/I')
etree.Branch('isIon', isIon, 'isIon/I') 
etree.Branch('isPrim', isPrim, 'isPrim/I') 
etree.Branch('isHad_minR', isHad_minR, 'isHad_minR/D') 


for jentry in xrange(entries):

    ientry = tree.LoadTree(jentry)
    if ientry < 0: break

    nb = tree.GetEntry(jentry)
    if nb <= 0: continue

    if tree.ncluster!=1: continue
    if len(tree.history_pdgid) ==0: continue

    gcounter = tree.gamma_global_counter
    pcounter = tree.gamma_photon_counter


    if pcounter==0:
        if gcounter!=0:
#            print 'isHadronic = ', display.isHadronic
            isHad[0] = display.isHadronic
            isHad_minR[0] = 999.

            if display.isHadronic == False and display.isBrem == False and display.isConv == False and display.isDecay == False and display.isIon == False:
                isPrim[0] = 1
            else:
                isPrim[0] = 0

            isBrem[0] = display.isBrem
            isConv[0] = display.isConv
            isDecay[0] = display.isDecay
            isIon[0] = display.isIon
                
            print gcounter, ', isPrimary = ', isPrim[0]

            if display.isHadronic:
                isHad_minR[0] = min(display.isHadronicR)

            etree.Fill()

            if gcounter < 200:
                display.viewEtaPhi(str(gcounter)) # save to the file

        display = DisplayManager('display' + str(gcounter))

        
    display.addPoint(tree.history_pdgid, tree.history_pt, tree.history_processtype, tree.history_r, pcounter, gcounter)
 
#    print tree.history_pdgid[-1], returnPDG(tree.history_pdgid[-1])
#    print 'Final = ', tree.history_pdgid[-1], tree.history_pt[-1]
    last_seed[0] = returnPDG(tree.history_pdgid[-1])
    last_seed_process[0] = tree.history_processtype[-1]
    last_seed_pt[0] = tree.history_pt[-1]
    last_seed_r[0] = tree.history_r[-1]
    ptree.Fill()

output.Write()
output.Close()

