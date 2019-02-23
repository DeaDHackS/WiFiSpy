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

def START_DNS_SNIFF(TARGETS, GATEWAY, INTERFACE):
    os.system("python3 dns_query_sniffer.py -t {0} -g {1} -i {2}".format(TARGETS, GATEWAY, INTERFACE))

def START_HTTP_SNIFF(TARGETS, GATEWAY, INTERFACE):
    os.system("python3 http_sniffer.py -t {0} -g {1} -i {2}".format(TARGETS, GATEWAY, INTERFACE))

def SNIFF_NETWORK(DNS_SNIFF, HTTP_SNIFF, TARGETS, GATEWAY, INTERFACE):
    print("[+] Loading sniffers ...")
    time.sleep(2)
    if DNS_SNIFF == True:
        print("[+] Created DNS_SNIFF.thread ...")
        DNS_SNIFFER = threading.Thread(target=START_DNS_SNIFF, args=(TARGETS, GATEWAY, INTERFACE))
        DNS_SNIFFER.setDaemon(True)
        
    if HTTP_SNIFF == True:
        print("[+] Created HTTP_SNIFF.thread ...")
        HTTP_SNIFFER = threading.Thread(target=START_HTTP_SNIFF, args=(TARGETS, GATEWAY, INTERFACE))
        HTTP_SNIFFER.setDaemon(True)
    
    print("[+] Beginning sniff ... against {0}".format(TARGETS))
    if DNS_SNIFF == True:
        DNS_SNIFFER.start()
    if HTTP_SNIFF == True:
        HTTP_SNIFFER.start() 
    try:
        while True:
            RANDOM = input(color.UNDERLINE+color.CYAN+"CURRENTLY SNIFFING ... \n"+color.END) 
    except KeyboardInterrupt:
        print("\n[+] Killing .thread(s) ...")
        yousure = input("[?] To properly quit, we need to kill all python scripts except this one. Can we safely do it? [Y]es / [N]o: ")
        for proc in subprocess.check_output(['ps', '-ef']).split('\n'):
           if 'python' in proc and __name__+".py" not in proc:
               os.kill(proc)
    
    

DNS_SNIFF = False
HTTP_SNIFF = False
TARGETS = "Unset"
GATEWAY = "Unset"
INTERFACE = "Unset"

def MAIN(DNS_SNIFF, HTTP_SNIFF, TARGETS, GATEWAY, INTERFACE):
    while True:
        try:
            cmd_term = input(color.UNDERLINE+color.CYAN+"WiFiSpy"+color.END+"::"+color.UNDERLINE+color.CYAN+"root"+color.END+" ["+color.CYAN+color.UNDERLINE+"network_sniffer"+color.END+"] +> ")
            
            if cmd_term == "?" or cmd_term == "help":
                print(r"""
* Description *
    - DNS QUERY SNIFF -
         Sniffs DNS requests and gather resolved domain
     
    - HTTP TRAFFIC SNIFF - 
         Sniffs HTTP requests and gather informations from it as cookies, full link, logins, post/get data
    
* WiFiSpy Commands *
    ? - help             <*>    this menu
    back                 <*>    back to main menu
    credits              <*>    shows WiFiSpy credits
    version              <*>    displays exact version
    clear                <*>    clear screen

* Network Sniff Commands *
    options              <*>    show current configurations / options
    set <option> <value> <*>    set options to the given value
    start                <*>    start sniffing
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
DNS_SNIFF     Yes       {0}
HTTP_SNIFF    Yes       {1}
TARGET        Yes       {2}
GATEWAY       Yes       {3}
INTERFACE     Yes       {4}

""".format(str(DNS_SNIFF), str(HTTP_SNIFF), TARGETS, GATEWAY, INTERFACE))

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

                if ARGS[0] == "DNS_SNIFF":
                    if ARGS[1] == "True":
                        DNS_SNIFF = True
                    elif ARGS[1] == "False":
                        DNS_SNIFF = True
                    else:
                        ERROR_print("DNS_SNIFF can only be assign to True or False")
                        MAIN(DNS_SNIFF, HTTP_SNIFF, TARGETS, GATEWAY, INTERFACE)
                    print("DNS_SNIFF => {0}".format(DNS_SNIFF))

                elif ARGS[0] == "HTTP_SNIFF":
                    if ARGS[1] == "True":
                        HTTP_SNIFF = True
                    elif ARGS[1] == "False":
                        HTTP_SNIFF = True
                    else:
                        ERROR_print("HTTP_SNIFF can only be assign to True or False")
                        MAIN(DNS_SNIFF, HTTP_SNIFF, TARGETS, GATEWAY, INTERFACE)
                    print("HTTP_SNIFF => {0}".format(HTTP_SNIFF))
                    
                elif ARGS[0] == "TARGET":
                    print("[+] TIP: You can add more tham 1 target by doing so: set TARGET 192.168.1.194,192.168.1.145")
                    TARGETS = ARGS[1]
                    print("TARGET(S) => {0}".format(TARGETS))
                    
                elif ARGS[0] == "GATEWAY":
                    GATEWAY = ARGS[1]
                    print("GATEWAY => {0}".format(GATEWAY))
                    
                elif ARGS[0] == "INTERFACE":
                    INTERFACE = ARGS[1]
                    print("INTERFACE => {0}".format(INTERFACE))
                
                else:
                    ERROR_print("'{0}' is not a valid option!".format(ARGS[0]))

            if cmd_term == "start":
                MAC_ADDRESS = "None"
                SNIFF_NETWORK(DNS_SNIFF, HTTP_SNIFF, TARGETS, GATEWAY, INTERFACE)        

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
MAIN(DNS_SNIFF, HTTP_SNIFF, TARGETS, GATEWAY, INTERFACE)

