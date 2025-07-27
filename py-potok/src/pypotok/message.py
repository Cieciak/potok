from dataclasses import dataclass, field

from zjadacz import Status
from .parser import potok_message_parser

from .segments import BodySegment, HeaderSegment, BeginSegment

class Message:

    def __init__(self):
        self.begin: BeginSegment  = None
        self.head:  HeaderSegment = None
        self.body:  BodySegment   = None

    @classmethod
    def fromBytes(cls, data: bytes):

        result = potok_message_parser.run(Status(data))

        print(result)