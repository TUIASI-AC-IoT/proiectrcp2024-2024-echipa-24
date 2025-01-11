import Mib as m
import time
import socket
import ASN_1.SNMPPacketBuilder

def sendTrap(manager_ip:str,mesaj:str ,oid:list[int], agent_ip,time_stamp) -> None:
    builder = ASN_1.SNMPPacketBuilder.SNMPPacketBuilder(community='public',version=1)
    trap_packet = builder.build_trap(oid,mesaj,agent_ip,time_stamp)

    manager_port = 162

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.sendto(trap_packet, (manager_ip, manager_port))

def checker(manager_ip,agent_ip):
    begin_time = int(time.time()*100)

    while True:
        crt_time = int(time.time()*100) - begin_time
        # Check CPU temperature
        if m.fm.get_cpu_temp(m.MIB.cpu_temp) > m.MIB.alert_temp_cpu:
            sendTrap(
                manager_ip,
                "Alerta temperatura CPU: " + str(m.fm.get_cpu_temp(m.MIB.cpu_temp)),
                m.MIB.CPU_TEMP_OID,
                agent_ip,
                crt_time,
            )
        # Check GPU temperature
        if m.fm.get_gpu_temp(m.MIB.gpu_temp) > m.MIB.alert_temp_gpu:
            sendTrap(
                manager_ip,
                "Alerta temperatura GPU: " + str(m.fm.get_gpu_temp(m.MIB.gpu_temp)),
                m.MIB.GPU_TEMP_OID,
                agent_ip,
                crt_time
            )
        # Check CPU utilization
        if m.fm.get_cpu_util() > m.MIB.alert_util_cpu:
            sendTrap(
                manager_ip,
                "Alerta utilizare CPU: " + str(m.fm.get_cpu_util()),
                m.MIB.CPU_UTIL_OID,
                agent_ip,
                crt_time
            )
        # Check GPU utilization
        if m.fm.get_gpu_util() > m.MIB.alert_util_gpu:
            sendTrap(
                manager_ip,
                "Alerta utilizare GPU: " + str(m.fm.get_gpu_util()),
                m.MIB.GPU_UTIL_OID,
                agent_ip,
                crt_time
            )
        # Check memory utilization
        if m.fm.get_mem_util() > m.MIB.alert_util_mem:
            sendTrap(
                manager_ip,
                "Alerta utilizare Memorie: " + str(m.fm.get_mem_util()),
                m.MIB.MEM_UTIL_OID,
                agent_ip,
                crt_time,
            )
        time.sleep(1)
