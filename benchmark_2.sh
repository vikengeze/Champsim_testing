#!/bin/bash

trace=$1
test_name=$2
echo "Starting on trace file $(basename $trace)..."

#echo "Running no prefetcher bench"
#./run_champsim.sh no-bimodal-no-no-no-lru-1core 1 100 ${trace} no 0 $test_name
#echo "No prefetcher is Done"

#echo "Running sequential prefetcher bench"
#./run_champsim.sh sp-bimodal-no-no-no-lru-1core 1 100 ${trace} sp 0 $test_name
#echo "Sequential prefetcher is Done"

#echo "Running arbitrary stride prefetcher bench"
#./run_champsim.sh asp-bimodal-no-no-no-lru-1core 1 100 ${trace} asp 0 $test_name
#echo "ASP prefetcher is Done"

#echo "Running distance prefetcher bench"
#./run_champsim.sh dp-bimodal-no-no-no-lru-1core 1 100 ${trace} dp 0 $test_name
#echo "DP prefetcher is Done"

echo "Running oracle prefetcher bench"
for number in {1..6}; do
	echo "Seeing ${number} ahead"
	./run_champsim.sh from_file-bimodal-no-no-no-lru-1core 1 100 ${trace} oracle ${number} $test_name
	echo "Oracle prefetcher(${number} ahead) is Done"
done

echo "Done with trace file $(basename $trace)"
