import socket
from struct import pack, unpack

UDP_IP = "attu2.cs.washington.edu"
UDP_PORT = 40047

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

header = pack('>IIHH', 54, 53, 1, 363)

payload = bytearray(56)
message = header + payload

sock.sendto(message, (UDP_IP, UDP_PORT))
sock.settimeout(0.5)
ans = sock.recv(1024)

print(ans)