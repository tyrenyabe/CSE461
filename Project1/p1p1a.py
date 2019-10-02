import socket
import ctypes
from struct import pack, unpack
import sys

UDP_IP = "attu2.cs.washington.edu"
UDP_PORT = 12235

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

sock.connect((UDP_IP, UDP_PORT))

message = 'hello world' + '\0'
header = pack('>IIHH', 12, 0, 1, 363) + message.encode('utf-8')

sock.sendto(header, (UDP_IP, UDP_PORT))

ans = sock.recv(1024)
print(unpack('>IIHHIIII', ans))
