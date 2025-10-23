from .segments import BodySegment, HeaderSegment, BeginSegment
from .message import Message

from typing import Self, Callable

import socket
import select

class Server:

    def __init__(self: Self, address: str, port: int):
        self.address: str = address
        self.port: int    = port

        self.alive: bool = False
        self.connections: list[socket.socket] = []
        self.handlers: dict[str, Callable[[Message, Server], Message]] = {}

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((address, port))
        self.server_socket.listen(10)

        self.connections.append(
            self.server_socket
        )        

    def serve(self: Self):
        self.alive = True
        while self.alive:
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
                        msg = Message.from_bytes(raw)
                        handle = self.handlers[msg.begin.method]
                        result = handle(msg, self)

                        socket.sendall(result.to_bytes())

                    else:
                        socket.close()
                        self.connections.remove(socket)

    def method(self: Self, name: str):
        def wrapper(handle: Callable[[Message, Server], Message]):
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

    sock.send(msg.to_bytes())
    sock.shutdown(socket.SHUT_WR)

    response = recvall(sock)
    sock.close()

    return Message.from_bytes(response)

__all__ = [BodySegment, HeaderSegment, BeginSegment, Message]