import socket

ETH_P_ALL = 3
s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(ETH_P_ALL))

s.bind(("eth0", 0))


try:
    while True:
        # read an incoming Ethernet frame
        # frame, addr = s.recvfrom(65535)
        frame = s.recv(2000)

        # extract the destination and source MAC addresses from the frame
        dest_mac = frame[:6]
        src_mac = frame[6:12]

        # extract the Ethernet protocol type from the frame
        eth_type = int.from_bytes(frame[12:14], byteorder="big")

        # print the destination and source MAC addresses and Ethernet protocol type
        print("Destination MAC address:", ":".join("%02x" % b for b in dest_mac))
        print("Source MAC address:", ":".join("%02x" % b for b in src_mac))
        print("Ethernet protocol type:", hex(eth_type))
        print("Payload:", frame[14:])

finally:
    # set the socket back to normal mode
    s.close()
