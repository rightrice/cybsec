packetSniffer README

the packet sniffer has a few parts that requires user input. this includes:
- the amount of packets you wish to capture
- the type of packets you wish to capture
- the network adapter you wish to use
- the file name you wish to save the pcap file as

ex:
packets: 100 OR 0 for a continous sniff until the spacebar is hit
packet filter: tcp
port: 80
network interface: eth0
file name: yourFirstSniffer.pcap