import Functii_Monitorizare as fm

class MIB:
    cpu_temp = "Celsius"
    gpu_temp = "Celsius"
    alert_temp_cpu =0
    alert_temp_gpu =0
    alert_util_cpu =0
    alert_util_gpu =0
    alert_util_mem =0
    Mesaj_Eroare = None
    def Get_Resource(OID:str):
        match OID :
            case '1.3.6.1.2.1.1.1' :
                return fm.get_cpu_temp(MIB.cpu_temp)
            case '1.3.6.1.2.1.1.2' :
                return fm.get_cpu_util()
            case '1.3.6.1.2.1.2.1' :
                return fm.get_gpu_temp(MIB.gpu_temp)
            case '1.3.6.1.2.1.2.2' :
                return fm.get_gpu_util()
            case '1.3.6.1.2.1.3' :
                return fm.get_mem_util()
            #case _ :
            #Mesaj_Eroare = "Introducere gresita a datelor" ???

    def Set_Resource(OID:str, value):
        match OID :
            case '1.3.6.1.2.2.1.1' :
                if value in ["Celsius","Kelvin", "Fahrenheit"] :
                    MIB.alert_util_cpu=fm.convert_temp(MIB.alert_temp_cpu,MIB.alert_temp_cpu,value)
                    MIB.cpu_temp = value
                #else trim trap
            case '1.3.6.1.2.2.1.2' :
                if value in ["Celsius","Kelvin", "Fahrenheit"] :
                    MIB.alert_util_gpu=fm.convert_temp(MIB.alert_temp_gpu,MIB.alert_temp_gpu,value)
                    MIB.gpu_temp = value
                #else trim trap
            case '1.3.6.1.2.2.2.1.1' :
                if type(value)==type(2.0) :
                    MIB.alert_temp_cpu=value
                #else trim trap
            case '1.3.6.1.2.2.2.1.2' :
                if type(value)==type(2) :
                    MIB.alert_util_cpu=value
                #else trim trap
            case '1.3.6.1.2.2.2.2.1':
                if type(value)==type(2.0) :
                    MIB.alert_temp_gpu=value
                #else trim trap
            case '1.3.6.1.2.2.2.2.2' :
                if type(value)==type(2) :
                    MIB.alert_util_gpu=value
                #else trim trap
            case '1.3.6.1.2.2.2.3' :
                if type(value)==type(2) :
                    MIB.alert_util_mem=value
                #else trim trap

