#!/bin/bash

# example: ./rtt.sh <output_file> <target_url> <num_workers>
OUTFILE=$1
TARGET=$2
WORKERS=$3

ARRAY=(/srv/Pictures/*)

echo "Running load test..."

# curl requests are only sent out once previous ones are completed.
# otherwise, the timing data in the results are skewed.
iterations=$(((${#ARRAY[@]} / $WORKERS) - 1))
remainder=$((${#ARRAY[@]} % $WORKERS))
for i in $( seq 0 $iterations );
do
    temp=$(($i * $WORKERS))
    for j in $( seq 0 $(($WORKERS - 1)));
    do
        curl --write-out "@curl-format.txt" -4 ${ARRAY[$(($temp + $j))]/\/*\//$TARGET} --silent --create-dirs --output imgs/${ARRAY[$(($temp + $j))]/\/*\//} >> $OUTFILE &
    done;
    wait
done;
for i in $( seq $(($((${#ARRAY[@]} / $WORKERS)) * $WORKERS)) $((${#ARRAY[@]}-1)) );
do
    curl --write-out "@curl-format.txt" -4 ${ARRAY[$i]/\/*\//$TARGET} --silent --create-dirs --output imgs/${ARRAY[$i]/\/*\//} >> $OUTFILE &
done;
wait
echo "load test completed."
