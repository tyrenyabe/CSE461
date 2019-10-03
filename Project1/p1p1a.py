import socket
from struct import pack, unpack

UDP_IP = "attu2.cs.washington.edu"
UDP_PORT = 12235

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

message = 'hello world' + '\0'
header = pack('>IIHH', 12, 0, 1, 363) + message.encode('utf-8')

sock.sendto(header, (UDP_IP, UDP_PORT))

ans = sock.recv(1024)

print(unpack('>IIHHIIII', ans))
payload_len, psecret, step, sid, num, ln, UDP_PORT, secretA = unpack('>IIHHIIII', ans)

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

i = 0
while(i < num):
    header = pack('>IIHHI', ln + 4, secretA, 1, 363, i)

    if (ln % 4 != 0):
        payload = bytearray(ln + (4 - (ln % 4)))
    else:
        payload = bytearray(ln)
    message = header + payload

    print(i, " | ", len(message))
    sock.sendto(message, (UDP_IP, UDP_PORT))

    try:
        sock.settimeout(0.5)
        ans = sock.recv(1024)
        print(ans)
    except socket.timeout:
        i -= 1

    i += 1

ans = sock.recv(1024)
print(unpack('>IIHHII', ans))

payload_len, psecret, step, sid, TCP_PORT, secretB = unpack('>IIHHII', ans)
