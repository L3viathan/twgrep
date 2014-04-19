#!/usr/bin/env python3
"""twgrep — search for tweets matching a specific pattern

What grep is for arbitrary text, and Tgrep2 is for syntax trees, twgrep aims to be for tweet archives.

Usage:
	twgrep.py [-t|-a] [-1cvs] [--client=<client>] [--in-reply-to=<user_replied_to>] [--mentioning=<mentioned_user>] [--timestamp=<timestamp>] [--path=<path-to-tweets>] [<keywords>...]
	twgrep.py -r [-t|-a] [-1cvs] [--client=<client>] [--in-reply-to=<user_replied_to>] [--mentioning=<mentioned_user>] [--timestamp=<timestamp>] [--path=<path-to-tweets>] <pattern>
	twgrep.py (-h | --help)
	twgrep.py --version
	twgrep.py [-t1cvas] -I

Options:
	-h --help                        Show this help screen
	--version                        Show version number
	--path=<path-to-tweets>          Path of the tweet archive [default: ./]
	--client=<client>                Search in client name
	--in-reply-to=<user_replied_to>  Search for tweets in reply to
	                                 specific user
	--mentioning=<mentioned_user>    Search for tweets mentioning
	                                 specific user
	--timestamp=<timestamp>          Search in timestamp
	-s                               Search case-sensitive
	-v                               invert matches
	-t                               Pretty-print
	-a                               Show complete tweet data
	-1                               Show only first result
	-c                               Show count

"""

from docopt import docopt

import glob
import json
import sys
import re

args=docopt(__doc__,version="twgrep v0.2.1")

if args['-s']:
	modifier = lambda x: x
else:
	modifier = str.lower

if args['-v']:
	all_or_none = lambda x: not any(x)
else:
	all_or_none = all

if args['-r']:
	regex = re.compile(args['<pattern>'])

count=0

for f in glob.glob("*.js"):
	for tweet in reversed(json.loads(open(f).read()[32:])):
		if (not args['-r'] and all_or_none(modifier(word) in modifier(tweet["text"]) for word in args['<keywords>'])) or args['-r'] and regex.match(tweet["text"]):
			if args['--client'] and args['--client'].lower() not in tweet.get("source","").lower():
				continue
			if args['--in-reply-to'] and args['--in-reply-to'].lower() != tweet.get('in_reply_to_screen_name',"").lower():
				continue
			if args['--mentioning'] and args['--mentioning'].lower() not in map(str.lower,tweet.get('user_mentions')):
				continue
			if args['--timestamp'] and args['--timestamp'].lower() not in tweet.get("created_at","").lower():
				continue
			
			if args['-t']:
				print("\nhttps://twitter.com/"+tweet["user"]["screen_name"]+"/status/"+tweet["id_str"]," – ",tweet["created_at"]+":\n"+tweet["text"])
			elif args['-a']:
				print(tweet)
			else:
				print(tweet["text"])

			count += 1

			if args['-1']: # print only first match
				sys.exit(0)

print("Total matches:",count)
