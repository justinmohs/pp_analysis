#!/bin/bash
#
# job name:
#SBATCH --job-name=smash_pp
#
# (only parallel allowed?)
#SBATCH --partition=general1
#
# mem allocation (only 200m default)
#SBATCH --mem-per-cpu=1000
#
# default time 10min, max 8 days?:
#SBATCH --time=0-0:19:59

smash_build_folder=$1
sqrtsnn=$2
var=$3
value=$4
config=$5

export OMP_NUM_THREADS=1
rm -rf "data_"$sqrtsnn"_"$var"_"$value
mkdir "data_"$sqrtsnn"_"$var"_"$value
start_dir=$PWD
cd $smash_build_folder
run_smash() {
    i=$1    # get index
    mkdir "$start_dir/data_"$sqrtsnn"_"$var"_"$value"/$i"
    ./smash -i "$start_dir/$config" \
            -c "Modi: {Collider: {Sqrtsnn: $sqrtsnn}}" \
            -c "Collision_Term: {String_Parameters: {"$var": "$value"}}" \
            -o "$start_dir/data_"$sqrtsnn"_"$var"_$value/$i" \
            > "$start_dir/data_"$sqrtsnn"_"$var"_$value/$i/out.txt"
    cd $start_dir
    python all_hist.py "data_"$sqrtsnn"_"$var"_"$value"/$i" $sqrtsnn
    #rm "data_"$sqrtsnn"_"$var"_$value/$i/full_event_history.oscar"
}

ncpu=`grep -c '^processor' /proc/cpuinfo`

for (( i=1; i<=$ncpu; i++ ))
do
  run_smash ${i} &
done
wait
cd $start_dir
rm -rf "data_"$sqrtsnn"_"$var"_$value/plot_data"
mkdir "data_"$sqrtsnn"_"$var"_$value/plot_data"
python gather_all_data.py $sqrtsnn $ncpu "data_"$sqrtsnn"_"$var"_$value/"

