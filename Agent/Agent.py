import Trap_Checker
from threading import Thread

if __name__=='__main__':
    agent_ip = '127.0.0.1'
    manager_ip = '127.0.0.1'
    t0 = Thread(target = Trap_Checker.checker, args=[manager_ip, agent_ip])
    t0.run()
