ProductionTasks.py -w '*.root' -c -N 1 -q 1nd -t SS14 --batch_user htautau_group --output_wildcard '*.root' --cfg miniAOD-prod_PAT.py `cat samples.txt`
