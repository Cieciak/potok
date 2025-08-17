from .message import Message, BeginSegment, HeaderSegment, BodySegment
from typing import Self, Callable

import socket
import select

type Handler = Callable[[Message, Server], Message]

class Server:

    def __init__(self: Self, address: str, port: int):
        
        self.address: str = address
        self.port: int    = port

        self.connections: list[socket.socket] = []
        self.handlers: dict[str, Handler] = {}

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((address, port))
        self.server_socket.listen(10)

        self.connections.append(
            self.server_socket
        )
    
    def serve(self: Self):
        while True:
            read, write, error = select.select(self.connections, [], [])

            for socket in read:
                # Handle incoming to server socket
                if socket == self.server_socket:
                    incoming, address = self.server_socket.accept()
                    self.connections.append(incoming)
                # Handle messages from others
                else:
                    raw = recvall(socket)
                    if raw:
                        msg = Message.fromBytes(raw)
                        
                        handle = self.handlers[msg.begin.method]

                        result = handle(msg, self)

                        socket.sendall(result.toBytes())

                    else:
                        socket.close()
                        self.connections.remove(socket)

    def method(self: Self, name: str):
        def wrapper(handle: Handler):
            self.handlers[name] = handle

        return wrapper



def recvall(sock: socket.socket) -> bytes:
    """Receive all data until the socket is closed."""
    data = bytearray()
    while True:
        packet = sock.recv(4096)  # read in chunks
        if not packet:  # connection closed
            break
        data.extend(packet)
    return bytes(data)



def request(address: str, port: int, msg: Message) -> Message:
    sock = socket.socket()
    sock.connect((address, port))

    sock.send(msg.toBytes())
    sock.shutdown(socket.SHUT_WR)

    response = recvall(sock)
    sock.close()

    return Message.fromBytes(response)