#!/usr/bin/env python3
import sys
from optparse import OptionParser, OptionGroup
import optparse
from colorama import Style, Fore
import os
import sys
import datetime
import random
import time
import requests
import random
import string

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

VERSION = "V.1"

def DIR_NAME(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def LOADING():
    print(r"""                                               
                                                              
"""+color.LIGHTGREEN+"""
oooo     oooo o88   ooooooooooo o88"""+color.RED+"""    oooooooo8"""+color.LIGHTGREEN+"""                    
 88   88  88  oooo   888        oooo"""+color.RED+"""  888        ooooooooo  oooo   oooo"""+color.LIGHTGREEN+"""
  88 888 88    888   888ooo8     888"""+color.RED+"""   888oooooo  888    888 888   888"""+color.LIGHTGREEN+"""  
   888 888     888   888         888"""+color.RED+"""          888 888    888  888 888"""+color.LIGHTGREEN+"""   
    8   8     o888o o888o       o888o"""+color.RED+""" o88oooo888  888ooo88      8888"""+color.CYAN+""" 
   [ WiFiSpy - V.1.0 ]                           """+color.RED+"""o888        o8o888"""+color.CYAN+"""    
   [ Coded By Ghosty / DeaDHackS Team ]                       
   [ https://www.github.com/WiFiSpy ]
""")
    LOADING_SECONDS = 10 
    while LOADING_SECONDS > 0:
        OVER_print("["+color.LIGHTGREEN+"+"+color.END+"]"+color.LIGHTGREEN+" Loading ."+color.END)
        LOADING_SECONDS = LOADING_SECONDS - 1
        time.sleep(0.25)
        OVER_print("["+color.LIGHTGREEN+"+"+color.END+"]"+color.LIGHTGREEN+" lOading .."+color.END)
        LOADING_SECONDS = LOADING_SECONDS - 1
        time.sleep(0.25)
        OVER_print("["+color.LIGHTGREEN+"+"+color.END+"]"+color.LIGHTGREEN+" loAding ..."+color.END)
        LOADING_SECONDS = LOADING_SECONDS - 1
        time.sleep(0.25)
        OVER_print("["+color.LIGHTGREEN+"+"+color.END+"]"+color.LIGHTGREEN+" loaDing ."+color.END)
        LOADING_SECONDS = LOADING_SECONDS - 1   
        time.sleep(0.25)
        OVER_print("["+color.LIGHTGREEN+"+"+color.END+"]"+color.LIGHTGREEN+" loadIng .."+color.END)
        LOADING_SECONDS = LOADING_SECONDS - 1 
        time.sleep(0.25)
        OVER_print("["+color.LIGHTGREEN+"+"+color.END+"]"+color.LIGHTGREEN+" loadiNg ..."+color.END)
        LOADING_SECONDS = LOADING_SECONDS - 1
        time.sleep(0.25)
        OVER_print("["+color.LIGHTGREEN+"+"+color.END+"]"+color.LIGHTGREEN+" loadinG ."+color.END)
        LOADING_SECONDS = LOADING_SECONDS - 1 
        time.sleep(0.25)
    if "nt" in os.name:
       os.system("cls")
    else:
       os.system("clear") 

def BANNER():
    print(r"""                                               
                                                              
"""+color.LIGHTGREEN+"""
oooo     oooo o88   ooooooooooo o88"""+color.RED+"""    oooooooo8"""+color.LIGHTGREEN+"""                    
 88   88  88  oooo   888        oooo"""+color.RED+"""  888        ooooooooo  oooo   oooo"""+color.LIGHTGREEN+"""
  88 888 88    888   888ooo8     888"""+color.RED+"""   888oooooo  888    888 888   888"""+color.LIGHTGREEN+"""  
   888 888     888   888         888"""+color.RED+"""          888 888    888  888 888"""+color.LIGHTGREEN+"""   
    8   8     o888o o888o       o888o"""+color.RED+""" o88oooo888  888ooo88      8888"""+color.CYAN+""" 
   [ WiFiSpy - V.1.0 ]                           """+color.RED+"""o888        o8o888"""+color.CYAN+"""    
   [ Coded By Ghosty / DeaDHackS Team ]                       
   [ https://www.github.com/WiFiSpy ]
""")

def MAIN(VERSION):
    BANNER()
    print("\n\n")
    INFO_print("Enter '?' or 'help' to start off!")
    while True:
        try:    
            cmd_term = input(color.UNDERLINE+color.CYAN+"WiFiSpy"+color.END+"::"+color.UNDERLINE+color.CYAN+"root"+color.END+" ["+color.CYAN+color.UNDERLINE+""+color.END+"] +> ")
        
            if cmd_term == "?" or cmd_term == "help":
                print(r"""
* Description *
    Handles all user needs here, including what to module to load etc!
    
* WiFiSpy Commands *
    ? - help             <*>    this menu
    credits              <*>    shows WiFiSpy credits
    version              <*>    displays exact version
    check_update         <*>    check github for an update
    clear                <*>    clear screen
    exit                 <*>    exit WiFiSpy

* Module Commands *
    network_scan         <">    scans network for alive hosts
    load_sniffer         <">    loads sniffers
    load_wifi_attacks    <">    loads WiFi attacks
            """)
            if cmd_term == "credits":
                print("Credits: ")
                print("Main Developer: Ghosty / DeaDHackS Team ")
                print("With?: No one ")
             
            if cmd_term == "version":
                print("1.0 - First version ever made!")
            
            if cmd_term == "check_update":
                r = requests.get("https://raw.githubusercontent.com/DeaDHackS/WiFiSpy/master/version")
                r = r.content.decode("utf-8")
                r = r.replace("\n", "")
                r = r.replace("V.", "")
                v = VERSION.replace("V.", "")
                if int(r) > int(v):
                    print("[*] GitHub Version: V."+str(r))
                    print("[*] Current Version: "+VERSION)
                    WARNING_print("Update is avalaible!")
                    print("\n")
                    update = input(color.END+"[?] Do you wish to update your WiFiSpy? [Y/N]: ")
                    if update == "Y":
                        DIR = DIR_NAME(5)
                        os.system("cd && cd Desktop && mkdir {0} && cd {1} && git clone https://github.com/DeaDHackS/WiFiSpy".format(DIR, DIR))
                        SUCCESS_print("WiFiSpy Downloaded At: /rppt/Desktop/"+DIR+"/WiFiSpy")
                        SUCCESS_print("Done!")
                elif int(r) < int(v):
                    print("[*] GitHub Version: V."+str(r))
                    print("[*] Current Version: "+VERSION)
                    ERROR_print("How the? How do you have a bigger version than the GitHub? #Illuminati!")
                elif int(r) == int(v):
                    print("[*] GitHub Version: V."+str(r))
                    print("[*] Current Version: "+VERSION)
                    SUCCESS_print("No update avalaible!")
              
             
            if cmd_term == "clear":
                if "nt" in os.name:
                    os.system("cls")
                else:
                    os.system("clear") 
            
            if cmd_term == "exit":
                print("[+] Quitting, bye-bye. Thanks for using WiFiSpy!")
                exit()
            
            if cmd_term == "network_scan":
                 os.system("cd scanners && python3 arp_scanner.py")
          
            if cmd_term == "load_sniffer":
                 os.system("cd sniffers && python3 __main__.py")
          
            if cmd_term == "load_wifi_attacks":
                 os.system("cd wifi_attacks && python3 __main__.py")

        except KeyboardInterrupt:
            print("\n[+] Quitting, bye-bye. Thanks for using WiFiSpy!")
            exit()
if __name__ == "__main__":
    LOADING()
    MAIN(VERSION)
