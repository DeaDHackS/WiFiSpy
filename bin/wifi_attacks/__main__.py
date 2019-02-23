#!/usr/bin/env python3
from datetime import datetime
from scapy.all import srp,Ether,ARP,conf
import os
import socket
import sys
import random
import time
import threading
import subprocess

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

ATTACK_MODE = "none"

def main():
    print("[*] Choose what script to load?")
    print("\n * Wireless Cracking Attack *")
    print("  c1: 4-Ways-Handshake-Capture    - Automated WPA / WEP Handshake Capturing Attack Module")
    print("  c2: Evil-Twin Attack            - Coming in V.2!\n")
    print(" * Wireless Attacks *")
    print("  a1: Deauth Attack               - Deauth (Connection Jammer) Attack Module")
    print("  a2: WiFi Jammer                 - WiFi Deauth (WiFi Jammer) Attack Module\n")
    print(" * Wireless Info *")
    print("  i1: WiFi / AP Scanner           - AP (WiFi) Scanner\n")
    script2load = input(color.UNDERLINE+color.CYAN+"WiFiSpy"+color.END+"::"+color.UNDERLINE+color.CYAN+"root"+color.END+" ["+color.CYAN+color.UNDERLINE+"LOAD_WIRELESS_SCRIPT"+color.END+"] +> ")

    

    if script2load == "c1":
        os.system("cd mains && python3 wpa_capture_main.py")
   
    elif script2load == "a1":
        os.system("cd mains && python3 deauth_main.py")
   
    elif script2load == "a2":
        os.system("cd mains && python3 wifi_jammer_main.py")
   
    elif script2load == "i1":
        os.system("cd mains && python3 ap_scanner_main.py")
    
    else:
        WARNING_print("Option is not valid! Please select another one")
        main()


main()
