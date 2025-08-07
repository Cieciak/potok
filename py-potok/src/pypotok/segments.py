from dataclasses import dataclass, field

@dataclass
class BeginSegment:
    name: str = 'POTOK'
    version: str = '0.0'
    method: str = ''

@dataclass
class HeaderSegment:
    tags: dict = field(default_factory=dict)

    @classmethod
    def fromTaglist(cls, tags: list[dict], /):
        final = dict()

        for tag in tags:
            final = {**tag, **final}

        return cls(final)

@dataclass
class BodySegment:
    raw: bytes = field(default_factory=bytes)
