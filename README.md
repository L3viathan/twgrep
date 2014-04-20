twgrep
======

Search through your tweets

What grep is for arbitrary text, and Tgrep2 is for syntax trees, twgrep aims to be for tweet archives.

`Usage:
	twgrep.py [-t|-a] [-1cvsd] [--format=<format>] [--client=<client>] [--in-reply-to=<user_replied_to>] [--mentioning=<mentioned_user>] [--timestamp=<timestamp>] [--path=<path-to-tweets>] [<keywords>...]
	twgrep.py -r [-t|-a] [-1cvsd] [--format=<format>] [--client=<client>] [--in-reply-to=<user_replied_to>] [--mentioning=<mentioned_user>] [--timestamp=<timestamp>] [--path=<path-to-tweets>] <pattern>
	twgrep.py (-h | --help)
	twgrep.py --version

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
	?id       ID`
