#!/usr/bin/python

import sys
import subprocess
import re

def print_usage(exit_code):
	print("%s <input file> [<encoding>]" % sys.argv[0])
	exit(exit_code)

def read_file(filename, encoding):
	return open(filename).read().decode(encoding, 'ignore').encode('utf-8')

if len(sys.argv) < 2:
	print_usage(1)

filename = sys.argv[1]
encoding = 'utf-8'

if len(sys.argv) > 2:
	encoding = sys.argv[2]

time = 0
lang = None
prev_lang = None
lines = []

for line in read_file(filename, encoding).split('\n'):
	line = line.strip()
	if line.startswith('<SYNC'):
		r = re.match('<SYNC Start=(\d+)><P Class=(.+)>', line)
		time = int(r.group(1))
		lang = r.group(2)
	elif not line.startswith('<') and time > 0:
		line = line.strip()
		if line.startswith('- '):
			line = line[2:]
		if line.endswith('<br>'):
			line = line[:-4]
		if lang == prev_lang:
			(t, s) = lines[-1]
			lines[-1] = (t, s + " " + line)
		else:
			lines.append((time, line))
			lang = prev_lang

lines.sort()
for (t, s) in lines:
	print s
