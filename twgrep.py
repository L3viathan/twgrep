#!/usr/bin/env python3
"""twgrep — search for tweets matching a specific pattern

What grep is for arbitrary text, and Tgrep2 is for syntax trees, twgrep aims to be for tweet archives.

Usage:
	twgrep.py [-t|-a] [-1cvsd] [--format=<format>] [--client=<client>]
	          [--in-reply-to=<user_replied_to>] [--mentioning=<mentioned_user>]
	          [--timestamp=<timestamp>] [--path=<path-to-tweets>] [<keywords>...]
	twgrep.py -r [-t|-a] [-1cvsd] [--format=<format>] [--client=<client>]
	          [--in-reply-to=<user_replied_to>] [--mentioning=<mentioned_user>]
	          [--timestamp=<timestamp>] [--path=<path-to-tweets>] <pattern>
	twgrep.py (-h | --help | --version)

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
	-s                               Search case-sensitive (applies only
		                             to tweet text)
	-v                               invert matches
	-t                               Pretty-print
	-a                               Show complete tweet data
	-1                               Show only first result
	-c                               Show count
	-r                               Regex mode (applies only to tweet text)
	-d                               Print docopt debug information

Output format:
	When using --format, you can provide an arbitrary string containing special character sequences, which will be replaced while printing. A list of possible special characters is given here:

	?user     Username
	?name     Full name
	?text     Tweet text
	?time     Timestamp
	?id       ID
	
"""

from docopt import docopt

import glob
import json
import sys
import re

def replaceDict(string, dictionary):
	#naive version:
	for key in dictionary:
		string = string.replace(key,dictionary[key])
	return string

args=docopt(__doc__,version="twgrep v0.2.3")

if args['-d']:
	print("DOCOPT args:\n\n",args,"\n")

if args['-s']:
	modifier = lambda x: x # case-sensitive: do not change 
else:
	modifier = str.lower

if args['-v']:
	all_or_none = lambda x: not any(x) # "not any" = "none"
	negate_maybe = lambda x: not x
else:
	all_or_none = all
	negate_maybe = lambda x: x

if args['-r']:
	regex = re.compile(args['<pattern>']) # compile for performance

count=0

for f in glob.glob("*.js"):
	for tweet in reversed(json.loads(open(f).read()[32:])):
		# either not regex mode and all/none of the words are in the text, or regex mode and pattern matches (or doesn't, if -v)
		if (not args['-r'] and all_or_none(modifier(word) in modifier(tweet["text"]) for word in args['<keywords>'])) or args['-r'] and negate_maybe(regex.search(tweet["text"])):
			if args['--client'] and negate_maybe(args['--client'].lower() not in tweet.get("source","").lower()):
				continue
			if args['--in-reply-to'] and negate_maybe(args['--in-reply-to'].lower() != tweet.get('in_reply_to_screen_name',"").lower()):
				continue
			if args['--mentioning'] and negate_maybe(args['--mentioning'].lower() not in map(str.lower,tweet.get('user_mentions'))):
				continue
			if args['--timestamp'] and negate_maybe(args['--timestamp'].lower() not in tweet.get("created_at","").lower()):
				continue
			
			if args['-t']:
				print("\nhttps://twitter.com/"+tweet["user"]["screen_name"]+"/status/"+tweet["id_str"]," – ",tweet["created_at"]+":\n"+tweet["text"])
			elif args['-a']:
				print(tweet)
			elif args['--format']: #print custom format.
				replacements = {
					"?user": tweet["user"]["screen_name"],
					"?text": tweet['text'],
					"?time": tweet['created_at'],
					"?id": tweet['id_str'],
					"?client": tweet['source'],
					"?name": tweet['user']['name']
				}
				print(replaceDict(args['--format'],replacements))
			else:
				print(tweet["text"])

			count += 1

			if args['-1']: # print only first match
				sys.exit(0)

if args['-c']:
	print("Total matches:",count)
