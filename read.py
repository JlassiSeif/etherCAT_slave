import socket

# https://download.beckhoff.com/download/document/io/ethercat-development-products/ethercat_esc_datasheet_sec1_technology_2i3.pdf
ETH_P_ALL = 3
s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(ETH_P_ALL))

s.bind(("eth0", 0))


def get_bytes(a):
    return a * 2


try:
    while True:
        # read an incoming Ethernet frame
        # frame, addr = s.recvfrom(65535)
        frame = s.recv(1518)
        hex_frame = frame.hex()
        # extract the destination and source MAC addresses from the frame
        dest_mac = hex_frame[: get_bytes(6)]
        src_mac = hex_frame[get_bytes(6) : get_bytes(12)]

        # extract the Ethernet protocol type from the frame
        eth_type = hex_frame[get_bytes(12) : get_bytes(14)]
        if eth_type == "88a4":  # 0x88a4:
            eth_cat_header = hex_frame[get_bytes(14) : get_bytes(16)]
            print(eth_cat_header)
            num_of_bits = 16
            from_binary = bin(int(eth_cat_header, 16))[2:].zfill(num_of_bits)
            print(from_binary)
            length_datagrams = from_binary[0:11]
            print(int(length_datagrams, 2))
            resereved = from_binary[12]
            ethcat_type = from_binary[13:]
        # # print the destination and source MAC addresses and Ethernet protocol type
        # print("Destination MAC address:", ":".join("%02x" % b for b in dest_mac))
        # print("Source MAC address:", ":".join("%02x" % b for b in src_mac))
        # print("Ethernet protocol type:", hex(eth_type))
        # print("Payload:", frame[14:])

finally:
    # set the socket back to normal mode
    s.close()
