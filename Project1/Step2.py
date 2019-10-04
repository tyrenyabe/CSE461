import socket
import threading
from _thread import *
from time import sleep

# Part A - Receive "hello world" from client using UDP protocol
def step_a(message, client_ip):
    print('Bytes :', message)
    print('Address: ', client_ip)

def Main():
    UDP_IP = "192.168.0.106"
    UDP_PORT = 12235

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))

    # while True:
    #     message, client_ip = sock.recvfrom(1024)
    #     start_new_thread(step_a, (message, client_ip))
    # sock.close()

    message, client_ip = sock.recvfrom(1024)
    start_new_thread(step_a, (message, client_ip))
    sleep(5)
    sock.close()

if __name__ == '__main__':
    Main()