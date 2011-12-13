#!/usr/bin/python3

import time

def start():
	return time.time()

def end(start):
	diff = time.time() - start
	if diff < 60:
		print('Took %s seconds to execute' %(diff))
	elif diff < 3600:
		print('Took %s minutes to execute' %(diff/60))
	else:
		print('Took %s hours to execute' %(diff/3600))
