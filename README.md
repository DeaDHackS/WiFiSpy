# WiFiSpy V.1 - First Version
WiFiSpy is a tool written to automate powerful wifi / local attacks, with its nice user friendly console and easy-to-use, WiFiSpy can deliver a powerful ability to break in a network or even spy over a network!

# BUG FIXED & MODULE UPDATE!
<p>
Fixed:
   - Error in wifi_jammer_main.py : Line 154 : "cd wpa_capture" that was missed-placed into that line.
   - Error in ap_scan.py : Line 58 : "INTERFACE.replace("mon", "")" INTERFACE was not declared and was replaced by a global inteface.
</p>

# IMPORTANT
At 24/2/2019 - 8:52 AM I updated __main__.py to add a new command, called check_update!
So no need to go on the page to check the news, simply do check_update and WiFiSpy will check for potential updates.

# Requirements!
</p>
WiFiSpy was developed and tested with python3 it will diffently not work with python2!
Since its for linux, you cannot run it into a Windows machine or MacOS.
</p>

# Required Tools
```
aircrack-ng and its libraries (airodump-ng,aireplay-ng,airebase-ng etc...)
pyrit (Optional)
XTerm
```

# Features
1. LOCAL ATTACKS
   - HTTP TRAFFIC SNIFFING
     - COOKIE, LOGIN, POST/GET DATA, URL
   - DNS QUERY SNIFFING
     - RESOLVED DOMAINS
   - NETWORK SCAN
     - HOSTNAME, MAC ADDRESS, LOCAL IP
   - WiFi STRIPER / CLIENT KICKER (COMING IN V.2)
     - COMING IN V.2

2. WIRELESS ATTACKS
   - Spoof Mac (OPTIONS NOT ATTACK / COMING IN V.2 ;))
   - 4-WAYS-HANDSHAKE CAPTURE
     - DETECT CLIENTS, AUTOMATED HANDSHAKE CHECKER / SNOOPER, AUTO DEAUTHER (INCLUDED WiFiSpy OWN DEAUTH MODULE)
   - EVIL-TWIN - COMING IN V.2 ;)
     - COMING IN V.2 ;)
   - DEAUTH ATTACK
     - DETECT CLIENTS (COMING IN V.2 ;)), KICK MORE THAN 1 HOST
   - AP / WiFi SCANNER
     - DETECT CLIENTS (COMING IN V.2 ;)), ESSID - NAME, BSSID - MAC ADDRESS, SECURITY TYPE, ENCRYPTED?

# Incoming Features In WiFiSpy V.2
```
1 - Evil-Twin Attack Module
2 - Client Detection (For Deauth, Kick Off Client(s) And Scanner)
3 - Spoof Mac (For Wireless Attacks)
5 - Automated Updating / Check Update Module
6 - (MAYBE) +DNS SPOOF / SSLstrip (For Sniffers)
7 - Kick Off Client(s) (For Local Attacks)
8 - Hash Attack / Cracking Menu
9 - Automated PMKID Capture!!!!
10 - Automated WPS Pixie-Dust Attack
```

# How-To-Use
```
python3 wifispy.py
```
  
# How-To-Install
```
git clone https://github.com/DeaDHackS/WiFiSpy
cd WiFiSpy
chmod 777 -R *
pip3 install -r requirements
```
  
# Screenshots
### The follow images are not how the script actually looks like, what i mean is that i cleared the screen to show the menus its self but when ran normally without running "clear" in the WiFiSpy console, a nice ASCII banner is there for you!

## Main Menu 
![Example](https://i.imgur.com/cpIXYhS.png)

## Network Scan Menu
![Example](https://i.imgur.com/0BNvAuX.png)

## Sniffers / Local Menu
![Example](https://i.imgur.com/n0lSpG9.png)

## Wireless Attacks Menu
![Example](https://i.imgur.com/vemC6FN.png)
