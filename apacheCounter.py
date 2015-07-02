#!/usr/bin/env python

# Copyright (c) 2015, Matthew Johansen
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""Python script to parse through an Apache log file and return the number of requests and unique IPs in a given time period"""

import sys
import re
import time
import datetime
import optparse
from collections import Counter

__version__ = '1.0.1'
__author__ = 'Matt Johansen <@mattjay>'
__license__ = 'MIT'

desc = "Python script to parse through an Apache log file and return the number of requests and unique IPs in a given time period. It takes an Apache log file via stdin, the number of hours back you'd like to look -t (Default = 24 hours), and if you want the actual list of unique IPs -i"
parser = optparse.OptionParser(description=desc)
parser.add_option('-i', '--ips', help='shows list of unique IPs', dest='bool', default=False, action='store_true')
parser.add_option('-t', help='number of hours back you want to look', dest='hours', default=24, type=int, action='store')
parser.add_option('-n', help='List the n most common IPs to visit in the given time period', dest='ips', default=0, type=int, action='store')
(opts, args) = parser.parse_args()

apacheLog = sys.stdin

hoursAgo = datetime.datetime.today() - datetime.timedelta(hours = opts.hours)
apacheHoursAgo = hoursAgo.strftime('%d/%b/%Y:%H:%M:%S')
t2 = time.strptime(apacheHoursAgo.split()[0], '%d/%b/%Y:%H:%M:%S')
d2 = datetime.datetime(*t2[:6])

requests = []
ips = Counter()

for line in apacheLog:
	m = map(''.join, re.findall(r'\"(.*?)\"|\[(.*?)\]|(\S+)', line))
	if m != None:
		t1 = time.strptime(m[3].split()[0], '%d/%b/%Y:%H:%M:%S')
		d1 = datetime.datetime(*t1[:6])
		if d1 > d2:
			requests.append(d1)
			#ips.append(m[0])
			ips[m[0]] += 1

print "Total Unique IP Addresses Since", d2, " :   ", len(ips)
print "Total Requests Since", d2, "            :   ", len(requests)
if opts.bool == True:
	print "Unique Ips Since", d2, "                :   ", ips.keys()
if opts.ips > 0:
	print "Top", opts.ips, "Visitor(s) :", ips.most_common(opts.ips)
