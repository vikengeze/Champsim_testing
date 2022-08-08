#!/usr/bin/python

import sys

if ("450" in sys.argv[1]):
	base = "/home/sonqo/Desktop/Diplom/trace_files_tlb/spec06/"
else:
	base = "/home/sonqo/Desktop/Diplom/trace_files_tlb/gap/"

finish = "_trace.txt"
if (len(sys.argv) == 3):
	file = base + sys.argv[1].split('/')[6] + finish
	number = int(sys.argv[2])
else:
	print("Usage: oracle.py $trace_name $no_of_cheating")
	exit()

instr_id = []
address = []
hit = []
with open(file) as f:
	lines = f.readlines()
	for line in lines:
		instr_id.append(line.split(', ')[0])
		#curr_cycle = line.split(', ')[1] 
		address.append(line.split(', ')[2]) 
		#ip = line.split(', ')[3]
		hit.append(line.split(', ')[4].split('\n')[0])

with open("prefetches.txt", 'w+') as file:
	for i in range(0, len(instr_id)-number):
		if (hit[i+number] == '0'):
			file.write(str(instr_id[i]) + ", " + str(address[i+number]) + '\n')
	for i in range(len(instr_id)-number, len(instr_id)):
		file.write(str(instr_id[i]) + ", " + str(address[len(address)-1]) + '\n')
