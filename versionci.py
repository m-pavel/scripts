#!/usr/bin/env python
# Walk through specified directory and perform provided svn action

import argparse
import os
import re
from subprocess import call

from os.path import join, getsize

parser = argparse.ArgumentParser(description='Process some integers.')

parser.add_argument('--action', dest='action',help='ci|up',required=True)
parser.add_argument('--dir', dest='dir',help='directory to process',required=True)
parser.add_argument('--message', dest='message',help='message', required=False)
parser.add_argument('--username', dest='username',help='username', required=False)

args = parser.parse_args()

print (args.dir)

for root in os.listdir(args.dir):
    print (args.dir + root+"\n")
    if args.action == 'ci':
	ci_arr = ["svn", "ci", "--message", args.message, args.dir + "/"+ root]
	if args.username:
	    ci_arr = ["svn", "ci", "--message", args.message, args.dir + "/"+ root, "--username", args.username]
        call(ci_arr)
    else:
	call(["svn", "up", args.dir + "/"+ root])
