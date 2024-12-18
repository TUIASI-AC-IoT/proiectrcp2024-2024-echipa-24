import Trap_Checker
from threading import Thread

if __name__=='__main__':
    agent_ip = '192.168.0.100'

    t0 = Thread(target = Trap_Checker.checker, args=[agent_ip])
    t0.run()
