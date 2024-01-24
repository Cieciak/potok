import socket, select, os, os.path, uuid
import pprint, types, json, typing
from parser.message_parser import TempParser, CPPP_JSON_Encoder

import threading

def recvall(sock: socket.socket, bufsize: int) -> bytes:
    output = b''
    while True:
        raw_data = sock.recv(bufsize)
        output += raw_data
        if not raw_data or output.endswith(b'}\01\01'): return output

class Context(object):
    ...

class Message:
    parser: TempParser = TempParser()

    def __init__(self, raw_data: bytes = None, head: dict = None, body: bytearray = None):
        self.__raw: bytes = raw_data

        if raw_data:
            self.head, self.body = self.parser.parse(raw_data)
        else:
            self.head:      dict = head
            self.body: bytearray = body

    def __repr__(self) -> str:
        return f'Header: {pprint.pformat(self.head, indent = 4)}\nBody: [\n{self.body}\n]'

    @classmethod
    def empty(cls):
        return cls(head = {'method': 'NONE'}, body = b'')

    @classmethod
    def error(cls, name: str, reason: str = None):
        message = f'Error {name}\nReason: {reason}'

        return cls(
            head = {'method': 'ERROR'},
            body = bytes(message, 'utf-8')
        )

    @classmethod
    def response(cls, payload: bytes):
        return cls(
            head = {'method': 'RESPONSE'},
            body = payload
        )

    @property
    def raw(self):
        JSON = {
            'head': self.head,
            'body': self.body,
        }

        self.__raw = bytes(
            json.dumps(
                JSON,
                cls = CPPP_JSON_Encoder,
            ),
            encoding = "utf-8"
        ) + b'\01\01'
        
        return self.__raw

    def add_header(self, header: dict):
        for key, value in header.items(): self.head[key] = value

    def add_body(self, data: bytes):
        self.body = data

class Server:
    MAX_BUFFER = 4096

    def __init__(self, address: str, port: int, *, path = os.getcwd()):
        # Server config
        self.address = address
        self.port = port
        self.root = path
        self.ctx = Context()
        self.ctx.whoami = uuid.uuid4()

        # Function table
        self.function_table: dict[str, function] = {}
        self.handler_table: dict[str, function] = {}

        # Create socket and make a list to keep track of the connections
        self.connections: list[socket.socket] = []
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((address, port))
        self.server_socket.listen(10)

        # Add self to connection
        self.connections += [self.server_socket, ]

    def __call__(self, function: types.FunctionType):
        self.function_table[function.__name__] = function

    def __task(self, sock: socket.socket, msg: Message):
        method = str(msg.head['method'])
        
        task = self.__handler(method, sock, msg)

        if task: task.start()
        else:
            error = Message.error('Handler Not Implemented', f'Cannot find handler for \"{method}\"')
            sock.sendall(error.raw)

    def __handler(self, method: str, sock: socket.socket, msg: Message) -> threading.Thread:
        handler = self.handler_table.get(method, None)
        if handler == None: return None

        task = threading.Thread(
            group = None,
            target = handler,
            kwargs = {'sock': sock, 'msg': msg, 'ctx': self},
            daemon = True,
        )

        return task

    def handler(self, name: str):
        def decorator(func: types.FunctionType):
            def wrapper(sock: socket.socket, msg: Message, ctx: typing.Self):
                result = func(sock, msg, ctx)

                result = result if result else Message.empty()

                sock.sendall(result.raw)

            self.handler_table[name] = wrapper
        return decorator

    def serve(self):
        self.function_table['init'](self.ctx)
        while True:
            read, write, error = select.select(self.connections, [], [])

            for socket in read:
                if socket == self.server_socket:
                    incoming, address = self.server_socket.accept()
                    self.connections.append(incoming)
                else:
                    raw = recvall(socket, self.MAX_BUFFER)

                    if raw:
                        self.__task(socket, Message(raw))
                    else:
                        socket.close()
                        self.connections.remove(socket)

class Client:
    MAX_BUFFER = 4096

    def __init__(self):
        self.whoami = uuid.uuid4()

    def request(self, address: str, port: int, message: Message) -> Message:
        sock = socket.socket()
        sock.connect((address, port))
        message.add_header({'whoami': self.whoami.bytes.hex()})
        sock.sendall(message.raw)

        response = recvall(sock, self.MAX_BUFFER)
        sock.close()

        return Message(raw_data = response)
