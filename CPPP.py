import socket, select
import time

NAME_REGEX = r"[a-zA-Z]+"

def recvall(sock: socket.socket, bufsize: int) -> bytearray:
    output = b''
    while True:
        raw_data = sock.recv(bufsize)
        if not raw_data: return output
        output += raw_data
    
def send_request(address: str, port: int, data: bytearray):
    s = socket.socket()
    s.connect((address, port))
    s.sendall(data)
    s.close()

class CPPPServer:

    MAX_BUFFER = 4096

    def __init__(self, address: str, port: int) -> None:
        # Save server address and port
        self.address = address
        self.port = port

        # Create socket and make a list to keep track of the connections
        self.connections: list[socket.socket] = []
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((address, port))
        self.server_socket.listen(10)

        # Add self to connections
        self.connections += [self.server_socket,]

    def serve(self):
        while True:
            read, write, error = select.select(self.connections, [], [])

            for socket in read:
                if socket == self.server_socket:
                    incoming, address = self.server_socket.accept()
                    self.connections.append(incoming)
                    print(f'New connection from {address}')
                else:
                    raw_data = recvall(socket, self.MAX_BUFFER)
                    if raw_data:
                        print(raw_data)
                    else:
                        socket.close()
                        self.connections.remove(socket)