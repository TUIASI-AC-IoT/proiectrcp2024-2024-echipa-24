import time
import socket
import threading
import queue
import ASN_1.SNMPPacketDecoder as Decoder

trap_queue = queue.Queue()

def receive_traps(manager_ip="0.0.0.0", manager_port=162) -> None:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.bind((manager_ip, manager_port))
    print(f"Listening for traps on {manager_ip}:{manager_port}...")

    while True:
        data, addr = sock.recvfrom(1024)
        try:
            decoded_trap = Decoder.decode_snmp_trap(data)
            trap_queue.put(decoded_trap)
        except Exception as e:
            print(f"Failed to decode trap from {addr}: {e}")


def update_trap_listbox(trap_listbox) -> None:
    while not trap_queue.empty():
        trap = trap_queue.get()
        message = (
            f"Trap Received:\n"
            f"Version: {trap['version']}\n"
            f"Community: {trap['community']}\n"
            f"Enterprise OID: {trap['enterprise_oid']}\n"
            f"Agent Address: {trap['agent_address']}\n"
            f"Generic Trap: {trap['generic_trap']}\n"
            f"Specific Trap: {trap['specific_trap']}\n"
            f"Timestamp: {trap['timestamp']}\n"
            f"Variable Bindings: {trap['variable_bindings']}\n\n"
        )
        trap_listbox.config(state="normal")
        trap_listbox.insert("end", message)
        trap_listbox.config(state="disabled")


def start_trap_thread(trap_listbox):
    def trap_listener():
        receive_traps(manager_ip="0.0.0.0", manager_port=162)

    trap_thread = threading.Thread(target=trap_listener, daemon=True)
    trap_thread.start()

    def periodic_update():
        update_trap_listbox(trap_listbox)
        trap_listbox.after(1000, periodic_update)  # Check queue every second

    periodic_update()
