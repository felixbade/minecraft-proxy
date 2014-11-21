# bitoperations are fun, not that efficiency would be significant

def encode(number):
    if number < 0:
        return None
    if number == 0:
        return b'\x00'
   
    varint_bytes = []
    while number > 0:
        varint_bytes.append((number & 0x7f) | 0x80)
        number >>= 7
    varint_bytes[-1] &= 0x7f
    return bytes(varint_bytes)

def decode(varint):
    if check_encoded(varint):
        return decode_no_check(varint)
    else:
        return None

def check_encoded(varint):
    if len(varint) == 0:
        return False
    if varint[-1] & 0x80 != 0:
        return False
    for byte in varint[:-1]:
        if byte & 0x80 == 0:
            return False
    return True

def decode_no_check(varint):
    number = 0
    for byte in reversed(varint):
        number = (number << 7) + (byte & 0x7f)
    return number

def separate_first_varint_and_the_rest(packet):
    for possible_index in range(1, len(packet)):
        if check_encoded(packet[:possible_index]):
            return decode(packet[:possible_index]), packet[possible_index:]
    return None, None
