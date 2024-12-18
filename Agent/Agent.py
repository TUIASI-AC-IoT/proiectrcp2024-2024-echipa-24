import threading
import socket


import Trap_Checker
from threading import Thread

if __name__=='__main__':
    t0 = Thread(target = Trap_Checker.checker, args=[])
    t0.run()

