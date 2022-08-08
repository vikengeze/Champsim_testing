#!/bin/bash

binary=${1}
n_warm=${2}
n_sim=${3}
trace=${4}
option=${5}
extra=${6}
test_name=${7}
#extra is no. of looking ahead for oracle, option is oracle or not
DESTINATION_FOLDER='statistics'
mkdir -p ${DESTINATION_FOLDER}/${option}

if [ $option == "oracle" ]; then
	python3 oracle.py ${trace}_${n_sim}M ${extra}
	(./bin/${binary} -warmup_instructions ${n_warm}000000 -simulation_instructions ${n_sim}000000 -traces ${trace}) &> ${DESTINATION_FOLDER}/${option}/$(basename $trace)_${n_sim}M_ahead_by_${extra}_$test_name.txt
else
	(./bin/${binary} -warmup_instructions ${n_warm}000000 -simulation_instructions ${n_sim}000000 -traces ${trace}) &> ${DESTINATION_FOLDER}/${option}/$(basename $trace)_${n_sim}M_$test_name.txt
fi
