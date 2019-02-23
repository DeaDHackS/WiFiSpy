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
    
INTERFACE = "Unset"
BSSID = "Unset"
TARGET_MAC = "Unset"
CHANNEL = "0"

def MAIN(INTERFACE, BSSID, TARGET_MAC, CHANNEL):
    while True:
        try:
            cmd_term = input(color.UNDERLINE+color.CYAN+"WiFiSpy"+color.END+"::"+color.UNDERLINE+color.CYAN+"root"+color.END+" ["+color.CYAN+color.UNDERLINE+"deauth_attack"+color.END+"] +> ")
            
            if cmd_term == "?" or cmd_term == "help":
                print(r"""
* Description *
    Sends deauth packet to client on a specific WiFi (BSSID) to jam its traffic
    
* WiFiSpy Commands *
    ? - help             <*>    this menu
    back                 <*>    back to main menu
    credits              <*>    shows WiFiSpy credits
    version              <*>    displays exact version
    clear                <*>    clear screen

* Deauth Attack Commands *
    options              <*>    show current configurations / options
    set <option> <value> <*>    set options to the given value
    start                <*>    start deauth attack
    show_info <options>  <*>    show description of a configuration / options
            """)

            if cmd_term == "back":
                exit()
             
            if cmd_term == "credits":
                print("Credits: ")
                print("Main Developer: Ghosty / DeaDHackS Team ")
                print("Who Coded This Module?: Ghosty / DeaDHackS Team ")
                print("With?: No one ")
             
            if cmd_term == "version":
                print("1.0 - First version ever made!")
             
            if cmd_term == "clear":
                if "nt" in os.name:
                    os.system("cls")
                else:
                    os.system("clear") 
                    
            if cmd_term == "options":
                print("""

OPTION        REQUIRED  VALUE
============= ========= ============
INTERFACE     Yes       {0}
BSSID         Yes       {1}
TARGET_MAC    Yes       {2}
CHANNEL       Yes       {3}

""".format(INTERFACE, BSSID, TARGET_MAC, CHANNEL))

            if "set" in cmd_term:
                CLEANED = cmd_term.replace("set ", "")
                ARGS = CLEANED.split()

                try:
                    if not ARGS[0]:
                        CHECK_ARG = "check"
                except:
                    pass
                    ERROR_print("Please give an option!")
                    MAIN(INTERFACE, BSSID, TARGET_MAC, CHANNEL)

                try:
                    if not ARGS[1]:
                        CHECK_ARG = "check"
                except:
                    pass
                    ERROR_print("Please give an value!")
                    MAIN(INTERFACE, BSSID, TARGET_MAC, CHANNEL)

                    
                if ARGS[0] == "INTERFACE":
                    INTERFACE = ARGS[1]
                    print("INTERFACE => {0}".format(INTERFACE))
                    
                elif ARGS[0] == "BSSID":
                    BSSID = ARGS[1]
                    print("BSSID => {0}".format(BSSID))
                    
                elif ARGS[0] == "TARGET_MAC":
                    print("[+] TIP: You can add more tham 1 target by doing so: set TARGET FF:FF:FF:FF:FF:FF,AA:AA:AA:AA:AA:AA")
                    TARGET_MAC = ARGS[1]
                    print("TARGET_MAC => {0}".format(TARGET_MAC))
               
                elif ARGS[0] == "CHANNEL":
                    CHANNEL = ARGS[1]
                    print("CHANNEL => {0}".format(CHANNEL))
                
                else:
                    ERROR_print("'{0}' is not a valid option!".format(ARGS[0]))

            if cmd_term == "start":
                monitor_quest = input("[?] Is your interface ({0}) already in monitor mode? [Y/N]: ".format(INTERFACE))
                
                if not monitor_quest == "Y" or not monitor_quest == "y":
                monitor_quest = input("[?] Is your interface ({0}) already in monitor mode? [Y/N]: ".format(INTERFACE))
                
                if not monitor_quest == "Y" or not monitor_quest == "y":
                    print("[*] No? Ok starting monitor mode for you ...")
                    os.system("airmon-ng start {0} >/dev/null 2>&1 &".format(INTERFACE))
                    print("[*] Killing error-causing proccess ...")
                    os.system("airmon-ng check kill >/dev/null 2>&1 &")
                    print("[*] Done!")
                    INFO_print("You can do 'ifconfig' in a terminal, to see all your adapters!")
                    monitor_quest = input(color.END+"[?] Is your new adapter '{0}mon'? [Y/N]: ".format(INTERFACE))
                    if monitor_quest == "Y" or monitor_quest == "y":
                        INTERFACE = INTERFACE+"mon"
                        print("[+] Ok good, starting module ...")
                    else:
                        monitor_quest = input("[?] Oh? Really? Please specifiy your new adapter: ")
                        INTERFACE = monitor_quest
                        
                os.system("cd ../ && python3 deauth_attack.py -i {0} -b {1} -t {2} -c {3}".format(INTERFACE, BSSID, TARGET_MAC, CHANNEL))        

            if "show_info" in cmd_term:  
                CLEANED = cmd_term.replace("show_info ", "")
                ARGS = CLEANED.split()
                 
                try:
                    if not ARGS[0]:
                        CHECK_ARG = "check"
                except:
                    pass
                    ERROR_print("Please give an option!")
                    MAIN(INTERFACE, BSSID, TARGET_MAC, PACKET, CHANNEL)
               
                if ARGS[0] == "INTERFACE":
                    print("The interface to use, example: do ifconfig (on linux) to see all your adapters, by default its something like wlan0 or wlan1.")

                else:
                    ERROR_print("'{0}' is not a valid option!".format(ARGS[0]))

        except KeyboardInterrupt:
            ERROR_print("\nWiFiSpy is now quitting, bye-bye ...")
            exit()
MAIN(INTERFACE, BSSID, TARGET_MAC, CHANNEL)

