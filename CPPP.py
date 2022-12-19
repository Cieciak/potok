import socket, pprint

HOST = "127.0.0.1"
PORT = 2000

byte = lambda x: bytearray([x,])

def print_bytes(_iter: bytearray):
    for byte in _iter:
        print(f'{byte:<3}', end=' ')

class CPPP:

    MAX_LEN = 1024

    @staticmethod
    def translate_message(message: bytearray):
        # Make a copy of the message
        to_process = message.copy()

        # Create output bytes
        output: bytearray = bytearray()
        while to_process:

            # Split to chunks with max size 255 bytes
            chunk      = to_process[:255]
            to_process = to_process[255:]

            # If max size chunk 
            if len(chunk) == 255 and to_process: output += byte(0xFF) + chunk + byte(0x00)
            else: output += byte(len(chunk)) + chunk

        return output

    @staticmethod
    def create_header(address: tuple[int], port: int, config: int):
        output: bytearray = bytearray()

        # Take care of 4 first bytes
        for number in address:
            output += byte(number)

        output += byte(port // 256) # Top half of the port
        output += byte(port  % 256) # Bottom half of the port
        output += byte(config)      # Config byte
        output += byte(0xBD)        # Reserved

        return output

    @staticmethod
    def create_packet(address: tuple[int], port: int, messages: list[str], *, config: int = 0x00):

        raw_bytearray: bytearray = bytearray()
        output_packets: list[bytearray] = []

        for message in messages:
            raw_bytearray += CPPP.translate_message(bytearray(message, 'utf-8'))

        while raw_bytearray:
            body          = raw_bytearray[:1016]
            raw_bytearray = raw_bytearray[1016:]

            if not raw_bytearray: config = config | 0x80
            else: config = config & 0x7F

            output_packets.append(CPPP.create_header(address, port, config) + body)

            if raw_bytearray: config = config | 0x01
            else: config = config & 0xFE

        return output_packets

    @staticmethod
    def read_body(packet: bytearray):
        # Make a copy of the recieved packet
        raw = packet.copy()

        messages = []
        message = bytearray()

        # Get the first step
        step = raw.pop(0)
        flag = 1

        while raw:
            # Get the fist frame of data
            data = raw[:step]
            raw  = raw[step:]

            # If you can get the next byte
            if raw: flag = raw.pop(0)

            message += data
            # If its 0x00 it's long frame, then get legnth of the next segment
            if flag == 0: 
                step = raw.pop(0)
            # If not add gathered message to the list
            else:
                messages.append(message)
                message = bytearray()
                step = flag

        # After nothing is left return
        return messages

    def __init__(self, sock: socket.socket = None) -> None:
        # If socket not given make new one
        if sock is None: self.socket = socket.socket()
        else: self.socket = socket.socket()

        self.recv_address: tuple[int]
        self.recv_port: int

        self.serve = -1

    def __repr__(self) -> str:
        return f'{self.recv_address}:{self.recv_port}'

    def connect(self, host: str, port: int) -> None:
        self.recv_address = tuple(int(val) for val in host.split('.'))
        self.recv_port    = port

        self.socket.connect((host, port))

    def send(self, *messages):
        # List of messages to send in the request
        RAW_PACKETS = CPPP.create_packet(self.recv_address, self.recv_port, messages)
        for packet in RAW_PACKETS:
            self.socket.send(packet)

    def sendconn(self, address, port, conn, *messages):
        # List of messages to send in the request
        RAW_PACKETS = CPPP.create_packet(address, port, messages)
        for packet in RAW_PACKETS:
            conn.send(packet)


    def close(self):
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()

    def bind(self, host, port):
        self.socket.bind((host, port))

    def listen(self):
        self.socket.listen()

    def recv(self):
        while True:
            conn, addr = self.socket.accept()
            rest = bytearray()

        # TODO: END bit chect to exit
            while conn:
                while True:
                    if not conn: break
                    raw_data = conn.recv(1024)
                    print(f'Raw data: {raw_data}')

                    if not raw_data: break
                    header = raw_data[:8]
                    rest  += raw_data[8:]

            return header, CPPP.read_body(rest), conn, addr
        # while True:
        #     # Establish connection
        #     conn, addr = self.socket.accept()
        #     rest = bytearray()
        #     # Get the packet
        #     print('Recieved the request')
        #     while True:
        #         raw_data = conn.recv(1024)
        #         print(f'Dada {raw_data}')
        #         if not raw_data: break
        #         header = raw_data[:8]
        #         rest  += raw_data[8:]

        #     print(rest)
        #     return header, CPPP.read_body(rest), conn, addr

# conn, addr = sock.accept()

# while conn:
#     while True:

#         data = conn.recv(1024)

#         if not data: break
#         conn.sendall(data)

    def raw_recv(self):
        request = bytearray()
        while True:
            raw_data = self.socket.recv(1024)
            if not raw_data: break
            header   = raw_data[:8]
            request += raw_data[8:]

        return header, CPPP.read_body(request)

class CP3Server:

    def __init__(self, address: str, port: int) -> None:
        self.socket = CPPP()
        self.socket.bind(address, port)

        self.alive = True

    def listen(self):
        self.socket.listen()

    def serve(self):

        while self.alive:
            head, body, conn, addr = self.socket.recv()
            print('RECIEVED')
            address = [int(i) for i in addr[0].split('.')]
            port = addr[1]

            print(f'Recieved {head} from {addr}')
            self.socket.sendconn(address, port, conn, 'Hello')

