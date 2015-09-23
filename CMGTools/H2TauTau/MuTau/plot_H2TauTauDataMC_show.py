import imp, math, copy, re, os, string

from CMGTools.H2TauTau.proto.plotter.H2TauTauDataMC import H2TauTauDataMC
from CMGTools.H2TauTau.proto.plotter.prepareComponents import prepareComponents
from CMGTools.H2TauTau.proto.plotter.rootutils import *
from CMGTools.H2TauTau.proto.plotter.categories_TauMu import *
from CMGTools.H2TauTau.proto.plotter.titles import xtitles
from CMGTools.H2TauTau.proto.plotter.plotmod import *
from CMGTools.H2TauTau.proto.plotter.datacards import *
from CMGTools.H2TauTau.proto.plotter.plotinfo import plots_All, plots_All_sorted_indices
from plot_helper import *
from optparse import OptionParser
from CMGTools.RootTools.RootInit import *

if __name__ == '__main__':

    parser = OptionParser()
    gROOT.SetBatch(True)
    
    parser.usage = '''   
    %prog <anaDir> <cfgFile>

    cfgFile: analysis configuration file, see CMGTools.H2TauTau.macros.MultiLoop
    anaDir: analysis directory containing all components, see CMGTools.H2TauTau.macros.MultiLoop.
    '''

    parser.add_option("-C", "--cut", 
                      dest="cut", 
                      help="cut to apply in TTree::Draw",
                      default='1')
    parser.add_option("-N", "--name", 
                      dest="name", 
                      help="category name",
                      default='none')
    
    (options,args) = parser.parse_args()
    if len(args) != 2:
        parser.print_help()
        sys.exit(1)

       
    cutstring = options.cut
    anaDir = args[0].rstrip('/')

    cfgFileName = args[1]
    cfgFile = open( cfgFileName, 'r' )
    cfg = imp.load_source( 'cfg', cfgFileName, cfgFile)

    options.cut = replaceCategories(options.cut, categories)    

    print 
    print '='*50
    print 'CUT : ', options.name
    print 'CUT : \t', options.cut
    print '='*50
    print 
