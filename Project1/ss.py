import socket
import threading
import socketserver
from time import sleep

class ThreadedUDPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        data = str(self.request.recv(1024), 'ascii')
        cur_thread = threading.current_thread()
        response = bytes("{}: {}".format(cur_thread.name, data), 'ascii')
        self.request.sendall(response)

class ThreadedUDPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

def client(ip, port, message):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.sendto(bytes(message, 'ascii'), ("192.168.0.106", 12235))
        # response = str(sock.recv(1024), 'ascii')
        # print("Received: {}".format(response))

if __name__ == "__main__":
    HOST, PORT = "192.168.0.106", 12235

    server = ThreadedUDPServer((HOST, PORT), ThreadedUDPRequestHandler)
    with server:
        ip, port = server.server_address

        # Start a thread with the server -- that thread will then start one
        # more thread for each request
        server_thread = threading.Thread(target=server.serve_forever)
        # Exit the server thread when the main thread terminates
        server_thread.daemon = True
        server_thread.start()
        print("Server loop running in thread:", server_thread.name)

        # client(ip, port, "Hello World 1")
        # client(ip, port, "Hello World 2")
        # client(ip, port, "Hello World 3")
        while(True):
            sleep(5)
        # server.shutdown()