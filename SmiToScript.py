#!/usr/bin/python

import sys
import subprocess
import re
import os
import glob

def print_usage(exit_code):
	print("%s <path> [<encoding>]" % sys.argv[0])
	exit(exit_code)

def read_file(filename, encoding):
	return open(filename).read().decode(encoding, 'ignore').encode('utf-8')

def translate_file(smipath, encoding):
    time = 0
    lang = None
    prev_lang = None
    lines = []
    for line in read_file(smipath, encoding).split('\n'):
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
            line = line.replace('<br>', ' ')
            if lang == prev_lang:
                (t, s) = lines[-1]
                lines[-1] = (t, s + " " + line)
            else:
                lines.append((time, line))
                lang = prev_lang
    lines.sort()
    return list(map(lambda (t, s): s, lines))

def translate_dir(dirpath, encoding):
    if not dirpath.endswith('/'):
        dirpath += '/'
    dirpath += '*.smi'
    for smipath in glob.glob(dirpath):
        scripts = translate_file(smipath, encoding)
        outfile = open(smipath + '.txt', 'w')
        outfile.write('\n'.join(scripts))

if len(sys.argv) < 2:
	print_usage(1)

path = sys.argv[1]
encoding = 'utf-8'

if len(sys.argv) > 2:
	encoding = sys.argv[2]

if os.path.isdir(path):
    translate_dir(path, encoding)
else:
    print '\n'.join(translate_file(path, encoding))

