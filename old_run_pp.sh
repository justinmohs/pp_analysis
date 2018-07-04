#!/bin/bash
#
#SBATCH --ntasks=20
#SBATCH --nodes=1
#
# constrain depending on how this was compiled
#SBATCH --constraint=intel20
#
# no hyperthreading necessary
#SBATCH --extra-node-info=2:10:1
#
# job name:
#SBATCH --job-name=smash
#
# (only parallel allowed?)
#SBATCH --partition=parallel
#
# mem allocation (only 200m default)
#SBATCH --mem-per-cpu=1000
#
# default time 10min, max 8 days?:
#SBATCH --time=0-9:59:59

smash_build_folder=$1
sqrtsnn=$2
rm -rf "data_$sqrtsnn"
mkdir "data_$sqrtsnn"
start_dir=$PWD
cd $smash_build_folder
run_smash() {
    i=$1    # get index
    mkdir "$start_dir/data_$sqrtsnn/$i"
    ./smash -i "$start_dir/config.yaml" \
            -c "Modi: {Collider: {Sqrtsnn: $sqrtsnn}}" \
            -o "$start_dir/data_$sqrtsnn/$i" \
            > "$start_dir/data_$sqrtsnn/$i/out.txt"
    cd $start_dir
    python x_F_hist.py "data_$sqrtsnn/$i" $sqrtsnn
}

ncpu=`grep -c '^processor' /proc/cpuinfo`

for (( i=1; i<=$ncpu; i++ ))
do
  run_smash ${i} &
done
wait
cd $start_dir
rm -rf "data_$sqrtsnn/plot_data"
mkdir "data_$sqrtsnn/plot_data"
python gather_data.py $sqrtsnn $ncpu

