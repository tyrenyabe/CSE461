# Send message test
import socket
import struct

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
# MESSAGE = bytes([socket.htonl(fixedint.UInt32(100))])
MESSAGE = struct.pack('!I', 461) + "Sup"

print(MESSAGE)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))