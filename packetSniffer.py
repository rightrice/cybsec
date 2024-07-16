from scapy.all import sniff, wrpcap, hexdump, conf, get_if_list, get_if_hwaddr
import time
import threading
import keyboard

# List to store captured packets
packets = []
sniffing = True

def packet_callback(packet):
    # Print the time when packet is captured
    print(f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Print a summary of the packet
    print(packet.summary())
    
    # Print a detailed hexdump of the packet
    print(hexdump(packet))
    
    # Add the packet to the list
    packets.append(packet)

def start_sniffing(count, full_filter, iface):
    global sniffing
    try:
        # Set the interface to promiscuous mode
        conf.iface = iface
        conf.promisc = True

        # Capture packets with the specified filter and callback
        sniff(prn=packet_callback, count=count, filter=full_filter, iface=iface, stop_filter=lambda x: not sniffing)
    except Exception as e:
        print(f"Error capturing packets: {e}")

def main():
    global sniffing
    # Display available interfaces
    print("Available network interfaces:")
    interfaces = get_if_list()
    for iface in interfaces:
        try:
            print(f"{iface}: {get_if_hwaddr(iface)}")
        except Exception as e:
            print(f"{iface}: Unable to get hardware address ({e})")

    # Get user input for count, filter, port, interface, and output file name
    count = int(input("Enter the number of packets to capture (use 0 for unlimited): "))
    packet_filter = input("Enter the packet filter (e.g., 'tcp'): ")
    port = input("Enter the port to filter on (e.g., '80'): ")
    iface = input("Enter the network interface to use: ")
    output_file = input("Enter the name of the output pcap file (e.g., 'captured_packets.pcap'): ")

    # Combine filter and port
    full_filter = f"{packet_filter} port {port}"

    # Start sniffing in a separate thread
    sniffer_thread = threading.Thread(target=start_sniffing, args=(count, full_filter, iface))
    sniffer_thread.start()

    print("Press spacebar to stop sniffing...")

    # Wait for the spacebar press to stop sniffing
    keyboard.wait('space')
    sniffing = False
    sniffer_thread.join()

    # Save captured packets to a pcap file
    wrpcap(output_file, packets)
    print(f"Packets saved to {output_file}")

if __name__ == "__main__":
    main()