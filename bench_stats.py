import sys
from os import listdir
from os.path import isfile, join

prefetchers = ['asp', 'dp', 'no', 'oracle', 'sp']
prefs = ['asp', 'dp', 'no', 'oracle1', 'oracle2', 'oracle3', 'oracle4', 'oracle5', 'oracle6', 'sp']
path = '/home/sonqo/Desktop/Diplom/champsim_testing/statistics/'
keepers = ['_pass_iflag.txt', '_baselines.txt', '_pass_1.txt']
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

def namer(filename):
	if ("_ahead_by_" in filename):
		name = filename.split('_ahead_by_')[0]
		if "_baselines" in filename:
			name = name + "_baselines.txt"
		if "_pass_iflag" in filename:
			name = name + "_pass_iflag.txt"
		if "_pass_1" in filename:
			name = name + "_pass_1.txt"
	else:
		name = filename
	#print(filename + "          ===============>          " + name)
	return name

def mesoroi(dict): #dict is [key, value] == [trace file, [prefetcher, ipc]]
	keys = list(dict.keys())
	soumes = [0.0] * len(dict[keys[0]])
	gain = [0.0] * len(prefs)
	max_gain = [0.0] * len(prefs)
	avg_gain = [0.0] * len(prefs)
	ipc_big = ipc_smol = 0

	
	for key in keys: #for each trace
		#print(key)
		for i in range(0, 10): #for each prefetcher
			#print(i)
			#print(dict[key][i])
			if (dict[key][i][0] == prefs[i]): #choose 1 prefetcher
				#print(dict[key][i])
				soumes[i] = soumes[i] + float(dict[key][i][1])
			 	# gain = ((ipc_big-ipc_smol)/ipc_smol)*100 where ipc_smol == ipc_no
				gain[i] = 100*(float(dict[key][i][1])-float(dict[key][2][1]))/float(dict[key][2][1])
				#print(str(prefs[i]) + ' - ' + str(gain[i]))
				avg_gain[i] = avg_gain[i] + gain[i]
				if (gain[i] > max_gain[i]):
					#print(key)
					#print(str(prefs[i]) + ' - ' + str(gain[i]))
					max_gain[i] = gain[i]

	for i in range(0, 10):
		soumes[i] = "{:.2f}".format((soumes[i]/len(keys)))
		avg_gain[i] = "{:.2f}".format((avg_gain[i]/len(keys)))
		max_gain[i] = "{:.2f}".format(max_gain[i])
	return soumes, max_gain, avg_gain

def sort_files(files, pref, path_used):
	for file in files:
		with open(path_used + pref + '/' + file) as f:
			#print(f)
			#print(pref)
			lines = f.readlines()
			for line in lines:
				if line.startswith('Finished CPU'):
					ipc = line.split('IPC: ')[1].split(' (')[0]
			#print(file)
			name = namer(file)
			if ("_baselines" in name):
				if name in gap_ipcs:
				#print(name)
					if 'oracle' in pref:
						for i in range(1, 7):
							if (("ahead_by_"+str(i)) in file):
								extra = str(i)
								break
						gap_ipcs[name].append([pref + extra, ipc])
					else:	
						gap_ipcs[name].append([pref, ipc])
				else:
					#print(name)
					if 'oracle' in pref:
						for i in range(0, 7):
							if (str(i) in file):
								extra = str(i)
								break
						gap_ipcs[name] = [[pref + extra, ipc]]
					else:
						gap_ipcs[name] = [[pref, ipc]]
			elif ("_pass_1" in name):
				if name in spec06_ipcs:
				#print(name)
					if 'oracle' in pref:
						for i in range(1, 7):
							if (("ahead_by_"+str(i)) in file):
								extra = str(i)
								break
						spec06_ipcs[name].append([pref + extra, ipc])
					else:	
						spec06_ipcs[name].append([pref, ipc])
				else:
					#print(name)
					if 'oracle' in pref:
						for i in range(0, 7):
							if (("ahead_by_"+str(i)) in file):
								extra = str(i)
								break
						spec06_ipcs[name] = [[pref + extra, ipc]]
					else:
						spec06_ipcs[name] = [[pref, ipc]]
			elif ("_pass_iflag" in name):
				if name in spec17_ipcs:
				#print(name)
					if 'oracle' in pref:
						for i in range(1, 7):
							if (("ahead_by_"+str(i)) in file):
								extra = str(i)
								break
						spec17_ipcs[name].append([pref + extra, ipc])
					else:	
						spec17_ipcs[name].append([pref, ipc])
				else:
					#print(name)
					if 'oracle' in pref:
						for i in range(0, 7):
							if (("ahead_by_"+str(i)) in file):
								extra = str(i)
								break
						spec17_ipcs[name] = [[pref + extra, ipc]]
					else:
						spec17_ipcs[name] = [[pref, ipc]]
		
			
