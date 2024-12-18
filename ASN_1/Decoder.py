
def decode_length(data: bytes) -> tuple[int, bytes]:

    first_byte = data[0]
    if first_byte < 128:
        return first_byte, data[1:]
    length_of_length = first_byte & 0x7F
    length = int.from_bytes(data[1:1 + length_of_length], 'big')
    return length, data[1 + length_of_length:]

def decode_integer(data: bytes) -> tuple[int, bytes]:


    length, rest = decode_length(data[1:])
    integer_bytes = rest[:length]
    value = int.from_bytes(integer_bytes, 'big', signed=False)
    return value, rest[length:]

def decode_string(data: bytes) -> tuple[str, bytes]:


    length, rest = decode_length(data[1:])
    string_bytes = rest[:length]
    return string_bytes.decode('ascii'), rest[length:]

def decode_oid(data: bytes) -> tuple[list[int], bytes]:

    length, rest = decode_length(data[1:])
    oid_bytes = rest[:length]
    oid = [oid_bytes[0] // 40, oid_bytes[0] % 40]
    sub_id = 0
    for byte in oid_bytes[1:]:
        if byte & 0x80:  # Continuation bit
            sub_id = (sub_id << 7) | (byte & 0x7F)
        else:
            sub_id = (sub_id << 7) | byte
            oid.append(sub_id)
            sub_id = 0
    return oid, rest[length:]

def decode_ip(data: bytes) -> tuple[str, bytes]:

    assert data[0] == 0x40, "Invalid IP tag"
    length, rest = decode_length(data[1:])
    ip_bytes = rest[:length]
    ip_address = '.'.join(map(str, ip_bytes))
    return ip_address, rest[length:]

def decode_sequence(encoded: bytes) -> tuple[list[bytes], bytes]:

    length, remainder = decode_length(encoded[1:])
    sequence_bytes = remainder[:length]
    remainder = remainder[length:]

    elements = []
    while sequence_bytes:
        element_length, sequence_bytes = decode_length(sequence_bytes[1:])
        element = sequence_bytes[:element_length]
        elements.append(bytes([encoded[0]]) + bytes([element_length]) + element)
        sequence_bytes = sequence_bytes[element_length:]

    return elements, remainder




