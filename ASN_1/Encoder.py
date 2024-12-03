def encode_length(length:int) -> bytes:
    if length < 128:
        return bytes([length])
    else:
        length_as_bytes = bytes([length])
        return bytes([0x80 | len(length_as_bytes)]) + length_as_bytes

def encode_integer(value:int) -> bytes:
    encoded_value = bytes([value])
    if encoded_value[0] & 0x80:
        encoded_value = b'\x00' + encoded_value
    return bytes([0x02]) + encode_length(len(encoded_value)) + encoded_value

def encode_octet_string(value:str) -> bytes:
    value_bytes = value.encode(encoding='ascii')
    return bytes([0x04]) + encode_length(len(value)) + value_bytes

def encode_oid(oid:list[int]) -> bytes:
    first_byte = 40 * oid[0] + oid[1]
    encoded_oid = bytes([first_byte])
    for sub_id in oid[2:]:
        encoded_oid += bytes([sub_id])
    return bytes([0x06]) + encode_length(len(encoded_oid)) + encoded_oid

def encode_sequence(encoded_elements:list[bytes]) -> bytes:
    concatenated = b''.join(encoded_elements)
    return bytes([0x30]) + encode_length(len(concatenated)) + concatenated
