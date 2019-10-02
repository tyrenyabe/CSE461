# Receiver Test
import socket

serversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDP_IP = "127.0.0.1"
UDP_PORT = 5005

print("Binding to: ", UDP_IP, " ", UDP_PORT)

serversocket.bind((UDP_IP, UDP_PORT))

# serversocket.listen(10)

print("Server started and listening")

while True:
    # (clientsocket, address) = serversocket.accept()
    # print("Connection found with: ", address)
    # data = clientsocket.recv(1024).decode()
    # print("Received message: ", data)
    # message = "I hear you!"
    # clientsocket.send(message.encode())
    data, addr = serversocket.recvfrom(1024)
    i = 0
    print("Received Message:")
    while i < len(data):
        print(chr(data[i]))
        i += 1