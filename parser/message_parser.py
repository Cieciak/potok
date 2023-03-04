import json 

class CPPP_JSON_Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytearray):
            return obj.decode('UTF-8')
        elif isinstance(obj, bytes):
            return obj.decode('UTF-8')
        return json.JSONEncoder.default(self, obj)

class TempParser:

    def __init__(self) -> None:
        pass

    def parse(self, raw_data: bytearray) -> tuple[dict, object]:
        parsed = json.loads(raw_data[:-2])
        return parsed['head'], parsed['body']