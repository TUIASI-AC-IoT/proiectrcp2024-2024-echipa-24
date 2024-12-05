import Encoder

class SNMPPacketBuilder:
    def __init__(self, community:str, version:int):
        self.community = community
        self.version = version


    def build_get_request(self, request_id, oid):
        version_encoded = Encoder.encode_integer(self.version)
        community_encoded = Encoder.encode_string(self.community)
        request_id_encoded = Encoder.encode_integer(request_id)
        error_status_encoded = Encoder.encode_integer(0)
        error_index_encoded = Encoder.encode_integer(0)

        oid_encoded = Encoder.encode_oid(oid)
        null_value_encoded = bytes([0x05, 0x00])
        varbind = Encoder.encode_sequence([oid_encoded, null_value_encoded])

        varbinds_sequence = Encoder.encode_sequence([varbind])

        pdu = bytes([0xA0]) + Encoder.encode_length(
            len(request_id_encoded + error_status_encoded + error_index_encoded + varbinds_sequence)
        ) + request_id_encoded + error_status_encoded + error_index_encoded + varbinds_sequence

        snmp_message = Encoder.encode_sequence([version_encoded, community_encoded, pdu])
        return snmp_message

    def build_get_next_request(self, request_id) -> bytes:
        version_encoded = Encoder.encode_integer(self.version)
        community_encoded = Encoder.encode_string(self.community)
        request_id_encoded = Encoder.encode_integer(request_id)
        error_status_encoded = Encoder.encode_integer(0)
        error_index_encoded = Encoder.encode_integer(0)

        null_value_encoded = bytes([0x05, 0x00])
        varbind = Encoder.encode_sequence([null_value_encoded])
        varbinds_sequence = Encoder.encode_sequence([varbind])

        pdu = bytes([0xA1]) + Encoder.encode_length(
            len(request_id_encoded + error_status_encoded + error_index_encoded + varbinds_sequence)
        ) + request_id_encoded + error_status_encoded + error_index_encoded + varbinds_sequence

        snmp_message = Encoder.encode_sequence([version_encoded, community_encoded, pdu])
        return snmp_message

    def build_get_response(self, request_id, oid, value):
        version_encoded = Encoder.encode_integer(self.version)
        community_encoded = Encoder.encode_string(self.community)
        request_id_encoded = Encoder.encode_integer(request_id)
        error_status_encoded = Encoder.encode_integer(0)
        error_index_encoded = Encoder.encode_integer(0)

        oid_encoded = Encoder.encode_oid(oid)

        if type(value) is int:
            value_encoded = Encoder.encode_integer(value)
        else:
            value_encoded = Encoder.encode_string(value)

        varbind = Encoder.encode_sequence([oid_encoded, value_encoded])

        varbinds_sequence = Encoder.encode_sequence([varbind])

        pdu = bytes([0xA2]) + Encoder.encode_length(
            len(request_id_encoded + error_status_encoded + error_index_encoded + varbinds_sequence)
        ) + request_id_encoded + error_status_encoded + error_index_encoded + varbinds_sequence

        snmp_message = Encoder.encode_sequence([version_encoded, community_encoded, pdu])
        return snmp_message

    def build_set_request(self, request_id, oid, value):
        version_encoded = Encoder.encode_integer(self.version)
        community_encoded = Encoder.encode_string(self.community)
        request_id_encoded = Encoder.encode_integer(request_id)
        error_status_encoded = Encoder.encode_integer(0)
        error_index_encoded = Encoder.encode_integer(0)

        oid_encoded = Encoder.encode_oid(oid)

        if type(value) is int:
            value_encoded = Encoder.encode_integer(value)
        else:
            value_encoded = Encoder.encode_string(value)

        varbind = Encoder.encode_sequence([oid_encoded, value_encoded])

        varbinds_sequence = Encoder.encode_sequence([varbind])

        pdu = bytes([0xA3]) + Encoder.encode_length(
            len(request_id_encoded + error_status_encoded + error_index_encoded + varbinds_sequence)
        ) + request_id_encoded + error_status_encoded + error_index_encoded + varbinds_sequence

        snmp_message = Encoder.encode_sequence([version_encoded, community_encoded, pdu])
        return snmp_message

    def build_trap(self, oid:list[int], message:str, ip_address:str, time_stamp:int) -> bytes:
        version_encoded = Encoder.encode_integer(self.version)
        community_encoded = Encoder.encode_string(self.community)

        oid_encoded = Encoder.encode_oid(oid)
        agent_ip_address_encode = Encoder.encode_ip(ip_address)
        generic_trap_encoded = Encoder.encode_integer(6)
        specif_trap_encoded = Encoder.encode_integer(1)
        time_stamp_encoded = Encoder.encode_integer(time_stamp)

        message_encoded = Encoder.encode_string(message)
        varbind = Encoder.encode_sequence([oid_encoded, message_encoded])
        varbinds_sequence = Encoder.encode_sequence([varbind])

        pdu = bytes([0xA4]) + Encoder.encode_length(
            len(oid_encoded + agent_ip_address_encode + generic_trap_encoded + specif_trap_encoded + time_stamp_encoded + varbinds_sequence)
        ) + oid_encoded + agent_ip_address_encode + generic_trap_encoded + specif_trap_encoded + time_stamp_encoded + varbinds_sequence

        snmp_message = Encoder.encode_sequence([version_encoded, community_encoded, pdu])
        return snmp_message

if __name__ == "__main__":
    packet_builder = SNMPPacketBuilder("public", 0)

    community = "public"
    enterprise_oid = [ 1,3,6,1,2,1,1,1]
    agent_address = "192.168.0.1"
    timestamp = 12345  # 123.45 secunde

    trap_packet = packet_builder.build_trap(enterprise_oid,"Eroare temperaturaaaaaaaaa",agent_address,timestamp)
    print("SNMP TRAP (hex):")
    print(trap_packet.hex())

    get_next = packet_builder.build_get_next_request(request_id=99)
    print("SNMP getNextRequest (hex):")
    print(get_next.hex())

    get_packet = packet_builder.build_get_request(request_id=100, oid=enterprise_oid)
    print("SNMP getRequest (hex):")
    print(get_packet.hex())
