#!/usr/bin/python 3
import time
import sys
from scapy.all import *
import optparse
import subprocess
import time
import re

parser = optparse.OptionParser()

parser.add_option('-t', '--tool', dest='HS_CHECKER', type=str,  help='')
parser.add_option('-b', '--bssid', dest='BSSID', type=str,  help='')
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

TOOL = options.HS_CHECKER

os.chdir("tmp")

if TOOL == "aircrack-ng":
    while True:
        print("[*] Waiting 20 seconds for the next handshake checking ...")
        time.sleep(20)
        print("[+] Checking file using Aircrack-ng ...")
        out = subprocess.Popen(["aircrack-ng", "-J", "TEMP_HS", "{0}_CAPTURE-01.cap".format(options.BSSID)], encoding='utf8',         
           stdout=subprocess.PIPE, 
           stderr=subprocess.STDOUT)
        stdout,stderr = out.communicate()
        stdout = stdout.splitlines()
        if "Successfully written to TEMP_HS.hccap" in stdout:
            try:
                os.remove("TEMP_HS.hccap")
            except:
                pass
            f = open("HANDSHAKE_CAPTURED.SUCCESS", "w")
            f.write("Handshake captured")
            print("[+] Handshake captured!!")
            exit()
        else:
            print("[~] Handshake not found")
            try:
                os.remove("TEMP_HS.hccap")
            except:
                pass 

if TOOL == "pyrit":
    while True:
        print("[*] Waiting 20 seconds for the next handshake checking ...")
        time.sleep(20)
        print("[+] Checking file using Pyrit ...")
        out = subprocess.Popen(["pyrit", "-r", "{0}_CAPTURE-01.cap".format(options.BSSID), "analyze"], encoding='utf8',         
           stdout=subprocess.PIPE, 
           stderr=subprocess.STDOUT)
        stdout,stderr = out.communicate()
        if "handshake(s):" in stdout:
            f = open("HANDSHAKE_CAPTURED.SUCCESS", "w")
            f.write("Handshake captured")
            print("[+] Handshake captured!!")
            exit()
        else:
            print("[~] Handshake not found")
  
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

