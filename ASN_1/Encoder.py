
def encode_length(length: int) -> bytes:
    if length < 128:
        return bytes([length])
    else:
        encoded_length = bytearray()
        while length > 0:
            encoded_length.insert(0, length % 256)
            length //= 256

        return bytes([0x80 | len(encoded_length)]) + bytes(encoded_length)

def encode_integer(value: int) -> bytes:
    encoded_value = bytearray()
    while value > 0:
        encoded_value.insert(0, value % 256)
        value //= 256
    if encoded_value and (encoded_value[0] & 0x80):
        encoded_value.insert(0, 0x00)
    return bytes([0x02]) + encode_length(len(encoded_value)) + bytes(encoded_value)

#def encode_byte_string(value:bytes) -> bytes:
#    return bytes([0x04]) + encode_length(len(value)) + value

def encode_string(value:str) -> bytes:
    value_bytes = value.encode('ascii')
    return bytes([0x04]) + encode_length(len(value)) + value_bytes

def encode_oid(oid:list[int]) -> bytes:
    first_byte = 40 * oid[0] + oid[1]
    encoded_oid = bytes([first_byte])
    for sub_id in oid[2:]:
        encoded_oid += bytes([sub_id])
    return bytes([0x06]) + encode_length(len(encoded_oid)) + encoded_oid

def encode_ip(ip_address:str) -> bytes:
    ip_as_int = map(int, ip_address.split("."))
    ip_as_bytes = bytes(ip_as_int)
    return bytes([0x40]) + encode_length(len(ip_as_bytes)) + ip_as_bytes

def encode_sequence(encoded_elements:list[bytes]) -> bytes:
    concatenated = b''.join(encoded_elements)
    return bytes([0x30]) + encode_length(len(concatenated)) + concatenated
