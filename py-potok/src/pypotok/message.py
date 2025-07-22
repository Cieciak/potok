from dataclasses import dataclass, field

@dataclass
class BeginSegment:
    name: str = 'POTOK'
    version: str = '0.1'
    method: str = ''

@dataclass
class HeaderSegment:
    tags: dict = field(default_factory=dict)

@dataclass
class BodySegment:
    raw: bytearray = field(default_factory=bytearray)

type Segment = BeginSegment | HeaderSegment | BodySegment

class Message:

    def __init__(self):
        self.begin: BeginSegment  = None
        self.head:  HeaderSegment = None
        self.body:  BodySegment   = None