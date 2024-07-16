from scapy.all import sniff, wrpcap, hexdump, conf, get_if_list, get_if_hwaddr
import time

# List to store captured packets
packets = []

def packet_callback(packet):
    # Print the time when packet is captured
    print(f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Print a summary of the packet
    print(packet.summary())
    
    # Print a detailed hexdump of the packet
    print(hexdump(packet))
    
    # Add the packet to the list
    packets.append(packet)

def main():
    # Display available interfaces
    print("Available network interfaces:")
    interfaces = get_if_list()
    for iface in interfaces:
        try:
            print(f"{iface}: {get_if_hwaddr(iface)}")
        except Exception as e:
            print(f"{iface}: Unable to get hardware address ({e})")

    # Get user input for count, filter, and output file name
    count = int(input("Enter the number of packets to capture: "))
    packet_filter = input("Enter the packet filter (e.g., 'tcp port 80'): ")
    iface = input("Enter the network interface to use: ")
    output_file = input("Enter the name of the output pcap file (e.g., 'captured_packets.pcap'): ")

    try:
        # Set the interface to promiscuous mode
        conf.iface = iface
        conf.promisc = True

        # Capture packets with the specified filter and callback
        sniff(prn=packet_callback, count=count, filter=packet_filter, iface=iface)
    except Exception as e:
        print(f"Error capturing packets: {e}")

    # Save captured packets to a pcap file
    wrpcap(output_file, packets)

if __name__ == "__main__":
    main()
