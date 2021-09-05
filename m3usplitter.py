# Python
# m3usplitter.py, by lakeconstance78@wolke7.net
#
# this script: 
# 				1.  Splits M3U file in files by group
# 
# requirements: Python3
#
# command line: m3usplitter.py M3UFILE.py
#				
# todo
# - 

import re
import argparse
from io import open
import time
import os

CHECK = 0
GROUPNAME = 0

print("M3U-Splitter Splits M3U file in files by group")
print("----------------------------------------------")

parser = argparse.ArgumentParser()
parser.add_argument('M3UINPUT')
args = parser.parse_args()
file = open(args.M3UINPUT)

print("processing: " + args.M3UINPUT)
print("----------------------------------------------")

for line in file:
    CHECK = re.search('group-title="(.*)"', line)
    if CHECK: 
        GROUPNAME = re.search('group-title="(.*)"', line).group(1)
    if GROUPNAME:
        FILENAME = GROUPNAME + ".m3u"
    else: FILENAME = "Emptygroup.m3u"
    with open(FILENAME,'a', encoding='utf-8') as FILE:
        FILE.write(line)
    with open(FILENAME,'r', encoding='utf-8') as FILE:
        CONTENT = FILE.read()
        FIRST = CONTENT.split('\n', 1)[0]
        if '#EXTM3U' != FIRST:
            print(FILENAME + "-> #EXTM3U does not exists -> insert in line 1")
            with open("tempfile",'w', encoding='utf-8') as t:
                t.write('#EXTM3U\n' + CONTENT)
            os.rename("tempfile", FILENAME)