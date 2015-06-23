#for a in dynamic95 standard
for a in dynamic95 run1
do
    echo $a &
    rm save_${a}.db &
    python runTauDisplay.py $a &
done
