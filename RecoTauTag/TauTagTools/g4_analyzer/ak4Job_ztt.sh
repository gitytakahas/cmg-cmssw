#cd ${dir}
currDir=`pwd`
echo 'Now working in '${currDir}
eval `scramv1 runtime -sh`
cmsRun g4.py maxEvents=${1} skipEvents=${2}
