import Trap_Checker
from threading import Thread
import Comm

if __name__=='__main__':
    input("Open OpenHardwareManager please")
    agent_ip = input("Agent IP: ")
    manager_ip = input("Manager IP: ")
    trap_thread = Thread(target = Trap_Checker.checker, args=[manager_ip, agent_ip])
    trap_thread.start()

    comm_thread = Thread(target=Comm.start_agent,args=[agent_ip])
    comm_thread.start()
