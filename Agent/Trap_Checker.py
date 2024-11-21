import Mib as m
import time

def checker():
    while(1) :
        if m.fm.get_cpu_temp(m.MIB.cpu_temp) > m.MIB.alert_temp_cpu :
            print("Alerta temperatura CPU", m.fm.get_cpu_temp(m.MIB.cpu_temp))
        if m.fm.get_gpu_temp(m.MIB.gpu_temp) > m.MIB.alert_temp_gpu :
            print("Alerta temperatura GPU",m.fm.get_gpu_temp(m.MIB.gpu_temp))
        if m.fm.get_cpu_util() > m.MIB.alert_util_cpu:
            print("Alerta utilizare CPU",m.fm.get_cpu_util())
        if m.fm.get_gpu_util() > m.MIB.alert_util_gpu:
            print("Alerta utilizare GPU",m.fm.get_gpu_util())
        if m.fm.get_mem_util() > m.MIB.alert_util_mem:
            print("Alerta utilizare Memorie",m.fm.get_mem_util())

        time.sleep(1)
