#!/bin/bash

fp='/home/sonqo/Desktop/Diplom/traces_gap/450*'

for trace in $fp; do
	echo "Starting on trace file $(basename $trace)..."
	./benchmark_2.sh $trace $1
	echo "Done with trace file $(basename $trace)"
done


notify-send "Benching_2 is done"
