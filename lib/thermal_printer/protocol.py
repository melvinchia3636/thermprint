import lzo

WRITE_UUID = "0000AE01-0000-1000-8000-00805F9B34FB"
GRAY_LEVELS = 16

CHECKSUM_TABLE = [
    0,
    7,
    14,
    9,
    28,
    27,
    18,
    21,
    56,
    63,
    54,
    49,
    36,
    35,
    42,
    45,
    112,
    119,
    126,
    121,
    108,
    107,
    98,
    101,
    72,
    79,
    70,
    65,
    84,
    83,
    90,
    93,
    -32,
    -25,
    -18,
    -23,
    -4,
    -5,
    -14,
    -11,
    -40,
    -33,
    -42,
    -47,
    -60,
    -61,
    -54,
    -51,
    -112,
    -105,
    -98,
    -103,
    -116,
    -117,
    -126,
    -123,
    -88,
    -81,
    -90,
    -95,
    -76,
    -77,
    -70,
    -67,
    -57,
    -64,
    -55,
    -50,
    -37,
    -36,
    -43,
    -46,
    -1,
    -8,
    -15,
    -10,
    -29,
    -28,
    -19,
    -22,
    -73,
    -80,
    -71,
    -66,
    -85,
    -84,
    -91,
    -94,
    -113,
    -120,
    -127,
    -122,
    -109,
    -108,
    -99,
    -102,
    39,
    32,
    41,
    46,
    59,
    60,
    53,
    50,
    31,
    24,
    17,
    22,
    3,
    4,
    13,
    10,
    87,
    80,
    89,
    94,
    75,
    76,
    69,
    66,
    111,
    104,
    97,
    102,
    115,
    116,
    125,
    122,
    -119,
    -114,
    -121,
    -128,
    -107,
    -110,
    -101,
    -100,
    -79,
    -74,
    -65,
    -72,
    -83,
    -86,
    -93,
    -92,
    -7,
    -2,
    -9,
    -16,
    -27,
    -30,
    -21,
    -20,
    -63,
    -58,
    -49,
    -56,
    -35,
    -38,
    -45,
    -44,
    105,
    110,
    103,
    96,
    117,
    114,
    123,
    124,
    81,
    86,
    95,
    88,
    77,
    74,
    67,
    68,
    25,
    30,
    23,
    16,
    5,
    2,
    11,
    12,
    33,
    38,
    47,
    40,
    61,
    58,
    51,
    52,
    78,
    73,
    64,
    71,
    82,
    85,
    92,
    91,
    118,
    113,
    120,
    127,
    106,
    109,
    100,
    99,
    62,
    57,
    48,
    55,
    34,
    37,
    44,
    43,
    6,
    1,
    8,
    15,
    26,
    29,
    20,
    19,
    -82,
    -87,
    -96,
    -89,
    -78,
    -75,
    -68,
    -69,
    -106,
    -111,
    -104,
    -97,
    -118,
    -115,
    -124,
    -125,
    -34,
    -39,
    -48,
    -41,
    -62,
    -59,
    -52,
    -53,
    -26,
    -31,
    -24,
    -17,
    -6,
    -3,
    -12,
    -13,
]


def crc8(data):
    crc = 0
    for b in data:
        crc = CHECKSUM_TABLE[(crc ^ b) & 0xFF]
    return crc & 0xFF


def build_packet(cmd, payload, sub=0x00):
    length = len(payload)
    pkt = [0x51, 0x78, cmd & 0xFF, sub, length & 0xFF, (length >> 8) & 0xFF, *payload]
    pkt.append(crc8(pkt[6:]))
    pkt.append(0xFF)
    return bytes(pkt)


def set_energy(energy_value):
    return build_packet(0xAF, [energy_value & 0xFF, (energy_value >> 8) & 0xFF])


def set_quality(level):
    return build_packet(0xA4, [level])


def set_print_mode_gray16():
    return build_packet(0xBE, [0x00, 0x01])


def feed_paper_speed(speed):
    return build_packet(0xBD, [speed & 0xFF])


def feed_paper(pixels):
    return build_packet(0xA1, [pixels & 0xFF, (pixels >> 8) & 0xFF])


def get_dev_state():
    return build_packet(0xA3, [0x00])


def build_gray_scan_packet(raw_data):
    raw = bytes(raw_data)
    compressed = lzo.compress(raw, 1, False)
    orig_len = len(raw)
    comp_len = len(compressed)

    pkt = [0x51, 0x78, 0xCF, 0x00]
    pkt.append((comp_len + 4) & 0xFF)
    pkt.append(((comp_len + 4) >> 8) & 0xFF)
    pkt.append(orig_len & 0xFF)
    pkt.append((orig_len >> 8) & 0xFF)
    pkt.append(comp_len & 0xFF)
    pkt.append((comp_len >> 8) & 0xFF)
    pkt.extend(compressed)
    pkt.append(crc8(pkt[6:]))
    pkt.append(0xFF)
    return bytes(pkt)
