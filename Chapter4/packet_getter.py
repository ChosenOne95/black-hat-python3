from scapy.all import *
import sys

host = "192.168.2.222"
packet_count = 5000
interface = "eth0"

bpf_filter = "ip host {}".format(host)

try:
    print("[*] Starting sniffer for {} packets".format(packet_count))

    packets = sniff(count=packet_count, filter=bpf_filter, iface=interface)

except KeyboardInterrupt:
    pass

finally:
    # write out the captured packets
    print("[*] Writing packets to arper.pcap")
    wrpcap("arper.pcap", packets)
    sys.exit(0)
