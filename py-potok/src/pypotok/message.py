from dataclasses import dataclass, field

from zjadacz import Status
from .parser import potok_message_parser

from .segments import BodySegment, HeaderSegment, BeginSegment

@dataclass
class Message:
    begin: BeginSegment | None = None
    head: HeaderSegment | None = None
    body: BodySegment | None   = None

    @classmethod
    def fromBytes(cls, data: bytes, /):
        msg = cls()
        msg.begin, msg.head, msg.body = potok_message_parser.run(Status(data)).result
        return msg
    
    def toBytes(self):
        begin_segment = f'-BEGIN-\n{self.begin.name}\n{self.begin.version}\n{self.begin.method}\n'
        head_segment = f'-HEAD-\n' + '\n'.join(f'{key}: {val}' for key, val in self.head.tags.items()) + '\n'
        body_segment = b'-BODY-\n' + self.body.raw

        data = bytes(begin_segment, 'utf-8') + bytes(head_segment, 'utf-8') + body_segment

        return data