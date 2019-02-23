#!/usr/bin/env python3
from datetime import datetime
from scapy.all import srp,Ether,ARP,conf
import signal
from multiprocessing import Process
import os
import socket
import sys
import random
import time
import threading
import subprocess
from scapy.all import *

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

def ERROR_print(msg):
    print(color.END+"["+color.RED+"x"+color.END+"]"+color.RED+" "+msg+color.CYAN)

def WARNING_print(msg):
    print(color.END+"["+color.ORANGE+"WARNING"+color.END+"]"+color.ORANGE+" "+msg+color.CYAN)

def SUCCESS_print(msg):
    print(color.END+"["+color.LIGHTGREEN+"+"+color.END+"]"+color.LIGHTGREEN+" "+msg+color.CYAN)

def INFO_print(msg):
    print(color.END+"["+color.YELLOW+"INFO"+color.END+"]"+color.YELLOW+" "+msg+color.CYAN)

def OVER_print(msg):
    if msg == "none":
        sys.stdout.flush()
        sys.stdout.write(".")
    else:
        sys.stdout.write("\033[F") #back to previous line
        sys.stdout.write("\033[K") #clear line
        print(msg)

interface=''
nrml_ssid = ''
aps = {}
AP = []
channel = 0

def sniffAP(p):
    if ((p.haslayer(Dot11Beacon) or p.haslayer(Dot11ProbeResp)) and p[Dot11FCS].addr3 not in aps):
        ssid       = p[Dot11Elt].info
        nrml_ssid  = p[Dot11Elt].info if b'\x00' not in p[Dot11Elt].info and p[Dot11Elt].info != '' else 'Hidden SSID' 
        bssid      = p[Dot11FCS].addr3    
        channel    = int( ord(p[Dot11Elt:3].info))
        capability = p.sprintf("{Dot11Beacon:%Dot11Beacon.cap%}\
                {Dot11ProbeResp:%Dot11ProbeResp.cap%}") 
        if not ssid in AP:
            p = p[Dot11Elt]
            cap = p.sprintf("{Dot11Beacon:%Dot11Beacon.cap%}"
                       "{Dot11ProbeResp:%Dot11ProbeResp.cap%}").split('+')
            crypto = set()
            while isinstance(p, Dot11Elt):
                if p.ID == 0:
                    ssid = p.info
                elif p.ID == 3:
                    channel = ord(p.info)
                elif p.ID == 48:
                    crypto.add("WPA2")
                elif p.ID == 221 and p.info.startswith(b'\x00P\xf2\x01\x01\x00'):
                    crypto.add("WPA")
                p = p.payload
                if not crypto:
                    if 'privacy' in cap:
                        crypto.add("WEP")
                else:
                    crypto.add("OPN")
            if re.search("privacy", capability): enc = 'Y'
            else: enc  = 'N'
            AP.append(ssid)
            msg = color.CYAN+"{0:20}{1:20}{2:5}{3:5}{4:5}".format(nrml_ssid.decode("latin-1"), str(bssid), str(channel), str(enc), str(" / ".join(crypto)))+color.END
            OVER_print(msg)
            #msg = ""+color.CYAN+color.UNDERLINE+"{0}".format(nrml_ssid.decode("latin-1"))+color.END+color.CYAN+"{0:21}{1:20}{2:5}{3:5}{4:5}".format("", str(bssid), str(channel), str(enc), str(" / ".join(crypto)))+color.END
            #print(msg)            
            print("")
def channel_hopper(channel):
    while True:
        try:
            channel = int(channel)
            channel = int(channel) + 1
            if channel == 12:
                channel = 0
            else:
                os.system("iw dev %s set channel %d &> /dev/null" % (interface, channel))
                time.sleep(0.25)
                OVER_print("CH: "+str(channel))
                time.sleep(0.15)
        except KeyboardInterrupt:
            break
            exit()
def signal_handler(signal, frame):
    p.terminate()
    p.join()
    monitor_quest = input("[?] Would you like to stop monitor mode? [Y/N]: ".format(INTERFACE))
            
    if monitor_quest == "Y" or monitor_quest == "y":
       print("[*] Yes? Ok stopping monitor mode for you ...")
       NEW_INTERFACE = INTERFACE.replace("mon", "")
       monitor_quest = input(color.END+"[?] Is your normal adapter '{0}'? [Y/N]: ".format(NEW_INTERFACE))
       if monitor_quest == "Y" or monitor_quest == "y":
          os.system("airmon-ng stop {0} >/dev/null 2>&1 &".format(INTERFACE))
          os.system("service network-manager start >/dev/null 2>&1 &")
    OVER_print("") 
    sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage %s monitor_interface" % sys.argv[0])
        sys.exit(1)

    interface = sys.argv[1]

    # Print the program header
    print("[*] Do ctrl+c to stop scanner when you are done!")
    print("-=-=-=-=-=-= "+color.CYAN+color.UNDERLINE+"WiFiSpy"+color.END+" AP "+color.CYAN+color.UNDERLINE+"Scan "+color.END+"=-=-=-=-=-=-")
    print("{0:20}{1:20}{2:5}{3:5}{4:5}".format("ESSID", "BSSID", "CH", "ENC?", "SECURITY"))
    print(".")

    # Start the channel hopper
    p = Process(target=channel_hopper, args=(str(channel),))
    p.start()

    # Capture CTRL-C
    signal.signal(signal.SIGINT, signal_handler)

    # Start the sniffer
    sniff(iface=interface, prn=sniffAP)
