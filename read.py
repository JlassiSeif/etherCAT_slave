import socket

# https://download.beckhoff.com/download/document/io/ethercat-development-products/ethercat_esc_datasheet_sec1_technology_2i3.pdf
ETH_P_ALL = 3
s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(ETH_P_ALL))

s.bind(("eth0", 0))


try:
    while True:
        # read an incoming Ethernet frame
        # frame, addr = s.recvfrom(65535)
        frame = s.recv(1518)

        # extract the destination and source MAC addresses from the frame
        dest_mac = frame[:6]
        src_mac = frame[6:12]

        # extract the Ethernet protocol type from the frame
        eth_type = int.from_bytes(frame[12:14], byteorder="big")
        print(hex(eth_type))
        if eth_type == 34980:
            eth_cat_header = int.from_bytes(frame[14:16], byteorder="big")
            print(bin(eth_cat_header))
            from_binary = bin(eth_cat_header)
            length_datagrams = from_binary[0:11]
            resereved = from_binary[12]
            ethcat_type = from_binary[13:]
            print(length_datagrams, resereved, ethcat_type)
        # # print the destination and source MAC addresses and Ethernet protocol type
        # print("Destination MAC address:", ":".join("%02x" % b for b in dest_mac))
        # print("Source MAC address:", ":".join("%02x" % b for b in src_mac))
        # print("Ethernet protocol type:", hex(eth_type))
        # print("Payload:", frame[14:])

finally:
    # set the socket back to normal mode
    s.close()
