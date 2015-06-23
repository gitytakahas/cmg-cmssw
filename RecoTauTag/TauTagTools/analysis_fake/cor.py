from array import array
import ROOT, shelve
import numpy as num

#ROOT.gROOT.SetBatch(True)

s_dynamic = shelve.open('save_dynamic95.db')
s_standard = shelve.open('save_standard.db')

file = ROOT.TFile('output.root', 'recreate')
tree = ROOT.TTree('tree','tree')

ispTeta = num.zeros(1, dtype=int)
ispT = num.zeros(1, dtype=int)
iseta = num.zeros(1, dtype=int)
iscIso = num.zeros(1, dtype=int)
isnIso = num.zeros(1, dtype=int)
isdm = num.zeros(1, dtype=int)
d2s = num.zeros(1, dtype=int)

pt_standard = num.zeros(1, dtype=float)
eta_standard = num.zeros(1, dtype=float)
ciso_standard = num.zeros(1, dtype=float)
niso_standard = num.zeros(1, dtype=float)
dm_standard = num.zeros(1, dtype=int)

pt_dynamic = num.zeros(1, dtype=float)
eta_dynamic = num.zeros(1, dtype=float)
ciso_dynamic = num.zeros(1, dtype=float)
niso_dynamic = num.zeros(1, dtype=float)
dm_dynamic = num.zeros(1, dtype=int)

tree.Branch('ispTeta', ispTeta, 'ispTeta/I')
tree.Branch('ispT', ispT, 'ispT/I')
tree.Branch('iseta', iseta, 'iseta/I')
tree.Branch('iscIso', iscIso, 'iscIso/I')
tree.Branch('isnIso', isnIso, 'isnIso/I')
tree.Branch('isdm', isdm, 'isdm/I')
tree.Branch('d2s', d2s, 'd2s/I')

tree.Branch('pt_standard', pt_standard, 'pt_standard/D')
tree.Branch('eta_standard', eta_standard, 'eta_standard/D')
tree.Branch('ciso_standard', ciso_standard, 'ciso_standard/D')
tree.Branch('niso_standard', niso_standard, 'niso_standard/D')
tree.Branch('dm_standard', dm_standard, 'dm_standard/I')

tree.Branch('pt_dynamic', pt_dynamic, 'pt_dynamic/D')
tree.Branch('eta_dynamic', eta_dynamic, 'eta_dynamic/D')
tree.Branch('ciso_dynamic', ciso_dynamic, 'ciso_dynamic/D')
tree.Branch('niso_dynamic', niso_dynamic, 'niso_dynamic/D')
tree.Branch('dm_dynamic', dm_dynamic, 'dm_dynamic/I')

#import pdb; pdb.set_trace()
print len(s_dynamic), len(s_standard)

for key, value_dynamic in s_dynamic.iteritems():
    
    if s_standard.has_key(key):
        value_standard = s_standard[key]
        
        d_tau_pt = value_dynamic['taupt']
        d_tau_eta = value_dynamic['taueta']
        d_tau_ciso = value_dynamic['ciso']
        d_tau_niso = value_dynamic['nweight']
        d_tau_dm = value_dynamic['taudm']
        
        s_tau_pt = value_standard['taupt']
        s_tau_eta = value_standard['taueta']
        s_tau_ciso = value_standard['ciso']
        s_tau_niso = value_standard['nweight']
        s_tau_dm = value_standard['taudm']

        if d_tau_pt > 20 and abs(d_tau_eta) < 2.3 and d_tau_ciso < 2 and d_tau_niso < 2 and d_tau_dm!=-1:

            print 'basic selection passed !'
            print 'dynamic :', d_tau_pt, d_tau_eta, d_tau_ciso, d_tau_niso, d_tau_dm
            print 'standard : ', s_tau_pt, s_tau_eta, s_tau_ciso, s_tau_niso, s_tau_dm
            print '-'*80

            if not (s_tau_pt > 20 and abs(s_tau_eta) < 2.3 and s_tau_ciso < 2 and s_tau_niso < 2 and s_tau_dm!=-1):
            
                print 'pass !'

                ispTeta[0] = not (s_tau_pt > 20 and abs(s_tau_eta) < 2.3)
                ispT[0] = not (s_tau_pt > 20)
                iseta[0] = not (abs(s_tau_eta) < 2.3)
                iscIso[0] = not (s_tau_ciso < 2)
                isnIso[0] = not (s_tau_niso < 2)
                isdm[0] = not (s_tau_dm !=-1)
                d2s[0] = 1
                
                pt_dynamic[0] = d_tau_pt
                eta_dynamic[0] = d_tau_eta
                ciso_dynamic[0] = d_tau_ciso
                niso_dynamic[0] = d_tau_niso
                dm_dynamic[0] = d_tau_dm
                
                pt_standard[0] = s_tau_pt
                eta_standard[0] = s_tau_eta
                ciso_standard[0] = s_tau_ciso
                niso_standard[0] = s_tau_niso
                dm_standard[0] = s_tau_dm
                
                print 'tree is filling 1'
                tree.Fill()


#for key, value_standard in s_standard.iteritems():        
#        
#    if s_dynamic.has_key(key):
#        value_dynamic = s_dynamic[key]
#                        
#        d_tau_pt = value_dynamic['taupt']
#        d_tau_eta = value_dynamic['taueta']
#        d_tau_ciso = value_dynamic['ciso']
#        d_tau_niso = value_dynamic['nweight']
#        d_tau_dm = value_dynamic['taudm']
#
#        s_tau_pt = value_standard['taupt']
#        s_tau_eta = value_standard['taueta']
#        s_tau_ciso = value_standard['ciso']
#        s_tau_niso = value_standard['nweight']
#        s_tau_dm = value_standard['taudm']
#        
#        if s_tau_pt > 20 and abs(s_tau_eta) < 2.3 and s_tau_ciso < 2 and s_tau_niso < 2 and s_tau_dm!=-1:
#            
#            print 'basic selection passed 2'
#
#            if not (d_tau_pt > 20 and abs(d_tau_eta) < 2.3 and d_tau_ciso < 2 and d_tau_niso < 2 and d_tau_dm!=-1):
#            
#                
#                print 'pass2 !'
#                ispTeta[0] = not (d_tau_pt > 20 and abs(d_tau_eta) < 2.3)
#                ispT[0] = not (d_tau_pt > 20)
#                iseta[0] = not (abs(d_tau_eta) < 2.3)
#                iscIso[0] = not (d_tau_ciso < 2)
#                isnIso[0] = not (d_tau_niso < 2)
#                isdm[0] = not (d_tau_dm !=-1)
#                d2s[0] = 0
#                
#                pt_dynamic[0] = d_tau_pt
#                eta_dynamic[0] = d_tau_eta
#                ciso_dynamic[0] = d_tau_ciso
#                niso_dynamic[0] = d_tau_niso
#                dm_dynamic[0] = d_tau_dm
#                
#                pt_standard[0] = s_tau_pt
#                eta_standard[0] = s_tau_eta
#                ciso_standard[0] = s_tau_ciso
#                niso_standard[0] = s_tau_niso
#                dm_standard[0] = s_tau_dm
#            
#                print 'tree is filling 2'
#                tree.Fill()
            

file.Write()
file.Close()
