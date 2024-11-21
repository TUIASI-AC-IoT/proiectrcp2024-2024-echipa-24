import psutil
import WinTmp
import wmi
import GPUtil


def get_cpu_temp(temp)->float:
    sum = 0
    k = 0
    w = wmi.WMI(namespace="root/OpenHardwareMonitor")
    temperature_infos = w.Sensor()
    for sensor in temperature_infos:
        if sensor.SensorType==u'Temperature':
            sum+=sensor.Value
            k+=1
    if k==0:
        raise Exception("OpenHardwareMonitor")
    temperature = sum/k
    if temp=="Celsius":
        return temperature
    elif temp == "Kelvin" :
        return temperature + 273.15
    elif temp == "Fahrenheit":
        return temperature*9/5+32


def get_cpu_util()->int :
    return int(psutil.cpu_percent(interval=1))


def get_gpu_temp(temp)->float:
    if temp=="Celsius":
        return WinTmp.GPU_Temp()
    elif temp == "Kelvin" :
        return WinTmp.GPU_Temp()+ 273.15
    elif temp == "Fahrenheit":
        return WinTmp.GPU_Temp()*9/5+32


def get_gpu_util()->int :
    gpus = GPUtil.getGPUs()
    for gpu in gpus:
        return int((gpu.load*100))

def get_mem_util()->int :
    return float((psutil.virtual_memory()[0]-psutil.virtual_memory()[1])/2**30)


def convert_temp(temp ,unit1,unit2) :
    if unit1 == 'Celsius' :
        match unit2 :
            case 'Fahrenheit' :
                return temp*9/5+32
            case "Kelvin" :
                return temp+273.15

    elif unit1 == 'Fahrenheit' :
        match unit2 :
            case 'Celsius' :
                return (temp-32)/1.8
            case "Kelvin" :
                return (temp+459.67)/5*9

    elif unit1 == 'Kelvin' :
        match unit2 :
            case 'Celsius' :
                return temp-273.15
            case "Fahrenheit" :
                return temp*9/5-459.67

    return temp
