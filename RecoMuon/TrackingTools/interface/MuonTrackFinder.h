#ifndef RecoMuon_TrackingTools_MuonTrackFinder_H
#define RecoMuon_TrackingTools_MuonTrackFinder_H

/** \class MuonTrackFinder
 *  Track finder for the Muon Reco
 *
 *  $Date: 2006/05/17 13:05:15 $
 *  $Revision: 1.3 $
 *  \author R. Bellan - INFN Torino
 */

#include "DataFormats/TrackReco/interface/TrackFwd.h"

#include "DataFormats/TrajectorySeed/interface/TrajectorySeedCollection.h"

#include "TrackingTools/PatternTools/interface/Trajectory.h"
#include <vector>

namespace edm {class ParameterSet; class Event; class EventSetup;}

class MuonTrajectoryBuilder;
class MuonTrajectoryCleaner;

class MuonTrackFinder{ 
  
 public:

  typedef std::vector<Trajectory> TrajectoryContainer;

 public:
  
  /// constructor
  MuonTrackFinder(MuonTrajectoryBuilder* ConcreteMuonTrajectoryBuilder);
  
  /// Destructor
  virtual ~MuonTrackFinder();
  
  /// Reconstruct tracks
  std::auto_ptr<reco::TrackCollection> reconstruct(const edm::Handle<TrajectorySeedCollection>&);

  /// Percolate the Event Setup
  void setES(const edm::EventSetup&);

 private:

  MuonTrajectoryBuilder* theTrajBuilder; // It isn't the same as in ORCA!!Now it is a base class

  MuonTrajectoryCleaner* theTrajCleaner;

  std::auto_ptr<reco::TrackCollection> convert(TrajectoryContainer&) const;
 protected:
  
};
#endif 

