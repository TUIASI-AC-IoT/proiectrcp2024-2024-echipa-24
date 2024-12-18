import Functii_Monitorizare as fm

class MIB:
    CPU_TEMP_OID = [1, 3, 6, 1, 2, 1, 1, 1]
    CPU_UTIL_OID = [1, 3, 6, 1, 2, 1, 1, 2]
    GPU_TEMP_OID = [1, 3, 6, 1, 2, 1, 2, 1]
    GPU_UTIL_OID = [1, 3, 6, 1, 2, 1, 2, 2]
    MEM_UTIL_OID = [1, 3, 6, 1, 2, 1, 3]

    ALERT_TEMP_CPU_OID = [1, 3, 6, 1, 2, 2, 2, 1, 1]
    ALERT_UTIL_CPU_OID = [1, 3, 6, 1, 2, 2, 2, 1, 2]
    ALERT_TEMP_GPU_OID = [1, 3, 6, 1, 2, 2, 2, 2, 1]
    ALERT_UTIL_GPU_OID = [1, 3, 6, 1, 2, 2, 2, 2, 2]
    ALERT_UTIL_MEM_OID = [1, 3, 6, 1, 2, 2, 2, 3]

    cpu_temp = "Celsius"
    gpu_temp = "Celsius"
    alert_temp_cpu = 0
    alert_temp_gpu = 0
    alert_util_cpu = 0
    alert_util_gpu = 0
    alert_util_mem = 0

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

    def Set_Resource(OID: list[int], value):
        match OID:
            case MIB.ALERT_TEMP_CPU_OID:
                if type(value) == float:
                    MIB.alert_temp_cpu = value
            case MIB.ALERT_UTIL_CPU_OID:
                if type(value) == int:
                    MIB.alert_util_cpu = value
            case MIB.ALERT_TEMP_GPU_OID:
                if type(value) == float:
                    MIB.alert_temp_gpu = value
            case MIB.ALERT_UTIL_GPU_OID:
                if type(value) == int:
                    MIB.alert_util_gpu = value
            case MIB.ALERT_UTIL_MEM_OID:
                if type(value) == int:
                    MIB.alert_util_mem = value

