# python3
# m3usplitter.py, by lakeconstance78@wolke7.net
#
# this script:
# 				1. Sortout duplicate files
#               2. Splits M3U file in files by group
# requirements: Python3
#
# command line: m3usplitter.py M3UFILE.py
#
# TODO:

import re
import argparse
from io import open
import time
import os
import string
import datetime

SORTOUTROUNDS=0 # DEFINES HOW MANY LOOPS THE DEDUPLICATE MECHANISM WILL DO
CHECK = 0
GROUPNAME = None
EXTINF = None
LINK = None
MERGECHANNELS = None

CHANNELCOUNT = 0
CHCOUNT = 0
MERGECOUNT = 0
MECOUNT = 0
SORTCOUNT = 0
SOCOUNT = 0

print("M3U-Splitter Splits M3U file in files by group")
print("----------------------------------------------")
TIMESTART = datetime.datetime.utcnow()

# READ INPUT FILE
parser = argparse.ArgumentParser()
parser.add_argument('M3UINPUT')
args = parser.parse_args()
INPUTFILE = open(args.M3UINPUT)
CHANNELS = INPUTFILE.read()

# TODO: OPTIMIZE SPACES AND ADDITION CHANNEL INFO AND DELETE BELOW
# PATTERN FOR CHANNEL
PATTERN = re.compile('#EXTINF:.*group-title="(.*?)".*,(.*)\nhttps?:\/\/(.*)\n')
# OLD! PATTERN = re.compile('#EXTINF:.*group-title="(.*?)".*,.*\nhttps?:\/\/(.*)\n')

print("Searching for duplicates in " + args.M3UINPUT)
print("----------------------------------------------")
# SEARCHING FOR DUPLICATES IN INPUTFILE
for i in range (SORTOUTROUNDS+1):
    for match in PATTERN.finditer(CHANNELS):
        CHANNELCOUNT = CHANNELCOUNT + 1
        CHCOUNT = CHANNELCOUNT / (i+1)
        if os.path.exists('m3u_merge_'+str(i)+'.m3u'):
            with open('m3u_merge_'+str(i)+'.m3u','r', encoding='utf-8') as MERGEFILE:
                MERGECHANNELS = MERGEFILE.read()
        else:
            with open('m3u_merge_'+str(i)+'.m3u','w', encoding='utf-8') as MERGEFILE:
                MERGEFILE.write('#EXTM3U\n')
        if MERGECHANNELS != None:
            CHANNEL = match.group(0)
            # RENAMES FOR CHANNEL TAGS
            # DELETE HD, FHD, UHD TAGS
            CHANNEL = re.sub('(F?U?HD)','',CHANNEL)
            # DELETE TEXT BETWEEN () AND [] e.g. (360p) OR [geo-blocked]
            CHANNEL = re.sub('\(.*?\)','',CHANNEL)
            CHANNEL = re.sub('\[.*?\]','',CHANNEL)
            # OPEN FILE WITH RENAME INFOS AND RENAME ALL GROUPS THAT MATCH TEXT IN RENAME INFOS
            with open('m3urenames.txt', 'r') as RENAMEFILE:
                    for line in RENAMEFILE:
                        TEXT, RENAME = line.split(",")
                        RENAME = RENAME.rstrip()
                        if re.findall(TEXT, match.group(1), flags=re.I|re.M):
                            GROUPNAMEBF = match.group(1)
                            CHANNEL = re.sub(match.group(1), RENAME, match.group(0), flags=re.I)
                            GROUPNAME = re.search(PATTERN, CHANNEL).group(1)
                            if (GROUPNAME != None) and (GROUPNAME != GROUPNAMEBF):
                                print("Groupname of Channel " + re.search(PATTERN, CHANNEL).group(2) + " renamed from " + GROUPNAMEBF + " to " + GROUPNAME)
                        continue
            # LOOKING FOR SPECIAL INTEREST e.g. MUSIC OR BROADCAST COMPANIES
            if re.findall('.*Mus?z?ic?k?.*', CHANNEL, flags=re.I) or re.findall('.*MTV.*', CHANNEL, flags=re.I) or re.findall('.*Stingray.*', CHANNEL, flags=re.I):
                if re.search(PATTERN, CHANNEL) != None:
                    GROUPNAMEBF = match.group(1)
                    CHANNEL = re.sub(match.group(1), 'Music', match.group(0), flags=re.I)
                    GROUPNAME = re.search(PATTERN, CHANNEL).group(1)
                    if (GROUPNAME != None) and (GROUPNAME != GROUPNAMEBF):
                        print("Groupname of Channel " + re.search(PATTERN, CHANNEL).group(2) + " renamed from " + GROUPNAMEBF + " to " + GROUPNAME)
            if re.findall('.*Pluto.*', CHANNEL, flags=re.I|re.M):
                if re.search(PATTERN, CHANNEL) != None:
                    GROUPNAMEBF = match.group(1)
                    CHANNEL = re.sub(match.group(1), 'Pluto', match.group(0), flags=re.I)
                    GROUPNAME = re.search(PATTERN, CHANNEL).group(1)
                    if (GROUPNAME != None) and (GROUPNAME != GROUPNAMEBF):
                        print("Groupname of Channel " + re.search(PATTERN, CHANNEL).group(2) + " renamed from " + GROUPNAMEBF + " to " + GROUPNAME)

            if re.search(PATTERN,CHANNEL) != None:
                # COMPARE IF CHANNEL NAME AND LINK ALREAD EXISTS
                if re.search(PATTERN, CHANNEL).group(2) and re.search(PATTERN, CHANNEL).group(3) in MERGECHANNELS:
                    print("Channel " + re.search(PATTERN, CHANNEL).group(2) + " -> already exists...")
                    SORTCOUNT = SORTCOUNT + 1
                    SOCOUNT = SORTCOUNT / (i+1)
                # IF NO WRITE ACTUAL MATCH IN MERGEFILE.
                # FIRST ROUND USES ORIGINAL CHANNEL NAMES.
                # SECOND ROUND USES CHANNEL NAMES WITHOUT HD, FHD, 360p..., GEO-BLOCKED TAGS
                else:
                    with open('m3u_merge_'+str(i)+'.m3u','a', encoding='utf-8') as MERGEFILE:
                        MERGECOUNT = MERGECOUNT + 1
                        MECOUNT = MERGECOUNT / (i+1)
                        MERGEFILE.write(CHANNEL)
    # USE LAST ROUND AS INPUT
    INPUTFILE = open('m3u_merge_'+str(i)+'.m3u')
    CHANNELS = INPUTFILE.read()

