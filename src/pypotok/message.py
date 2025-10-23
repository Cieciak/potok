from zjadacz import Status

from .segments import BeginSegment, HeaderSegment, BodySegment
from .parser import potok_message_parser


class Message:

    def __init__(self, begin: BeginSegment = None, head: HeaderSegment = None, body: BodySegment = None):
        self.begin: BeginSegment  = begin
        self.head:  HeaderSegment = head
        self.body:  BodySegment   = body

    @classmethod
    def empty(cls, name: str = 'POTOK', version: str = '0.0', method: str = 'NONE'):
        msg = cls()
        msg.begin = BeginSegment(name, version, method)

        return msg

    @classmethod
    def response(cls, payload: bytes):
        msg = cls()

        msg.begin = BeginSegment(method='RESPONSE')
        msg.head  = HeaderSegment({'valid': 'True'})
        msg.body  = BodySegment(payload)

        return msg

    @classmethod
    def from_bytes(cls, data: bytes):
        status = potok_message_parser.run(Status(data))

        # Throw an error if can't parse the data
        if not isinstance(status, Status):
            print(status)
            raise ValueError('Error while parsing raw data')
        
        begin  = BeginSegment(**status.result[0])
        
        # All tags as one dict
        tags = {}
        for element in status.result[1]:
            tags.update(element)
        header = HeaderSegment(tags)

        body = BodySegment(status.result[2])

        msg = cls()
        msg.begin = begin
        msg.head  = header
        msg.body  = body

        return msg

    def to_bytes(self):
        msg = bytearray()

        msg += b'-INIT-\n'
        msg += self.begin.name.encode('utf-8') + b'\n'
        msg += self.begin.version.encode('utf-8') + b'\n'
        msg += self.begin.method.encode('utf-8') + b'\n'

        msg += b'-HEAD-\n'
        for name, value in self.head.tags.items():
            msg += f'{name}: {value}\n'.encode('utf-8')

        msg += b'-BODY-\n'
        msg += self.body.raw

        return bytes(msg)