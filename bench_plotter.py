import sys
from scipy.stats import dgamma
import matplotlib.pyplot as plt
import seaborn as sns
from os import listdir
from os.path import isfile, join
from matplotlib import colors
from matplotlib.ticker import PercentFormatter
import numpy as np
plt.rcParams.update({'font.size': 16})
plt.rcParams.update({'figure.autolayout': True})

prefetchers = ['asp', 'dp', 'no', 'oracle', 'sp']
prefs = ['asp', 'dp', 'no', 'oracle1', 'oracle2', 'oracle3', 'oracle4', 'oracle5', 'oracle6', 'sp']
path = '/home/sonqo/Desktop/Diplom/bench_results/bench/'
folder = ''
ipc = 0
gap_ipcs = {}		#[key, value] = [trace file, [prefetcher, ipc]
spec06_ipcs = {}
spec17_ipcs = {}
#Single diagrammata gia kathe bench -- done
#Thelw na ftiaksw kapoia sum diagrammata:
#1) Sunoliko gia kathe fakelo
#2) Sunoliko gia ola ta benchmarks
#3) --?


def get_folder(file):
	if file.startswith('4'):
		folder = 'spec06'
	elif file.startswith('6'):
		folder = 'spec17'
	else:
		folder = 'gap'
	return folder

#ftiaxnw mia lista soumes
def mesoroi(dict): #dict is [key, value] == [trace file, [prefetcher, ipc]] 
	keys = list(dict.keys())
	soumes=[0]*len(dict[keys[0]])

	for key in keys:
		for i in range(0, 10):
			if (dict[key][i][0] == prefs[i]):
				soumes[i] = soumes[i] + float(dict[key][i][1])

	for i in range(0, 10):
		soumes[i] = soumes[i]/len(keys)

	return soumes

def sort_files(files, pref):
	for file in files:
		with open(path + pref + '/' + file) as f:
			lines = f.readlines()
		for line in lines:
			if line.startswith('Finished CPU'):
				ipc = line.split('IPC: ')[1].split(' (')[0]
		if file.startswith('4'):
			folder = 'spec06'
			if file in spec06_ipcs:
				if 'oracle' in pref:
					spec06_ipcs[file].append([pref.split('/')[0] + pref.split('_')[2], ipc])
				else:	
					spec06_ipcs[file].append([pref, ipc])
			else:
				if 'oracle' in pref:
					spec06_ipcs[file] = [[pref.split('/')[0] + pref.split('_')[2], ipc]]
				else:	
					spec06_ipcs[file] = [[pref, ipc]]
		elif file.startswith('6'):
			folder = 'spec17'
			if file in spec17_ipcs:
				if 'oracle' in pref:
					spec17_ipcs[file].append([pref.split('/')[0] + pref.split('_')[2], ipc])
				else:	
					spec17_ipcs[file].append([pref, ipc])
			else:
				if 'oracle' in pref:
					spec17_ipcs[file] = [[pref.split('/')[0] + pref.split('_')[2], ipc]]
				else:	
					spec17_ipcs[file] = [[pref, ipc]]
		else:
			folder = 'gap'
			if file in gap_ipcs:
				if 'oracle' in pref:
					gap_ipcs[file].append([pref.split('/')[0] + pref.split('_')[2], ipc])
				else:	
					gap_ipcs[file].append([pref, ipc])
			else:
				if 'oracle' in pref:
					gap_ipcs[file] = [[pref.split('/')[0] + pref.split('_')[2], ipc]]
				else:	
					gap_ipcs[file] = [[pref, ipc]]

for prefetcher in prefetchers:
	if prefetcher == 'oracle':
		for i in range(1, 7):
			pref = prefetcher + '/ahead_by_' + str(i)
			files = [f for f in listdir(path + pref) if isfile(join(path+pref, f))]
			sort_files(files, pref)
	else: 
		pref = prefetcher
		files = [f for f in listdir(path + prefetcher) if isfile(join(path+prefetcher, f))]
		sort_files(files, pref)

