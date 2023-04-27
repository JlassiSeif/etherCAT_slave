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

LEN_DIAG_HDR = 10

Frame_dict = {}
commands = {
    "0": "No Operation",
    "1": "Auto Increment Read",
    "2": "Auto Increment Write",
    "3": "Auto Increment Read Write",
    "4": "Configured Address Read",
    "5": "Configured Address Write",
    "6": "Configured Address Read Write",
    "7": "Broadcast Read",
    "8": "Broadcast Write",
    "9": "Broadcast Read Write",
    "a": "Logical Memory Read",
    "b": "Logical Memory Write",
    "b": "Logical Memory Read Write",
    "d": "Auto Increment Read Multiple Write",
    "e": "Configured Read Multiple Write",
}


def pprint(id, frame_dict):
    print(f'Frame {id}: {frame_dict["frame_length"]} bytes captured.')
    print(f'src: {frame_dict["src_mac"]}, Dest: {frame_dict["dest_mac"]}')
    print(f"EtherCAT frame header")
    print(
        f'    Length {hex(frame_dict["length_datagrams"])} = {frame_dict["length_datagrams"]}'
    )
    print(
        f'    Reserved {hex(int(Frame_dict["resereved"],2))} = {Frame_dict["resereved"]}'
    )
    print(
        f'    Type: EtherCat command {hex(int(Frame_dict["Protocol_type"],2))} = {Frame_dict["Protocol_type"]}'
    )
    print(f"EtherCAT datagram")
    print(f"    Header")
    print(
        f'        Command     : {commands[Frame_dict["cmd"]]} ({hex(int(Frame_dict["cmd"],2))})'
    )
    print(f'        Index       : {hex(int(Frame_dict["inedex"],2))}')
    print(f'        Log Addr    : {hex(int(Frame_dict["address"],2))}')
    print(f'        Length      : {int(Frame_dict["length"],2)}')
    print(f'            Reserved   = {Frame_dict["R"]}')
    print(f'            Round Trip = {Frame_dict["C"]}')
    print(f'            Last Indicator = {Frame_dict["M"]}')
    print(f'        Interrupt   : {hex(int(Frame_dict["length"],2))}')
    print(f'    Data    : {Frame_dict["diagram_data"]}')
    print(f'    Working Counter : {Frame_dict["diagram_data"]}')


def process_diagrams(diagrams):
    DIAGRAM_HDR = diagrams[0 : 0 + LEN_DIAG_HDR].hex()
    Frame_dict["cmd"] = DIAGRAM_HDR[0]
    Frame_dict["inedex"] = DIAGRAM_HDR[1]
    Frame_dict["address"] = DIAGRAM_HDR[2:6]
    len_r_c_m = DIAGRAM_HDR[7:9]
    len_r_c_m = bin(int(len_r_c_m, 16))[2:].zfill(16)
    Frame_dict["length"] = len_r_c_m[:11]
    Frame_dict["R"] = len_r_c_m[11:14]
    Frame_dict["C"] = len_r_c_m[14:15]
    Frame_dict["M"] = len_r_c_m[15:]
    Frame_dict["IRQ"] = DIAGRAM_HDR[9:11]
    l = int(Frame_dict["length"], 2)
    Frame_dict["diagram_data"] = diagrams[LEN_DIAG_HDR : LEN_DIAG_HDR + l]
    Frame_dict["working_counter"] = diagrams[LEN_DIAG_HDR + l : LEN_DIAG_HDR + l + 2]


try:
    while True:
        frame = s.recv(1518)

        # extract the destination and source MAC addresses from the frame

        # extract the Ethernet protocol type from the frame
        eth_type = frame[START_ETH_TYPE:END_ETH_TYPE].hex()
        if eth_type == "88a4":  # 0x88a4:
            Frame_dict["frame_length"] = len(frame.hex())
            Frame_dict["dest_mac"] = frame[START_DEST_MAC:END_DEST_MAC].hex()
            Frame_dict["src_mac"] = frame[START_SRC_MAC:END_SRC_MAC].hex()
            Frame_dict["eth_type"] = eth_type
            eth_cat_header = frame[START_ETHC_HDR:END_ETHC_HDR].hex()
            num_of_bits = 16
            from_binary = bin(int(eth_cat_header, 16))[2:].zfill(num_of_bits)
            Frame_dict["length_datagrams"] = int(from_binary[:11], 2)
            Frame_dict["resereved"] = from_binary[11:12]
            Frame_dict["Protocol_type"] = from_binary[12:4]
            length_byte = Frame_dict["length_datagrams"] // 8
            # print(length_byte)
            # print(from_binary)
            # print(ethcat_type, resereved, from_binary[5:16])
            process_diagrams(frame[START_ETHC_DATAG : START_ETHC_DATAG + length_byte])
            pprint(1, Frame_dict)

finally:
    # set the socket back to normal mode
    s.close()
