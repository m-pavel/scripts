#!/usr/bin/env python
# Checkout specified list of projects

import argparse
import re
import os
from subprocess import call

parser = argparse.ArgumentParser()
parser.add_argument('--list', dest='list', required=True)
parser.add_argument('--dir', dest='dir',required=True)
args = parser.parse_args()


f = open(args.list, 'r')
for line in f:
    m = re.search('\/([\w|-]+)\/(trunk|branches)', line)
    if m:
	prjname = args.dir + "/" +m.group(1)	
	call (["/usr/bin/svn", "co", line.strip(), prjname])