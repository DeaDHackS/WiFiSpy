#!/usr/bin/python 3
import time
import sys
from scapy.all import *
import optparse
import subprocess
import os

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

INTERFACE = options.INTERFACE
BSSID = options.BSSID
CHANNEL = options.CHANNEL

os.chdir("tmp")

p = subprocess.Popen("airodump-ng {0} --bssid {1} -c {2} --write {3}_CAPTURE".format(INTERFACE, BSSID, CHANNEL, BSSID), encoding='utf8', shell=True, stderr=subprocess.PIPE)  
while True:
    try:
        out = p.stderr.read(1)
        if os.path.isfile("HANDSHAKE_CAPTURED.SUCCESS"):
            exit()
        if out == '' and p.poll() != None:
            break
        if out != '':
            sys.stdout.write(out)
            #sys.stdout.flush()
    except KeyboardInterrupt:
        pass
        break
        exit()
