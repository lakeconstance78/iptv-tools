# IPTV-Tools

A collection of scripts I'm using for a better IPTV experience.

m3usplitter - is a small python script to split a M3U file in multiple files by group

	python3 m3usplitter.py M3UFILE.M3U

The #EXTM3U tag will be added if it doesn't exist.
Channels without groups will be saved as "Emtygroups.m3u".
