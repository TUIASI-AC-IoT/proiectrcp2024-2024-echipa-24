import sys
from typing import List
import socket
from ASN_1.SNMPPacketDecoder import decode_snmp_set_get
from ASN_1.SNMPPacketBuilder import SNMPPacketBuilder

TIMEOUT = 5
PORT = 161

def send_getRequest(agent_ip, oid: List[int], request_id: int) -> None:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

    packet_builder = SNMPPacketBuilder()
    packet = packet_builder.build_get_request(request_id, oid)

    sock.sendto(packet, (agent_ip, PORT))
    sock.close()

def receive_getResponse(manager_ip):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.bind((manager_ip, PORT))
    sock.settimeout(TIMEOUT)

    try:
        packet, addr = sock.recvfrom(2048)
        decoded_packet = decode_snmp_set_get(packet)
        return decoded_packet['variable_bindings'][0]['value']
    except socket.timeout:
        return ""
    finally:
        sock.close()

def start_get_thread(value_var,manager_ip, agent_ip, oid, request_id):
    send_getRequest(agent_ip, oid, request_id)
    response_msg = receive_getResponse(manager_ip)
    value_var.set(response_msg)

if __name__ == "__main__":
    manager_ip = '127.0.0.1'
    MANAGER_PORT = 161  # Use an unprivileged port
    agent_ip = '127.1.1.100'
    agent_port = 161
    oid = [1, 3, 6, 1, 2, 1, 1, 1, 0]  # Replace with a valid OID
    request_id = 1

    response = start_get_thread(manager_ip, agent_ip, oid, request_id)
    if response is not None:
        print(f"SNMP GET Response: {response}")
    else:
        print("No response received.")
