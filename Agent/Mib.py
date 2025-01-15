from ASN_1.Oid_config import oids
import Functii_Monitorizare as fm

class MIB:
    CPU_TEMP_OID = [1, 3, 6, 1, 2, 1, 1, 1]
    CPU_UTIL_OID = [1, 3, 6, 1, 2, 1, 1, 2]
    GPU_TEMP_OID = [1, 3, 6, 1, 2, 1, 2, 1]
    GPU_UTIL_OID = [1, 3, 6, 1, 2, 1, 2, 2]
    MEM_UTIL_OID = [1, 3, 6, 1, 2, 1, 3]

    CPU_UNIT_OID = [1, 3, 6, 1, 2, 2, 1, 1]
    GPU_UNIT_OID = [1, 3, 6, 1, 2, 2, 1, 2]

    ALERT_TEMP_CPU_OID = [1, 3, 6, 1, 2, 2, 2, 1, 1]
    ALERT_UTIL_CPU_OID = [1, 3, 6, 1, 2, 2, 2, 1, 2]
    ALERT_TEMP_GPU_OID = [1, 3, 6, 1, 2, 2, 2, 2, 1]
    ALERT_UTIL_GPU_OID = [1, 3, 6, 1, 2, 2, 2, 2, 2]
    ALERT_UTIL_MEM_OID = [1, 3, 6, 1, 2, 2, 2, 3]

    cpu_temp = "Celsius"
    gpu_temp = "Celsius"
    alert_temp_cpu = 99
    alert_temp_gpu = 99
    alert_util_cpu = 99
    alert_util_gpu = 99
    alert_util_mem = 15000

    def Get_Resource(OID: list[int]):
        match OID:
            case MIB.CPU_TEMP_OID:
                return fm.get_cpu_temp(MIB.cpu_temp)
            case MIB.CPU_UTIL_OID:
                return fm.get_cpu_util()
            case MIB.GPU_TEMP_OID:
                return fm.get_gpu_temp(MIB.gpu_temp)
            case MIB.GPU_UTIL_OID:
                return fm.get_gpu_util()
            case MIB.MEM_UTIL_OID:
                return fm.get_mem_util()
            case MIB.ALERT_TEMP_CPU_OID:
                return MIB.alert_temp_cpu
            case MIB.ALERT_UTIL_CPU_OID:
                return MIB.alert_util_cpu
            case MIB.ALERT_TEMP_GPU_OID:
                return MIB.alert_temp_gpu
            case MIB.ALERT_UTIL_GPU_OID:
                return MIB.alert_util_gpu
            case MIB.ALERT_UTIL_MEM_OID:
                return MIB.alert_util_mem
            case MIB.CPU_UNIT_OID:
                return MIB.cpu_temp
            case MIB.GPU_UNIT_OID:
                return MIB.gpu_temp
        return "NO ITEM WITH THIS OID"

    def Set_Resource(OID: list[int], value):
        try:
            match OID:
                case MIB.ALERT_TEMP_CPU_OID:
                        MIB.alert_temp_cpu = int(value)
                case MIB.ALERT_UTIL_CPU_OID:
                        MIB.alert_util_cpu = int(value)
                case MIB.ALERT_TEMP_GPU_OID:
                        MIB.alert_temp_gpu = int(value)
                case MIB.ALERT_UTIL_GPU_OID:
                        MIB.alert_util_gpu = int(value)
                case MIB.ALERT_UTIL_MEM_OID:
                        MIB.alert_util_mem = int(value)
                case MIB.CPU_UNIT_OID:
                        MIB.alert_temp_cpu = fm.convert_temp(MIB.alert_temp_cpu, MIB.cpu_temp,value)
                        MIB.cpu_temp = value
                case MIB.GPU_UNIT_OID:
                        MIB.alert_temp_gpu = fm.convert_temp(MIB.alert_temp_gpu, MIB.gpu_temp,value)
                        MIB.gpu_temp = value
        except:
            print("STRING INSTEAD OF INTEGER FOR OID" + str(OID))

    def get_next_oid(OID: list[int]):
        oid_list = list(oids.values())
        oid_index = oid_list.index(OID)
        if oid_index < -1:
            return oid_list[0]
        next_oid_index = (oid_index + 1) % len(oid_list)
        return oid_list[next_oid_index]
