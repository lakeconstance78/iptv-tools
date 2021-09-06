# IPTV-Tools

A collection of scripts I have created for a better IPTV experience.

m3usplitter - is a small python script to split a M3U file in multiple files by group

	python3 m3usplitter.py M3UFILE.M3U

The #EXTM3U tag will be added if it doesn't exist.
Channels without groups will be saved as "Emtygroups.m3u".


iptv-channels.bash - download and check multiple m3u files in an directory

	iptv-channels.bash

1.  Download my IPTV-channel collection from my playlist repository
	https://github.com/lakeconstance78/IPTV-channels
2.	Download m3u channel lists defined below
3.	Checks every links in all m3u channel lists and safe them under *_checked.
	The checking tool is used from https://github.com/FutureSharks/iptv-stream-cleaner	
