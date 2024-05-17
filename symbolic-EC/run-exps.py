from os import sys, path
from multiprocessing import Process
from os import listdir
from os.path import isfile, join, exists
import argparse
import subprocess, os, time, re
from time import sleep
import timeit
import shutil
import csv
import math
from datetime import datetime


convert = lambda text: int(text) if text.isdigit() else text
alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]

examples = {'b': 'brest', 'i': 'imis', 't': 'toy'}
methods = {'p': 'point-based', 'i': 'interval-based'}
times = {'b': [1443650401, 1445378401, [3600, 7200, 14400, 28800], 10],
	 'i': [1451606400, 1451806411, [2000, 500, 1000, 2000], 30],
	 't': [1443650401, 1443650512, [10], 100]}

xsb_command = ['xsb', '--noprompt', '--quietload', '--nobanner', '-c', '5g', '-m', '5g', '-o', '2g', '--nofeedback', '-e']


def main(args):

	if not os.path.exists(args['results_dir']):
		os.makedirs(args['results_dir'])

	# Run experiments

	print('Running experiments...')
	dstart = datetime.now()

	run_from_file(args)

	dend = datetime.now()
	dexp = dend - dstart
	print('System time elapsed for experiments...')
	print(dexp)

	print('Done!')


def run_from_file(args):

	print(args['data'])

	start = args['start_time']

	for w in args['window']:

		end = start + w * args['number_of_windows']
        
		wm = w

		step = wm
	  
		processes = []
		
		EC_stats_file = os.path.join(args['results_dir'], 'stats-wm=%s-step=%s' % (wm, step))

		EC_patterns_file = os.path.join(args['results_dir'], 'CEs-wm=%s-step=%s' % (wm, step))

		EC_command = getCommand(args['data'], str(start), str(wm), str(step), str(end),
			EC_stats_file, EC_patterns_file, args['dynPair'])

		if args['prolog'] == 'yap':
			EC_command = 'nb_setval(prl,yap),' + EC_command
			EC_prolog_args = [['yap', '-s', '0', '-h', '0', '-t', '0', '-l', args['prologFile'], '-g', EC_command]]
		elif args['prolog'] == 'swipl':
			EC_command = 'nb_setval(prl,swipl),' + EC_command
			EC_prolog_args = [['swipl', '--stack-limit=15g', '-l', args['prologFile'], '-g', EC_command]]
		elif args['prolog'] == 'xsb':
			EC_command = 'consult(\'' + args['prologFile'] + '\'),' + EC_command
			EC_prolog_args = [xsb_command + [EC_command]]

		print("New EC process... ")
		print(EC_prolog_args)

		sleep(1)
		p_EC = Process(target=run_prolog, args=EC_prolog_args)
		processes.append(p_EC)

		for p in processes:
			p.start()
		for p in processes:
			p.join()


def run_prolog(prolog_args):
	print("\nInvoking Prolog. Wait...\n")
	sleep(1)
	subprocess.call(prolog_args)
    

def getCommand(datafile, start, wm, step, end, statsFile, patternsFile, dynPair):
	dfstr = '[\'' + datafile + '\']'
	command = 'performFullER(%s,\'%s\',\'%s\',%s,%s,%s,%s),halt.' % (dfstr, statsFile, patternsFile, str(start), str(wm),
		str(step), str(end))
	if dynPair:
		command = 'assert(dynPair),' + command
	return command


if __name__ == "__main__":

	args = {}
	args['prolog'] = 'xsb'
	method = 'p'
	args['method'] = methods[method]

	args['dynPair'] = False

	if args['prolog'] == 'yap' or args['prolog'] == 'swipl':
		prolog_system = 'swipl'
	else:
		prolog_system = args['prolog']

	args['app'] = 'b'

	example = examples[args['app']]
	if args['app'] != 't':
		example = 'maritime'
	
	topDir = os.getcwd()
	EC_dir = topDir + '/../examples/' + example
	if args['app'] != 't':
		EC_data = EC_dir + '/' + examples[args['app']] + '/data/dynamic_data/'
		args['results_dir'] = EC_dir + '/' + examples[args['app']] + '/data/results/symbolic-EC/' + args['method'] + '/' + args['prolog'] + '/'
	else:
		EC_data = EC_dir + '/data/dynamic_data/'
		args['results_dir'] = EC_dir + '/data/results/symbolic-EC/' + args['method'] + '/' + args['prolog'] + '/'
	EC_data_files = [EC_data+f for f in listdir(EC_data) if isfile(EC_data+f) and f.endswith('.csv')]
	
	if args['app'] != 't':
		if args['dynPair']:
			args['results_dir'] += 'dp/'
		else:
			args['results_dir'] += 'ndp/'

	args['prologFile'] = EC_dir + '/symbolic-EC-files/' + args['method'] + '/' + prolog_system
	print(args['prologFile'])
	if args['prolog'] == 'swipl' or args['prolog'] == 'yap':
		args['prologFile'] += '/loadFiles.prolog'
	else:
		args['prologFile'] += '/loadFiles.P'
	args['start_time'] = times[args['app']][0]
	args['data'] = EC_data_files[0]
	args['window'] = times[args['app']][2]
	args['end_time'] = times[args['app']][1]
	args['number_of_windows'] = times[args['app']][-1]
	
	print("\nParameters set:")
	print(args)
	print("\n")
	main(args)

