import socket
from Mib import MIB
from ASN_1.SNMPPacketDecoder import decode_snmp_set_get
from ASN_1.SNMPPacketBuilder import SNMPPacketBuilder

TIMEOUT = 5
PORT = 161


def handle_get_request(packet):
    # Decode the received SNMP request
    decoded_packet = decode_snmp_set_get(packet)

    # Extract the OID and request_id
    oid = decoded_packet['variable_bindings'][0]['oid']
    request_id = decoded_packet['request_id']

    # Check the OID and prepare a response
    response_value = MIB.Get_Resource(oid)

    # Build the SNMP response packet
    packet_builder = SNMPPacketBuilder()
    response_packet = packet_builder.build_get_response(request_id, oid, response_value)

    return response_packet


def receive_snmp_request(agent_ip):
    """ Function to receive SNMP requests. """
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
    """ Function to send SNMP response back to the manager. """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

    try:
        sock.sendto(response_packet, (addr[0],PORT))
    except Exception as e:
        print(f"Error sending response: {e}")
    finally:
        sock.close()


def start_agent(agent_ip):
    while True:
        # Receive SNMP request
        packet, addr = receive_snmp_request(agent_ip)

        if packet is None or addr is None:
            continue  # Skip if there was an error receiving the request

        # Handle the request and generate a response
        response_packet = handle_get_request(packet)

        # Send the response back to the manager
        send_snmp_response(response_packet, addr)


if __name__ == "__main__":
    agent_ip = '127.1.1.100'

    start_agent(agent_ip)
