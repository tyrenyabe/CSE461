import socket
import threading
import random
from _thread import *
from time import sleep
from struct import pack, unpack

def ProcessPacket(message, client_ip):
    # Verify header of message
    if (len(message) % 4 != 0):
        return

    payload_len, psecret, step, sid = unpack('>IIHH', message[0:12])
    payload = message[12:12+payload_len]

    if (psecret != 0 or payload_len != 12 or step != 1 or ("hello world" + '\0').encode("utf-8") != payload):
        return
    
    # Send response to client
    udp_ip = "127.0.0.1"
    num = random.randint(5, 20)
    ln = random.randint(24, 500)
    udp_port = random.randint(30000, 42000)
    secretA = random.randint(1, 500)
    response = pack('>IIHHIIII', 16, psecret, 2, sid, num, ln, udp_port, secretA)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(response, client_ip)

    # Bind this new socket to new port
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((udp_ip, udp_port))
    sock.settimeout(3)

    received_messages = 0
    print(num)
    while received_messages < num:
        try:
            message = sock.recv(1024)
        except:
            return
        
        if (random.randint(1, 2) == 2):
            continue
        
        # Verify message contents
        if (len(message) % 4 != 0):
            return

        payload_len, psecret, step, sid, pid = unpack('>IIHHI', message[0:16])
        payload = message[16:16+payload_len]

        if (psecret != secretA or payload_len != ln + 4 or step != 1 or pid != received_messages):
            return
        
        # Form and send response
        response = pack('>IIHHI', 4, psecret, 2, sid, received_messages)
        sock.sendto(response, client_ip)

        received_messages += 1

    # Form and send final response for part B
    tcp_port = random.randint(30000, 42000)
    secretB = random.randint(1, 500)
    response = pack('>IIHHII', 4, psecret, 2, sid, tcp_port, secretB)
    sock.sendto(response, client_ip)


def Main():
    # UDP_IP = "192.168.0.106"
    UDP_IP = "127.0.0.1"
    UDP_PORT = 12235

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))

    while True:
        message, client_ip = sock.recvfrom(1024)
        start_new_thread(ProcessPacket, (message, client_ip))
    sock.close()

if __name__ == '__main__':
    Main()