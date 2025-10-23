from zjadacz import Status, ParserError
from zjadacz import choiceOf, many, sequenceOf, future
from zjadacz.string import word

import pypotok

repeats = lambda s: {s.result[0]: len(s.result)}

parser_loop = future()

parser_instruction = choiceOf(
    many(word('+'), strict=True).map(repeats),
    many(word('-'), strict=True).map(repeats),
    many(word('>'), strict=True).map(repeats),
    many(word('<'), strict=True).map(repeats),
    word('.'),
    word(','),
    parser_loop,
)

parser_loop.reassign(sequenceOf(
    word('['),
    many(parser_instruction),
    word(']'),
).map(
    lambda s: {'loop': s.result[1]}
))

parser_program = many(parser_instruction, strict=True)

class AST_Runner:

    def __init__(self, mem_size: int = 30):
        self.memory = [0, ] * mem_size
        self.pointer = 0

    def run(self, tree: Status):
        buffer = ''

        for element in tree:
            if isinstance(element, dict):
                key, *_ = element.keys()
                val, *_ = element.values()
            else:
                key = element

            match key:

                case '+':
                    self.memory[self.pointer] = (self.memory[self.pointer] + val) % 256
                case '-':
                    self.memory[self.pointer] = (self.memory[self.pointer] - val) % 256
                case '>':
                    self.pointer = (self.pointer + val) % len(self.memory)
                case '<':
                    self.pointer = (self.pointer - val) % len(self.memory)
                case 'loop':
                    while self.memory[self.pointer] != 0:
                        self.run(val)
                case '.':
                    buffer += chr(self.memory[self.pointer])
                case ',':
                    self.memory[self.pointer] = ord(input()[0])

        return buffer

addr = '0.0.0.0'
port = 8000

bf_server = pypotok.Server(addr, port)
runner = AST_Runner()

@bf_server.method('GET')
def run_bf_code(msg: pypotok.Message, srv: pypotok.Server):

    s = Status(msg.body.read_bytes().decode('utf-8'))

    r = parser_program.run(s)

    buffer = runner.run(r.result)

    return pypotok.Message.response(bytes(buffer, 'utf-8'))

@bf_server.method('PEEK')
def run_bf_code(msg: pypotok.Message, srv: pypotok.Server):
    limit = int(msg.body.read_bytes().decode('utf-8'))

    memory = runner.memory[:limit]

    return pypotok.Message.response(bytes(', '.join(str(el) for el in memory), 'utf-8'))

try: bf_server.serve()
except KeyboardInterrupt: print('Server stopped!')