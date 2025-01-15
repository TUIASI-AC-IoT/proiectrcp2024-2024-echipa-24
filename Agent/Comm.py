import socket
from Mib import MIB
from ASN_1.SNMPPacketDecoder import decode_snmp_set_get
from ASN_1.SNMPPacketBuilder import SNMPPacketBuilder

TIMEOUT = 5
PORT = 161


def handle_get_request(packet):
    decoded_packet = decode_snmp_set_get(packet)

    oid = decoded_packet['variable_bindings'][0]['oid']
    request_id = decoded_packet['request_id']

    response_value = MIB.Get_Resource(oid)

    packet_builder = SNMPPacketBuilder()
    response_packet = packet_builder.build_get_response(request_id, oid, response_value)

    return response_packet

def handle_get_next_request(packet):
    decoded_packet = decode_snmp_set_get(packet)

    oid = decoded_packet['variable_bindings'][0]['oid']
    request_id = decoded_packet['request_id']

    next_oid = MIB.get_next_oid(oid)

    response_value = MIB.Get_Resource(next_oid)

    packet_builder = SNMPPacketBuilder()
    response_packet = packet_builder.build_get_response(request_id, next_oid, response_value)

    return response_packet


def handle_set_request(packet):
    decoded_packet = decode_snmp_set_get(packet)

    oid = decoded_packet['variable_bindings'][0]['oid']
    request_id = decoded_packet['request_id']
    value = decoded_packet['variable_bindings'][0]['value']

    MIB.Set_Resource(oid, value)
    response_value = MIB.Get_Resource(oid)

    packet_builder = SNMPPacketBuilder()
    response_packet = packet_builder.build_get_response(request_id, oid, response_value)

    return response_packet


def receive_snmp_request(agent_ip):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.bind((agent_ip, PORT))

    print(f"Agent listening on {agent_ip}:{PORT}...")

    try:
        packet, addr = sock.recvfrom(2048)
        print(f"Received SNMP request from {addr}")
        return packet, addr
    except Exception as e:
        print(f"Error receiving request: {e}")
        return None, None
    finally:
        sock.close()


def send_snmp_response(response_packet, addr):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.sendto(response_packet, (addr[0],PORT))



def start_agent(agent_ip):
    while True:
        packet, addr = receive_snmp_request(agent_ip)

        if packet is None or addr is None:
            continue

        decoded_packet = decode_snmp_set_get(packet)
        pdu_type=decoded_packet['pdu_type']
        if pdu_type == 0xA0 :
            response_packet = handle_get_request(packet)
        if pdu_type == 0xA1:
           response_packet = handle_get_next_request(packet)
        if pdu_type == 0xA3:
            response_packet = handle_set_request(packet)

        send_snmp_response(response_packet, addr)


if __name__ == "__main__":
    agent_ip = '127.1.1.100'

    start_agent(agent_ip)
