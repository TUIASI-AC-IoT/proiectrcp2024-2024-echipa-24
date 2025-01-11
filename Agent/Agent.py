import Trap_Checker
from threading import Thread

if __name__=='__main__':
    input("Open OpenHardwareManager please")
    agent_ip = input("Agent IP: ")
    manager_ip = input("Agent IP: ")
    trap_thread = Thread(target = Trap_Checker.checker, args=[manager_ip, agent_ip])
    trap_thread.run()
