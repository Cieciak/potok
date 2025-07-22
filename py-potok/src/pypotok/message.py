from dataclasses import dataclass

@dataclass
class BeginSegment:
    name: str = 'POTOK'
    version: str = '0.1'
    method: str = ''