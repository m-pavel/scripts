#!/usr/bin/env python
# Walk throug specified directory and update provided property in pom.xml files
# property has to be expected value

import argparse
import os
import re
from os.path import join, getsize
vv = set()
def fpr(fname, expct, vers, bom):
    f = open(fname, 'r')
    list1 = []
    matches = False
    for line in f:
        m = re.search("(.*)<"+bom+">(.*)</"+bom+">(.*)", line)
	if m:
	    if m.group(2) == expct:
		print ("Updated "+expct+" in "+fname+"\n")
		list1.append(m.group(1)+"<"+bom+">"+vers+"</"+bom+">"+m.group(3)+"\n")
		matches = True
    	    else:
    		print ("Skiped "+m.group(2)+" in "+fname+"\n")
    		vv.add(m.group(2))
		list1.append(line)
		matches = False
	else:
    	    list1.append(line)
    if matches:
        f = open(fname,'w')
        for line in list1:
            f.write(line)
        f.close()

parser = argparse.ArgumentParser(description='Process some integers.')

parser.add_argument('--dir', dest='dir',help='directory to process',required=True)
parser.add_argument('--expct', dest='expct',help='expected version', required=True)
parser.add_argument('--version', dest='version',help='version to replace', required=True)
parser.add_argument('--bom', dest='bom',help='artifact name',required=True)

args = parser.parse_args()

print (args.dir)

for root, dirs, files in os.walk(args.dir):
    if 'pom.xml' in files:   
	fpr (root+"/pom.xml", args.expct, args.version, args.bom)
print vv