def printer(mesoi, max_gains, avg_gains, folder):
	print("Printing stats for " + folder + " traces")
	print("Stats are for prefetchers: ")
	for i in range(10):
		if ('oracle' in prefs[i]):
			print(str(prefs[i]) + '\t', end= " ")
		else:
			print(str(prefs[i]) + '\t\t\t', end= " ")
	print()

	print("Average IPCs")
	for i in range(10):
		print(str(mesoi[i]) + '\t\t', end=" ")
	print()

	print("Maximum gains (%)")
	for i in range(10):
		print(str(max_gains[i]) + '\t\t', end=" ")	
	print()

	print("Average gains (%)")
	for i in range(10):
		print(str(avg_gains[i]) + '\t\t', end=" ")
	print()
	print('*'*42 + '*'*42*2)

print("Stats (using Prefetch Buffer)")
for prefetcher in prefetchers:
	if prefetcher == 'oracle':
		pref = prefetcher
		files = [f for f in sorted(listdir(path + pref)) if (isfile(join(path+pref, f)))]
		#new_files = [f for f in files if (f.split('M')[1] in keepers)]
		#print(new_files)
		sort_files(files, pref, path)
	else: 
		pref = prefetcher
		files = [f for f in sorted(listdir(path + pref)) if (isfile(join(path+pref, f)))]
		#new_files = [f for f in files if f.split('M')[1] in keepers]
		#print(new_files)	
		sort_files(files, pref, path)

#print(spec06_ipcs)
all_ipcs = {}
all_ipcs.update(gap_ipcs)
all_ipcs.update(spec06_ipcs)
all_ipcs.update(spec17_ipcs)

mesoi, max_gains, avg_gains = mesoroi(gap_ipcs)
printer(mesoi, max_gains, avg_gains, 'baselines')
mesoi, max_gains, avg_gains = mesoroi(spec06_ipcs)
printer(mesoi, max_gains, avg_gains, 'pass_1')
mesoi, max_gains, avg_gains = mesoroi(spec17_ipcs)
printer(mesoi, max_gains, avg_gains, 'pass_iflag')
#mesoi, max_gains, avg_gains = mesoroi(all_ipcs)
#printer(mesoi, max_gains, avg_gains, 'all')

print()
print()

gap_ipcs.clear()
spec06_ipcs.clear()
spec17_ipcs.clear()
all_ipcs.clear()
'''
print("Stats when not using Prefetch Buffer")

for prefetcher in prefetchers:
	if prefetcher == 'oracle':
		for i in range(1, 7):
			pref = prefetcher + '/ahead_by_' + str(i)
			files = [f for f in listdir(path_no_pb + pref) if isfile(join(path_no_pb+pref, f))]
			sort_files(files, pref, path_no_pb)
	else: 
		pref = prefetcher
		files = [f for f in listdir(path_no_pb + prefetcher) if isfile(join(path_no_pb+prefetcher, f))]
		sort_files(files, pref, path_no_pb)

all_ipcs = {}
all_ipcs.update(gap_ipcs)
all_ipcs.update(spec06_ipcs)
all_ipcs.update(spec17_ipcs)

mesoi, max_gains, avg_gains = mesoroi(gap_ipcs)
printer(mesoi, max_gains, avg_gains, 'gap')
mesoi, max_gains, avg_gains = mesoroi(spec06_ipcs)
printer(mesoi, max_gains, avg_gains, 'spec06')
mesoi, max_gains, avg_gains = mesoroi(spec17_ipcs)
printer(mesoi, max_gains, avg_gains, 'spec17')
mesoi, max_gains, avg_gains = mesoroi(all_ipcs)
printer(mesoi, max_gains, avg_gains, 'all')'''