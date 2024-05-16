import os
from os import listdir
from os.path import isfile, join
import sys
import argparse
import subprocess
import re
from time import sleep, process_time
from datetime import datetime
from multiprocessing import Process
import csv
import tracemalloc

import src
from data_loader.data_loading import readAppDynamicData

topDir = os.getcwd()

examples = {'b': 'brest', 'i': 'imis', 't': 'toy'}
times = {'b': [1443650401, 1445378401, [3600, 7200, 14400, 28800], 10],
	 'i': [1451606400, 1451806411, [2000, 500, 1000, 2000], 30],
	 't': [1443650401, 1443650512, [10], 100]}

example = 'b'
if example == 'b' or example == 'i':
	sys.path.insert(1, topDir + '/../examples/maritime')
	prolog_file = topDir + '/../examples/maritime/symbolic-EC-files/point-based/xsb/patterns.P'
	example_dir = topDir + '/../examples/maritime/' + examples[example] + '/data'
else:
	sys.path.insert(1, topDir + '/../examples/' + examples[example])
	prolog_file = ''
	example_dir = topDir + '/../examples/' + examples[example] + '/data'

dynamic_data = example_dir + '/dynamic_data/' + examples[example] + '.csv'
results_dir = example_dir + '/results/Tensor-EC/'
dynamic_grounding = True
clock = 1

fos = 'csr'
linear = False

import Tensor_EC_files as app


def main():
	if not os.path.exists(results_dir):
		os.makedirs(results_dir)

	# Run experiments

	print('Running experiments...')
	dstart = datetime.now()

	run_from_file()

	dend = datetime.now()
	dexp = dend - dstart
	print('System time elapsed for experiments...')
	print(dexp)

	print('Done!')


def run_from_file():

	windows = times[example][2]
	start_time = times[example][0]
	number_of_windows = times[example][-1]

	for w in windows:

		end_time = start_time + w * number_of_windows

		step = w
		er = src.ER(w, step, clock, dynamic_grounding, fos)
		cachingOrder, definitions, tensors_dim = app.readDefinitions(prolog_file)

		data = open(dynamic_data)
		csv_f = csv.reader(data, delimiter='|')
		previous_row = None

		results_file = open(results_dir + 'CEs-wm=%d-step=%d' % (w, step), 'w')
		stats = []
		memory = []

		for initTime in range(start_time, end_time, step):

			tracemalloc.start()

			qt = initTime + step

			if qt > end_time:
				break

			er.__windowParams__(initTime, qt)

			print('ER: ', qt, ' Remaining steps: ', int(round((end_time - qt) / step)))

			src.sev.__forget__()
			src.isdf.__forget__()

			previous_row = readAppDynamicData(csv_f, initTime, qt, clock, app.declarations, previous_row)

			if dynamic_grounding:
				app.dg()
				er.__updateParams__(tensors_dim)

			src.sev.__finalize__()
			src.isdf.__finalize__()

			er_start = process_time()

			er.__run__(cachingOrder, app.declarations, definitions, linear)

			er_end = process_time()

			memory.append(round(tracemalloc.get_traced_memory()[-1]/(1024 ** 2), 3))
			tracemalloc.stop()

			writeResults(results_file, qt)
			stats.append(int(round(((er_end - er_start) * 1000))))

		writeStats(stats, memory, w, step)

		data.close()
		results_file.close()
		src.simple.__forget__()
		src.sev.__forget__()
		src.isdf.__forget__()
		del er


def writeResults(results, qt):
	results.write('ER: ' + str(qt) + '\n\n')

	for fluent in src.simple.instances:
		results.write(src.simple.instances[fluent].__getString__())

	for fluent in src.csdf.instances:
		results.write(src.csdf.instances[fluent].__getString__())

	for event in src.cev.instances:
		results.write(src.cev.instances[event].__getString__())

	results.write('\n\n')


def writeStats(stats, memory, window, step):
	with open(results_dir + 'stats-wm=%d-step=%d' % (window, step), 'w') as fw:
		fw.write('Times:\n')
		fw.write('[')
		fw.write(', '.join(map(str, stats)))
		fw.write(']\n\n')
		total = sum(stats)
		average = round(total / len(stats))
		fw.write('Total/Average Time: ' + str(total) + '/' + str(average) + '\n\n')

		fw.write('Memory Allocation:\n')
		fw.write('[')
		fw.write(', '.join(map(str, memory)))
		fw.write(']\n\n')
		total = round(sum(memory), 3)
		average = round(total / len(memory), 2)
		fw.write('Total/Average Memory: ' + str(total) + '/' + str(average) + '\n')


if __name__ == "__main__":
	main()
