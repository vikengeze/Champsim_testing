#!/bin/bash

fp='/home/sonqo/Desktop/Diplom/traces_gap/bfs*'

for trace in $fp; do
	echo "Starting on trace file $(basename $trace)..."
	./benchmark.sh $trace $1
	echo "Done with trace file $(basename $trace)"
done


notify-send "Benching is done"
