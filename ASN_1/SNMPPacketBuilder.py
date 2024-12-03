import Encoder

class SNMPPacketBuilder:
    def __init__(self, community:str, version:int):
        self.community = community
        self.version = version

    def build_get_request(self, request_id, oid):
        version_encoded = Encoder.encode_integer(self.version)
        community_encoded = Encoder.encode_octet_string(self.community)
        request_id_encoded = Encoder.encode_integer(request_id)
        error_status_encoded = Encoder.encode_integer(0)
        error_index_encoded = Encoder.encode_integer(0)

        oid_encoded = Encoder.encode_oid(oid)
        null_value_encoded = bytes([0x05, 0x00])  # NULL value: Tag 0x05, Length 0
        varbind = Encoder.encode_sequence([oid_encoded, null_value_encoded])

        varbinds_sequence = Encoder.encode_sequence([varbind])

        pdu = bytes([0xA0]) + Encoder.encode_length(
            len(request_id_encoded + error_status_encoded + error_index_encoded + varbinds_sequence)
        ) + request_id_encoded + error_status_encoded + error_index_encoded + varbinds_sequence

        snmp_message = Encoder.encode_sequence([version_encoded, community_encoded, pdu])
        return snmp_message

if __name__ == "__main__":
    snmp_builder = SNMPPacketBuilder(community="public", version=1)

    # Build SNMP GetRequest for OID .1.3.6.1.2.1.1.1.0
    oid = [1, 3, 6, 1, 2, 1, 1, 1, 0]  # sysDescr.0
    request_id = 123
    snmp_packet = snmp_builder.build_get_request(request_id, oid)

    print("SNMP Packet (hex):", snmp_packet.hex())