import socket
import binascii


def send_ethernet_frame(dst_mac, src_mac, eth_type, payload):
    # Create a raw socket and bind it to the Ethernet interface
    sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW)
    sock.bind(("eth0", 0))

    # Build the Ethernet frame
    dst_mac_bytes = binascii.unhexlify(dst_mac.replace(":", ""))
    src_mac_bytes = binascii.unhexlify(src_mac.replace(":", ""))
    eth_type_bytes = eth_type.to_bytes(2, byteorder="big")
    ethernet_frame = dst_mac_bytes + src_mac_bytes + eth_type_bytes + payload

    # Send the Ethernet frame
    sock.send(ethernet_frame)


my_mac = "01:01:01:01:01:01"
other_mac = "ff:ff:ff:ff:ff:ff"


def send():
    send_ethernet_frame(other_mac, my_mac, 0x0800, b"Hello, world!")
