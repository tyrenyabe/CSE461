import socket
import fixedint

# Establish header
PAYLOAD = "hello world"
PAYLOAD_LEN = socket.htonl(fixedint.UInt32(len(PAYLOAD)))
PSECRET = socket.htonl(fixedint.UInt32(0))
STEP = socket.htonl(fixedint.UInt16(1))
SID = socket.htonl(fixedint.UInt16(416))

# Concatenate header
HEADER = format(PAYLOAD_LEN, '04d') + format(PSECRET, '04d') + format(STEP, '02d') + format(SID, '02d')

print(len(format(PAYLOAD_LEN, '04d')))

# Pad payload with '\0' until it has a length that is a multiple of 4
while (len(PAYLOAD) % 4 != 0):
    PAYLOAD = PAYLOAD + '\0'

MESSAGE = HEADER + PAYLOAD

print(len(PAYLOAD))
print(len(MESSAGE))

UDP_IP = "attu2.cs.washington.edu"
UDP_PORT = 12235

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

sock.connect((UDP_IP, UDP_PORT))

sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

# print(sock.recv(1024))