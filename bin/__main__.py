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

def MAIN():
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
    MAIN()
