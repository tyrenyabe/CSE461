# Receiver Test
import socket
import struct

serversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDP_IP = "127.0.0.1"
UDP_PORT = 5005

print("Binding to: ", UDP_IP, " ", UDP_PORT)

serversocket.bind((UDP_IP, UDP_PORT))

print("Server started and listening")

while True:
    data, addr = serversocket.recvfrom(1024)
    print("Received Message:")
    ID = struct.unpack('!I', data[:4])[0]
    print(ID)
    PAYLOAD = data[4::]
    i = 0
    while i < len(PAYLOAD):
        print(chr(PAYLOAD[i]))
        i += 1