import socket

class CPPP:

    def __init__(self, sock: socket.socket = None):
        
        if sock is None: self.socket = socket.socket()
        else: self.socket = sock

        self.recv_address: tuple[int]
        self.recv_port: int

    def connect(self, host: str, port: int):
        self.socket.connect((host, port))

    def send(self, message):
        self.socket.send(bytearray(message, 'UTF-8'))

    def close(self):
        self.socket.close()

    def raw_recive(self):
        raw_data = self.socket.recv(1024)
        return raw_data

    def recv(self):
        connection, address = self.socket.accept()
        request = bytearray()

        while True:
            raw_data = connection.recv(1024)
            if request and not raw_data:break
            header   = raw_data[:8]
            request += raw_data[8:]

        return request
