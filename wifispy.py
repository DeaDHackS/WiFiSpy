#!/usr/bin/env python3
import sys
from optparse import OptionParser, OptionGroup
import optparse
from colorama import Style, Fore
import os
import sys
import datetime
import random

# Checks if the user used Python2 or Python3 ...
if "major=2" in str(sys.version_info):
    sys.stdout.write("[*] Please use Python3+ not Python2!\n")
    exit()

# Because github deletes empty directory, i just make a if statement to check and create one
if not os.path.isdir("bin/wifi_attacks/wpa_capture/tmp"):
    os.mkdir("bin/wifi_attacks/wpa_capture/tmp")

# Check if we are root
if not os.getuid() == 0:
    print("[*] Please run WiFiSpy as root!\n Command: sudo python3 wifispy.py")
    exit()

# Launches main menu
os.system("cd bin && python3 __main__.py")
