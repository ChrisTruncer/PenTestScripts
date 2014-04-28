#!/usr/bin/env python
# IP sort and uniquing script by @ChrisTruncer

import os
import sys

try:
    # Take filename as first argument
    ip_file = sys.argv[1]
except IndexError:
    # Clear the console
    os.system('clear')
    print "#####################################################################"
    print "#                             IP Sorter                             #"
    print "#####################################################################\n"
    print "[*] ERROR: Please provide a file containing IPs to be uniqued \
        and sorted!\n".replace('    ', '')
    print "Example: ./IPSorter.py ips.txt"
    sys.exit()

# Read in all IPs from user specified file
with open(ip_file, 'r') as open_file:
    ips = open_file.readlines()

# Convert to a set to remove duplicates, then convert to list
ips = list(set(ips))

# This came from http://www.secnetix.de/olli/Python/tricks.hawk#sortips
for i in range(len(ips)):
    ips[i] = "%3s.%3s.%3s.%3s" % tuple(ips[i].split("."))

# Use built in sort method
ips.sort()

# Replace all the spaces in our list
for i in range(len(ips)):
    ips[i] = ips[i].replace(" ", "")
    print ips[i].strip()