INPUTFILE = open('m3u_merge_'+str(i)+'.m3u')
CHANNELS = INPUTFILE.read()

#SPLIT M3U FILE IN FILES BY GROUP
print("----------------------------------------------")
print("Spliting " + args.M3UINPUT)
print("----------------------------------------------")
for match in PATTERN.finditer(CHANNELS):

    CHANNEL = re.search(PATTERN, match.group(0))
    GROUPNAME = match.group(1).title()
    CHANNEL = re.sub(match.group(1), GROUPNAME.title(), match.group(0), flags=re.I|re.M)

    # GENERATE FILENAME FROM GROUPNAME
    if GROUPNAME:
        FILENAME = GROUPNAME + ".m3u"
        FILENAME = string.capwords(FILENAME)
    else: FILENAME = "m3u_emptygroup.m3u"

    # CHECK LINE 1 IF #EXTM3U EXISTS
    if os.path.exists(FILENAME):
        with open(FILENAME,'r', encoding='utf-8') as OUTPUTFILE:
            CONTENT = OUTPUTFILE.read()
            FIRST = CONTENT.split('\n', 1)[0]
            if '#EXTM3U' != FIRST:
                print(FILENAME + " -> #EXTM3U does not exists -> insert in line 1")
                with open(FILENAME+'.tempfile','w', encoding='utf-8') as t:
                    t.write('#EXTM3U\n' + CONTENT)
                os.rename(FILENAME+'.tempfile', FILENAME)

    # WRITING CHANNEL TO FILE
    with open(FILENAME,'a', encoding='utf-8') as OUTPUTFILE:
        CHANNEL = match.group(0)
        OUTPUTFILE.write(CHANNEL)

print("----------------------------------------------")
print("finished: ", args.M3UINPUT, " -> channels: ", int(CHCOUNT), " -> merged: ", int(MECOUNT), " -> sorted out: ", int(SOCOUNT))
TIMEEND = datetime.datetime.utcnow()
print(int((TIMEEND - TIMESTART).total_seconds()))
