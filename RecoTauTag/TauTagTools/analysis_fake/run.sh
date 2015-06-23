for a in dynamic95 standard
do
    echo $a &
    rm save_${a}.db &
    python runTauDisplay.py $a &
done