values = []
labels = prefs
x = np.arange(10)

fig, ax = plt.subplots(figsize=(24,12))

for key in gap_ipcs:
	for i in range (0, len(gap_ipcs[key])):
		values.append(float(gap_ipcs[key][i][1]))

	plt.xlabel('TLB prefetcher used')
	plt.xticks(ticks=x, labels=labels)
	plt.ylabel('IPC')
	plt.title('Benchmarks for trace file ' + key.split('_')[0])
	plt.bar(x, values, color ='maroon', width = 0.1)
	#plt.show()
	plt.savefig('plots/pb_used/singles/' + get_folder(key) + '/' + key.split('_')[0] + '.png', dpi=300)
	plt.clf()
	#cleanup
	values = []

for key in spec06_ipcs:
	for i in range (0, len(spec06_ipcs[key])):
		values.append(float(spec06_ipcs[key][i][1]))

	plt.xlabel('TLB prefetcher used')
	plt.xticks(ticks=x, labels=labels)
	plt.ylabel('IPC')
	plt.title('Benchmarks for trace file ' + key.split('_')[0])
	plt.bar(x, values, color ='maroon', width = 0.1)
	#plt.show()
	plt.savefig('plots/pb_used/singles/' + get_folder(key) + '/' + key.split('_')[0] + '.png', dpi=300)
	plt.clf()
	#cleanup
	values = []

for key in spec17_ipcs:
	for i in range (0, len(spec17_ipcs[key])):
		values.append(float(spec17_ipcs[key][i][1]))

	plt.xlabel('TLB prefetcher used')
	plt.xticks(ticks=x, labels=labels)
	plt.ylabel('IPC')
	plt.title('Benchmarks for trace file ' + key.split('_')[0])
	plt.bar(x, values, color ='maroon', width = 0.1)
	#plt.show()
	plt.savefig('plots/pb_used/singles/' + get_folder(key) + '/' + key.split('_')[0] + '.png', dpi=300)
	plt.clf()
	#cleanup
	values = []

total_gap = mesoroi(gap_ipcs)
total_spec06 = mesoroi(spec06_ipcs)
total_spec17 = mesoroi(spec17_ipcs)

plt.xlabel('TLB prefetcher used')
plt.xticks(ticks=x, labels=labels)
plt.ylabel('IPC')
plt.title('Benchmarks for all gap trace files')
plt.bar(x, total_gap, color ='maroon', width = 0.1)
#plt.show()
plt.savefig('plots/pb_used/total/gap_total.png', dpi=600)
plt.clf()

plt.xlabel('TLB prefetcher used')
plt.xticks(ticks=x, labels=labels)
plt.ylabel('IPC')
plt.title('Benchmarks for all spec06 trace files')
plt.bar(x, total_spec06, color ='maroon', width = 0.1)
#plt.show()
plt.savefig('plots/pb_used/total/spec06_total.png', dpi=600)
plt.clf()

plt.xlabel('TLB prefetcher used')
plt.xticks(ticks=x, labels=labels)
plt.ylabel('IPC')
plt.title('Benchmarks for all spec17 trace files')
plt.bar(x, total_spec17, color ='maroon', width = 0.1)
#plt.show()
plt.savefig('plots/pb_used/total/spec17_total.png', dpi=600)
plt.clf()

total_final = [0]*len(total_gap)
for i in range(len(total_gap)):
	total_final[i] = (total_gap[i] + total_spec06[i] + total_spec17[i])/3

plt.xlabel('TLB prefetcher used')
plt.xticks(ticks=x, labels=labels)
plt.ylabel('IPC')
plt.title('Benchmarks for all trace files')
plt.bar(x, total_final, color ='maroon', width = 0.1)
#plt.show()
plt.savefig('plots/pb_used/total/final_total.png', dpi=600)
plt.clf()