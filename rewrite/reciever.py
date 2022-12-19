#from main import CPPP
import socket

sock = socket.socket()

sock.bind(('0.0.0.0', 8001))
sock.listen()

conn, addr = sock.accept()

while conn:
    while True:

        data = conn.recv(1024)

        if not data: break
        conn.sendall(data)
