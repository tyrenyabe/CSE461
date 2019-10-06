import socket
import threading
import random
from _thread import *
from time import sleep
from struct import pack, unpack

## TODO Test on attu, clean up code(?)

# Anti-magic variables
HEADER_LEN = 12
INITIAL_SECRET = 0
SERVER_STEP_NUM = 2
CLIENT_STEP_NUM = 1
BYTE_ALIGNMENT = 4
FOUR_BYTE_INT = 4
BUFFER_LEN = 1024
CLIENT_BACKLOG = 10
SERVER_TIMEOUT = 3

def ProcessPacket(message, client_ip):
    # Part A
    # Verify header of message
    EXPECTED_PAYLOAD = "hello world" + '\0'
    EXPECTED_MESSAGE_LEN = HEADER_LEN + len(EXPECTED_PAYLOAD)

    if (len(message) != EXPECTED_MESSAGE_LEN):
        return

    payload_len, psecret, step, sid = unpack('>IIHH', message[0:12])
    payload = message[12:12+payload_len]

    if (psecret != INITIAL_SECRET or payload_len != len(EXPECTED_PAYLOAD) \
    or step != CLIENT_STEP_NUM or EXPECTED_PAYLOAD.encode("utf-8") != payload):
        return
    
    # Send response to client
    udp_ip = "127.0.0.1"

    # No random number generation guidlines were provided, so
    # bounds were used that we found to be decent
    num = random.randint(5, 20)
    ln = random.randint(24, 500)
    udp_port = random.randint(30000, 42000)
    secretA = random.randint(1, 500)

    response = pack('>IIHHIIII', 4 * FOUR_BYTE_INT, psecret, SERVER_STEP_NUM, sid, num, ln, udp_port, secretA)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(response, client_ip)

    # Part B
    # Create new socket and bind to new port that was passed to client
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((udp_ip, udp_port))
    sock.settimeout(SERVER_TIMEOUT)

    EXP_PADDED_PAYLOAD_LN = ln + FOUR_BYTE_INT
    if (EXP_PADDED_PAYLOAD_LN % BYTE_ALIGNMENT != 0):
        EXP_PADDED_PAYLOAD_LN = ln + FOUR_BYTE_INT + (BYTE_ALIGNMENT - (ln % BYTE_ALIGNMENT))

    EXPECTED_MESSAGE_LEN = HEADER_LEN + EXP_PADDED_PAYLOAD_LN

    received_messages = 0
    while received_messages < num:
        try:
            message = sock.recv(BUFFER_LEN)
        except:
            return
        
        # 50% chance to ignore message
        if (random.randint(1, 2) == 2):
            continue
        
        # Verify message contents
        if (len(message) != EXPECTED_MESSAGE_LEN):
            return

        payload_len, psecret, step, sid, pid = unpack('>IIHHI', message[0:HEADER_LEN + FOUR_BYTE_INT])
        payload = message[HEADER_LEN + FOUR_BYTE_INT:HEADER_LEN + FOUR_BYTE_INT + payload_len]

        if (psecret != secretA or payload_len != ln + FOUR_BYTE_INT or step != CLIENT_STEP_NUM or pid != received_messages):
            return
        
        # Form and send response
        response = pack('>IIHHI', FOUR_BYTE_INT, psecret, SERVER_STEP_NUM, sid, received_messages)
        sock.sendto(response, client_ip)

        received_messages += 1

    # Form and send final response for part B
    # No random number generation guidlines were provided, so
    # bounds were used that we found to be decent
    tcp_port = random.randint(30000, 42000)
    secretB = random.randint(1, 500)
    response = pack('>IIHHII', FOUR_BYTE_INT, psecret, SERVER_STEP_NUM, sid, tcp_port, secretB)
    sock.sendto(response, client_ip)

    # Part C
    # Bind socket to new TCP port
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((udp_ip, tcp_port))
    sock.listen(CLIENT_BACKLOG)
    connection, client_address = sock.accept()

    # No random number generation guidlines were provided, so
    # bounds were used that we found to be decent
    num = random.randint(5, 20)
    ln = random.randint(24, 500)
    secretC = random.randint(1, 500)
    special_char = chr(random.randint(0, 100)) # Randomly generates some ASCII character
    buffer = special_char + "xxx"              # Append 3 characters to align to four bytes
    response = pack('>IIHHIII', 3 * FOUR_BYTE_INT + len(special_char), secretB, SERVER_STEP_NUM, sid, num, ln, secretC) + buffer.encode("ascii")
    connection.sendto(response, client_address)
    
    # Part D
    received_messages = 0
    sock.settimeout(SERVER_TIMEOUT)
    message_length = HEADER_LEN + ln

    if (message_length % BYTE_ALIGNMENT != 0):
        message_length += (BYTE_ALIGNMENT - message_length % BYTE_ALIGNMENT)

    while received_messages < num:
        try:
            message = connection.recv(message_length)
        except:
            return
        
        # Verify message contents
        if (len(message) != message_length):
            return

        payload_len, psecret, step, sid = unpack('>IIHH', message[0:HEADER_LEN])
        payload = message[HEADER_LEN:HEADER_LEN + ln]

        if (psecret != secretC or payload_len != ln or step != CLIENT_STEP_NUM):
            return

        for i in range(ln):
            if chr(payload[i]) != special_char:
                return

        received_messages += 1

    # No random number generation guidlines were provided, so
    # bounds were used that we found to be decent
    secretD = random.randint(1, 500)
    response = pack('>IIHHI', FOUR_BYTE_INT, secretC, SERVER_STEP_NUM, sid, secretD)
    connection.sendto(response, client_address)


def Main():
    UDP_IP = "127.0.0.1"
    UDP_PORT = 12235

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))

    while True:
        message, client_ip = sock.recvfrom(BUFFER_LEN)
        start_new_thread(ProcessPacket, (message, client_ip))
    sock.close()

if __name__ == '__main__':
    Main()