from dataclasses import dataclass, field
from typing import Any

@dataclass
class BeginSegment:
    name: str    = 'POTOK'
    version: str = '0.0'
    method: str  = ''

@dataclass
class HeaderSegment:
    tags: dict[str, Any] = field(default_factory=dict)

    def __repr__(self):
        return 'Head:\n  ' + '\n  '.join(
            [f'{key}: {val}' for key, val in self.tags.items()]
        )

    def add_tag(self, name: str, value: Any):
        self.tags[name] = value

    def remove_tag(self, name: str):
        del self.tags[name]

@dataclass
class BodySegment:
    raw: bytes = field(default_factory=bytes)

    @classmethod
    def from_bytes(cls, data: bytes):
        new = cls()
        new.load_bytes(data)

        return new

    def __repr__(self) -> str:
        return self.raw.decode('utf-8')

    def load_bytes(self, data: bytes):
        escaped = data.replace(br'-', br'\-')
        self.raw = escaped

    def read_bytes(self) -> bytes:
        decoded = self.raw.replace(br'\-', br'-')
        return decoded