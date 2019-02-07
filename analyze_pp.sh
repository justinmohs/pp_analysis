#!/bin/bash
#
#SBATCH --nodes=1
#
# no hyperthreading necessary
#SBATCH --extra-node-info=2:10:1
#
# job name:
#SBATCH --job-name=smash
#
# (only parallel allowed?)
#SBATCH --partition=test
#
# mem allocation (only 200m default)
#SBATCH --mem-per-cpu=1000
#
# default time 10min, max 8 days?:
#SBATCH --time=0-0:03:59

sqrtsnn=$1
foldername=$2
nfolders=$3
run_smash() {
    i=$1    # get index
    python all_hist.py "$foldername$i" $sqrtsnn
}

ncpu=`grep -c '^processor' /proc/cpuinfo`

for (( i=1; i<=$ncpu; i++ ))
do
  run_smash ${i} &
done
wait
rm -rf "data_$sqrtsnn/plot_data"
mkdir "data_$sqrtsnn/plot_data"
python gather_all_data.py $sqrtsnn $nfolders $foldername

