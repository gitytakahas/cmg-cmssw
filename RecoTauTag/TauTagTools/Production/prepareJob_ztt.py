import os,sys
argList=sys.argv
if len(argList) != 4:
  print 'Wrong number of arguments! [dirname][Nevents_per_job][Njob]'
  sys.exit(1)

jobName=argList[1]
eventsPerJob=argList[2]
numberOfJobs=argList[3]
batchScript='ak4Job_ztt.sh'
cfgScript='SingleTaupt_50_cfi_GEN_SIM_DIGI_L1_DIGI2RAW_RAW2DIGI_L1Reco_RECO.py'
#cfgScript='SinglePi.py'
currDir=os.getcwd()

print 'This job will run from dir '+jobName
print 'The number of events per job will be '+str(eventsPerJob)
print 'The number of jobs will be '+str(numberOfJobs)
cont=raw_input('Do you agree? (Y/N) ')

if cont!='Y' :
  print 'Ending execution!'
  sys.exit(1)

from subprocess import call
call(["mkdir","-p",jobName]) # make dir if not exist

f=open(batchScript)
batchCommands=f.readlines()
f.close()


for j_number in range(int(numberOfJobs)):
  print j_number
  call(["mkdir","-p",jobName+"/job_"+str(j_number)])
  command=currDir+'/'+jobName+'/job_'+str(j_number)+'/'+batchScript + ' ' + str(eventsPerJob)+' '+str(j_number)
  print command
  call(["cp",cfgScript,jobName+"/job_"+str(j_number)])
  os.chdir(jobName+"/job_"+str(j_number))
  print os.getcwd()
  cmd_f=open(batchScript,'w')
  cmd_f.write('dir='+currDir+'/'+jobName+'/job_'+str(j_number)+'\n')
  for line in batchCommands:
    cmd_f.write(line)
  cmd_f.close()
  call(["chmod","+x",batchScript])
  call(["bsub","-q","8nh",command])
  os.chdir(currDir)

print os.getcwd()

