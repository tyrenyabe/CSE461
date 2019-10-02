# Send message test
import socket
import fixedint

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
MESSAGE = str(socket.htonl(fixedint.UInt32(100)))

print(100)
print(MESSAGE)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))