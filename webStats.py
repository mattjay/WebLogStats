#!/usr/bin/env python

# Copyright (c) 2015, Matt Johansen
# All rights reserved.
 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
 
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""Python script to parse through a Web log file and return the number of requests and unique IPs in a given time period"""

import sys
import fileinput
import re
import time
import datetime
import optparse
from collections import Counter

__version__ = '1.0.1'
__author__ = 'Matt Johansen <@mattjay>'
__license__ = 'BSD'

desc = "Python script to parse through a Web log file and return the number of requests and unique IPs in a given time period. It takes an Apache log file via stdin, the number of hours back you'd like to look -t (Default = 24 hours), and if you want the actual list of unique IPs -i"
parser = optparse.OptionParser(description=desc)
parser.add_option('-t', help='number of hours back you want to look', dest='hours', default=24, type=int, action='store')
parser.add_option('-i', '--ips', help='shows list of unique IPs', dest='bool', default=False, action='store_true')
parser.add_option('-n', help='List the n most common IPs to visit in the given time period', dest='ips', default=0, type=int, action='store')
parser.add_option('-f', '--files', help='list of web log file paths', dest='files', type='string', action='store')
(opts, args) = parser.parse_args()

filenames = [x.strip() for x in opts.files.split(',')]

hoursAgo = datetime.datetime.today() - datetime.timedelta(hours = opts.hours)
apacheHoursAgo = hoursAgo.strftime('%d/%b/%Y:%H:%M:%S')
t2 = time.strptime(apacheHoursAgo.split()[0], '%d/%b/%Y:%H:%M:%S')
d2 = datetime.datetime(*t2[:6])

requests = []
ips = Counter()

for f in filenames:
	with open(f) as fi:
		for line in fi:
			m = map(''.join, re.findall(r'\"(.*?)\"|\[(.*?)\]|(\S+)', line))
			if m != None:
				t1 = time.strptime(m[3].split()[0], '%d/%b/%Y:%H:%M:%S')
				d1 = datetime.datetime(*t1[:6])
				if d1 > d2:
					requests.append(d1)
					ips[m[0]] += 1

try:
	from pyfiglet import Figlet
	fig = Figlet()
	print(fig.renderText("Web Log Stats"))
except ImportError:
	print "Install pyfiglet for a (useless) pretty cool header!"

print "Total Unique IP Addresses Since", d2, " :   ", len(ips)
print "Total Requests Since", d2, "            :   ", len(requests)
if opts.bool == True:
	print "Unique Ips Since", d2, "                :   ", ips.keys()
if opts.ips > 0:
	print "Top", opts.ips, "Visitor(s) :", ips.most_common(opts.ips)
	try:
		from ascii_graph import Pyasciigraph
		graph = Pyasciigraph()
		for line in graph.graph("Most Common Ips", ips.most_common(opts.ips)):
			print line
	except ImportError:
		print "Install ascii_graph for a cool graph!"
