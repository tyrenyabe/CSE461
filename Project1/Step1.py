import socket
from struct import pack, unpack

# Part A - Send "hello world" to server using UDP protocol
print("Beginning Part A")

UDP_IP = "attu2.cs.washington.edu"
UDP_PORT = 12235

# Initialization of variables to reduce use of magic numbers
INITIAL_SECRET = 0
CLIENT_STEP_NUM = 1
STUDENT_ID = 363
TIMEOUT = 1
QUICK_TIMEOUT = 0.5
BUFFER_LEN = 1024
BYTE_ALIGNMENT = 4

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

message = 'hello world' + '\0'
header = pack('>IIHH', len(message), INITIAL_SECRET, CLIENT_STEP_NUM, STUDENT_ID) + message.encode('utf-8')

sock.sendto(header, (UDP_IP, UDP_PORT))

ans = sock.recv(BUFFER_LEN)

print(unpack('>IIHHIIII', ans))
payload_len, psecret, step, sid, num, ln, UDP_PORT, secretA = unpack('>IIHHIIII', ans)

# Part B - send set of packets to server and make sure the server responds
# indicating that the packets have been received using UDP protocol
print("Beginning Part B")

i = 0
while(i < num):
    header = pack('>IIHHI', ln + BYTE_ALIGNMENT, secretA, CLIENT_STEP_NUM, STUDENT_ID, i)

    if (ln % BYTE_ALIGNMENT != 0):
        payload = bytearray(ln + (BYTE_ALIGNMENT - (ln % BYTE_ALIGNMENT)))
    else:
        payload = bytearray(ln)
    message = header + payload

    sock.sendto(message, (UDP_IP, UDP_PORT))

    try:
        sock.settimeout(QUICK_TIMEOUT)
        ans = sock.recv(BUFFER_LEN)
    except socket.timeout:
        i -= 1

    i += 1

ans = sock.recv(BUFFER_LEN)
print(unpack('>IIHHII', ans))

payload_len, psecret, step, sid, TCP_PORT, secretB = unpack('>IIHHII', ans)

# Part C - Connect to server using TCP protocol and extract information from received packet
print("Beginning Part C")

TCP_IP = "attu2.cs.washington.edu"

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((TCP_IP, TCP_PORT))

sock.settimeout(TIMEOUT)
ans = sock.recv(BUFFER_LEN)

print(unpack('>IIHHIIIcccc', ans))

payload_len, psecret, step, sid, num2, ln2, secretC, c, _, _, _ = unpack('>IIHHIIIcccc', ans)

# Part D - Send set of packets each with a previously specified length that are filled with
# the provided character from Part C
print("Beginning Part D")
header = pack('>IIHH', ln2, secretC, CLIENT_STEP_NUM, STUDENT_ID)

payload = c
i = 1

if (ln2 % BYTE_ALIGNMENT == 0):
    while (i < ln2):
        payload += c
        i += 1
else:
    while (i < (ln2 + (BYTE_ALIGNMENT - ln2 % BYTE_ALIGNMENT))):
        payload += c
        i += 1

message = header + payload

for i in range(num2):
    sock.sendto(message, (TCP_IP, TCP_PORT))

sock.settimeout(TIMEOUT)
ans = sock.recv(BUFFER_LEN)

payload_len, psecret, step, sid, secretD = unpack('>IIHHI', ans)

print(unpack('>IIHHI', ans))
