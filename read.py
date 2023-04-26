import socket

# https://download.beckhoff.com/download/document/io/ethercat-development-products/ethercat_esc_datasheet_sec1_technology_2i3.pdf
ETH_P_ALL = 3
s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(ETH_P_ALL))

s.bind(("eth0", 0))
START_DEST_MAC = 0
END_DEST_MAC = 6

START_SRC_MAC = 6
END_SRC_MAC = 12

START_ETH_TYPE = 12
END_ETH_TYPE = 14

START_ETHC_HDR = 14
END_ETHC_HDR = 16

START_ETHC_DATAG = 16


def get_bytes(a):
    return a * 2


def process_diagrams(diagrams):
    pass


try:
    while True:
        # read an incoming Ethernet frame
        # frame, addr = s.recvfrom(65535)
        frame = s.recv(1518)
        hex_frame = frame.hex()
        # extract the destination and source MAC addresses from the frame
        dest_mac = frame[START_DEST_MAC:END_DEST_MAC].hex()
        src_mac = frame[START_SRC_MAC:END_SRC_MAC].hex()

        # extract the Ethernet protocol type from the frame
        eth_type = frame[START_ETH_TYPE:END_ETH_TYPE].hex()
        print(eth_type)
        if eth_type == "88a4":  # 0x88a4:
            eth_cat_header = frame[START_ETHC_HDR:END_ETHC_HDR].hex()
            num_of_bits = 16
            from_binary = bin(int(eth_cat_header, 16))[2:].zfill(num_of_bits)
            length_datagrams = int(from_binary[0:11], 2)
            resereved = from_binary[12]
            ethcat_type = from_binary[13:]
            length_byte = length_datagrams // 8
            process_diagrams(frame[START_ETHC_DATAG : START_ETHC_DATAG + length_byte])


finally:
    # set the socket back to normal mode
    s.close()
