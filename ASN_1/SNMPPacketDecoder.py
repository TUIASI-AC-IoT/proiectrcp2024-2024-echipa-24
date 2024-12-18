import ASN_1.Decoder as Decoder


def decode_snmp_set_get(data: bytes) -> dict:

    length, rest = Decoder.decode_length(data[1:])
    version, rest = Decoder.decode_integer(rest)
    community , rest = Decoder.decode_string(rest)

    pdu_type = rest[0]
    rest = rest[1:]

    length_pdu, rest = Decoder.decode_length(rest)
    request_id, rest = Decoder.decode_integer(rest)
    error_status, rest = Decoder.decode_integer(rest)
    error_index, rest = Decoder.decode_integer(rest)


    variable_bindings, _ = Decoder.decode_sequence(rest)

    snmp_message = {
        'version': version,
        'community': community,
        'pdu_type': pdu_type,
        'request_id': request_id,
        'error_status': error_status,
        'error_index': error_index,
        'variable_bindings': []
    }
    value = 0

    for binding in variable_bindings:
        lenght2,rest= Decoder.decode_length(binding[1:])
        binding_oid, rest = Decoder.decode_oid(rest)
        value_type = rest[0]

        if value_type == 0x02:
            value,rest  = Decoder.decode_integer(rest)
        elif value_type == 0x04:
            value,rest = Decoder.decode_string(rest)
        elif value_type == 0x40:
            value,rest = Decoder.decode_ip(rest)

        snmp_message['variable_bindings'].append({
            'oid': binding_oid,
            'value': value
        })

    return snmp_message

# def decode_snmp_trap(data: bytes) -> dict:
#     length, rest = Decoder.decode_length(data[1:])
#     version, rest = Decoder.decode_integer(rest)
#     community , rest = Decoder.decode_string(rest)
#
#     pdu_type = rest[0]
#     rest = rest[1:]
#     length_pdu, rest = Decoder.decode_length(rest)
#

def decode_snmp_trap(data: bytes) -> dict:
    # Decode the overall message structure
    length, rest = Decoder.decode_length(data[1:])
    version, rest = Decoder.decode_integer(rest)
    community, rest = Decoder.decode_string(rest)

    pdu_type = rest[0]
    if pdu_type != 0xA4:  # Ensure it's a Trap PDU
        raise ValueError("Data is not a valid SNMP Trap PDU.")
    rest = rest[1:]  # Skip the PDU type

    # Decode the Trap PDU fields
    length_pdu, rest = Decoder.decode_length(rest)
    enterprise_oid, rest = Decoder.decode_oid(rest)
    agent_address , rest = Decoder.decode_ip(rest)
    generic_trap, rest = Decoder.decode_integer(rest)
    specific_trap, rest = Decoder.decode_integer(rest)
    timestamp, rest = Decoder.decode_integer(rest)

    # Decode variable bindings
    variable_bindings, _ = Decoder.decode_sequence(rest)

    # Construct the SNMP Trap message
    snmp_trap_message = {
        'version': version,
        'community': community,
        'pdu_type': pdu_type,
        'enterprise_oid': enterprise_oid,
        'agent_address': agent_address,
        'generic_trap': generic_trap,
        'specific_trap': specific_trap,
        'timestamp': timestamp,
        'variable_bindings': []
    }

    value = 0
    # Decode each variable binding (OID and value)
    for binding in variable_bindings:
        length, rest = Decoder.decode_length(binding[1:])
        binding_oid, rest = Decoder.decode_oid(rest)
        value_type = rest[0]

        if value_type == 0x02:  # Integer
            value, rest = Decoder.decode_integer(rest)
        elif value_type == 0x04:  # String
            value, rest = Decoder.decode_string(rest)
        elif value_type == 0x40:  # IP Address
            value, rest = Decoder.decode_ip(rest)
        # Add more types as necessary

        snmp_trap_message['variable_bindings'].append({
            'oid': binding_oid,
            'value': value
        })

    return snmp_trap_message

