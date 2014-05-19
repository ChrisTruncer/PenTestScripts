#!/usr/bin/python

# Quick script that attempts to find the reverse DNS info
# from a provided IP range.

import argparse
import os
import socket
import sys
from netaddr import IPNetwork


def cli_parser():

    # Command line argument parser
    parser = argparse.ArgumentParser(
        add_help=False,
        description="DNSReverser takes IP addresses and tries to find its hostname.")
    parser.add_argument(
        "-f", metavar="ips.txt", default=None,
        help="File containing IPs to resolve hostnames for.")
    parser.add_argument(
        "-ip", metavar='192.168.1.1', default=None,
        help="Used to find hostname about a specific IP.")
    parser.add_argument(
        "-cidr", metavar='192.168.1.0/24', default=None,
        help="Used to find hostnames about a specific CIDR range.")
    parser.add_argument(
        '-h', '-?', '--h', '-help', '--help', action="store_true",
        help=argparse.SUPPRESS)
    args = parser.parse_args()

    if args.h:
        parser.print_help()
        sys.exit()

    return args.f, args.ip, args.cidr


def rdns_lookup(ip_address):

    try:
        # Get the reverse dns name if it exists
        reverse_dns = socket.gethostbyaddr(ip_address)[0]
        script_out = ip_address.strip() + ' ' + reverse_dns + '\n'
        with open('reverse_dns_results.txt', 'a') as rev_results:
            rev_results.write(script_out)
    except:
        print "No Reverse DNS for " + str(ip_address) + "."

    return


def cidr_net(cidr_range):
    net_1 = IPNetwork(cidr_range)

    return net_1


def file_read(input_file):
    with open(input_file, 'r') as f:
        ip_file = f.readlines()

    return ip_file


def title():
    # Clear the screen
    os.system('clear')

    print "############################################################"
    print "#                    Reverse DNS Scanner                   #"
    print "############################################################\n"
    print "Starting Reverse DNS Scan...\n"

    return


if __name__ == '__main__':

    # Parse command line options
    cli_file, cli_ip, cli_cidr = cli_parser()

    title()

    if cli_cidr is not None and cli_file is None and cli_ip is None:
        ip_cidr_list = cidr_net(cli_cidr)
        for ip_add in ip_cidr_list:
            ip_add = str(ip_add)
            ip_add = ip_add.strip()
            rdns_lookup(ip_add)

    elif cli_file is not None and cli_cidr is None and cli_ip is None:
        ip_file_input = file_read(cli_file)
        for ip_add_file in ip_file_input:
            ip_add_file = ip_add_file.strip()
            rdns_lookup(ip_add_file)

    elif cli_ip is not None and cli_cidr is None and cli_file is None:
        rdns_lookup(cli_ip)

    else:
        print "[*]ERROR: Please start over and provide a valid input option."
        sys.exit()

    print "\nScan Completed! Check the output file!\n"
