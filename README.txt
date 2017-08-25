REFERENCIAS
- Si escucharon mi charla, este personaje explica mejor que yo:
Wireless LAN Security and Penetration Testing Megaprimer - http://www.securitytube.net/groups?operation=view&groupId=9

- Tipos de Paquetes 802.11
https://www.savvius.com/resources/compendium/wireless_lan/wlan_packet_types

- Stadar 802.11, viejo pero sireve como referencia:
http://www.ie.itcr.ac.cr/acotoc/Ingenieria/Lab%20TEM%20II/Antenas/Especificacion%20802%2011-2007.pdf

- Estos son los scripts:
https://pastebin.com/raw/mexyNstb
https://pastebin.com/raw/kCnBzZ1s

- Herramientas que te pueden servir:
	* scapy
	* python (les recomiendo el libro violent python)
	* aircrack suit
	* wireshark
	* hostapd (Les dejo una guia muy chambona de como utilizarlo - Son notas mias espero les sea de utilidad)
	* john (pero el jumbo)	
------------------------HOSTAPD----------------------------------------------------
service network-manager stop  //Networkmanager has incompatibilities with hostapd
ifconfig wlan1 up 10.0.0.1 netmask 255.255.255.0
echo 1 > /proc/sys/net/ipv4/ip_forward  //Port FW

+++ masquearading from wlan1 to eth0
iptables --flush
iptables --table nat --flush
iptables --delete-chain
iptables --table nat --delete-chain
iptables --table nat --append POSTROUTING --out-interface eth0 -j MASQUERADE
iptables --append FORWARD --in-interface wlan1 -j ACCEPT

sysctl -w net.ipv4.ip_forward=1 //Prot FW

chmod 777 /var/lib/dhcp/dhcpd.leases // its a mess but it works
dhcpd -cf /etc/dhcp/dhcpd.conf -pf /var/run/dhcpd.pid wlan1 //Start dhcp


hostapd /etc/hostapd/hostapd.conf // star
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
dhcpd.conf
******************************************************************************************************************
ddns-update-style none;
ignore client-updates;
authoritative;
option local-wpad code 252 = text;

subnet
10.0.0.0 netmask 255.255.255.0 {
# --- default gateway
option routers
10.0.0.1;
# --- Netmask
option subnet-mask
255.255.255.0;
# --- Broadcast Address
option broadcast-address
10.0.0.255;
# --- Domain name servers, tells the clients which DNS servers to use.
option domain-name-servers
10.0.0.1, 8.8.8.8, 8.8.4.4;
option time-offset
0;
range 10.0.0.3 10.0.0.13;
default-lease-time 1209600;
max-lease-time 1814400;
}
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
******************************************************************************************************************

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
hostapd.conf
******************************************************************************************************************
# WiFi Hotspot
interface=wlan1
driver=nl80211
ssid=workshop
hw_mode=g
channel=1
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase=12345678
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP
