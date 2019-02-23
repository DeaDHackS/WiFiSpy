#!/usr/bin/env python3
from datetime import datetime
from scapy.all import srp,Ether,ARP,conf
import os
import socket
import sys
import random

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

def RANDOM_MAC():
    return "%02x:%02x:%02x:%02x:%02x:%02x" % (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255)
        )

def SCAN_NETWORK(MAC_ADDRESS, IP_RANGE, INTERFACE):
    print("[+] Scanning network ... \n")
    start_time = datetime.now() 
    conf.verb = 0
    if MAC_ADDRESS == "None":
        ans, unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst = IP_RANGE), timeout = 2,   iface=INTERFACE,inter=0.1)
    else:
        ans, unans = srp(Ether(src=MAC_ADDRESS, dst="ff:ff:ff:ff:ff:ff")/ARP(pdst = IP_RANGE), timeout = 2,   iface=INTERFACE,inter=0.1)
    for snd,rcv in ans:
        try:
            hostname = socket.gethostbyaddr(str(rcv[ARP].psrc))[0]
            print(rcv.sprintf(r"%ARP.psrc% ["+color.CYAN+color.UNDERLINE+hostname+color.END+"] - %Ether.src%"))
        except: 
            ERROR_print("Error occured while scanning!")
            MAIN(IP_RANGE, SPOOF_MAC, INTERFACE)
    stop_time = datetime.now()
    total_time = stop_time - start_time 
    print("\n")
    print("[*] Module Completed!")
    print("[*] Scan Duration: %s \n" %(total_time))

IP_RANGE = "Unset"
SPOOF_MAC = False
INTERFACE = "Unset"
MAC_ADDRESS = ""

def MAIN(IP_RANGE, SPOOF_MAC, INTERFACE, MAC_ADDRESS):
    while True:
        try:
            cmd_term = input(color.UNDERLINE+color.CYAN+"WiFiSpy"+color.END+"::"+color.UNDERLINE+color.CYAN+"root"+color.END+" ["+color.CYAN+color.UNDERLINE+"network_scan"+color.END+"] +> ")
            if cmd_term == "?" or cmd_term == "help":
                print(r"""
* Description *
    Scan subnet (IP RANGE) and see which hosts are reachable then gather info as hostname, mac address and local ip
    
* WiFiSpy Commands *
    ? - help             <*>    this menu
    back                 <*>    back to main menu
    credits              <*>    shows WiFiSpy credits
    version              <*>    displays exact version
    clear                <*>    clear screen

* Network Scan Commands *
    options              <*>    show current configurations / options
    set <option> <value> <*>    set options to the given value
    start                <*>    start network scan
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
IP_RANGE      Yes       {0}
INTERFACE     Yes       {1}
""".format(IP_RANGE, INTERFACE))

            if "set" in cmd_term:
                CLEANED = cmd_term.replace("set ", "")
                ARGS = CLEANED.split()

                try:
                    if not ARGS[0]:
                        CHECK_ARG = "check"
                except:
                    pass
                    ERROR_print("Please give an option!")
                    MAIN(IP_RANGE, SPOOF_MAC, INTERFACE. MAC_ADDRESS)

                try:
                    if not ARGS[1]:
                        CHECK_ARG = "check"
                except:
                    pass
                    ERROR_print("Please give an value!")
                    MAIN(IP_RANGE, SPOOF_MAC, INTERFACE, MAC_ADDRESS)

                if ARGS[0] == "IP_RANGE":
                    IP_RANGE = ARGS[1]
                    print("IP_RANGE => {0}".format(IP_RANGE))

                elif ARGS[0] == "INTERFACE":
                    INTERFACE = ARGS[1]
                    print("INTERFACE => {0}".format(INTERFACE))
                
                else:
                    ERROR_print("'{0}' is not a valid option!".format(ARGS[0]))

            if cmd_term == "start":
                MAC_ADDRESS = "None"
                SCAN_NETWORK(MAC_ADDRESS, IP_RANGE, INTERFACE)        

            if "show_info" in cmd_term:  
                CLEANED = cmd_term.replace("show_info ", "")
                ARGS = CLEANED.split()
                 
                try:
                    if not ARGS[0]:
                        CHECK_ARG = "check"
                except:
                    pass
                    ERROR_print("Please give an option!")
                    MAIN(IP_RANGE, SPOOF_MAC, INTERFACE. MAC_ADDRESS)
                
                if ARGS[0] == "IP_RANGE":
                    print("The subnet to scan, example: if my local IP is 192.168.1.164, my IP_RANGE would be: 192.168.1.0/24")
               
                elif ARGS[0] == "INTERFACE":
                    print("The interface to use, example: do ifconfig (on linux) to see all your adapters, by default its something like wlan0 or wlan1.")

                else:
                    ERROR_print("'{0}' is not a valid option!".format(ARGS[0]))

        except KeyboardInterrupt:
            ERROR_print("\nWiFiSpy is now quitting, bye-bye ...")
            exit()
MAIN(IP_RANGE, SPOOF_MAC, INTERFACE, MAC_ADDRESS)
