import CPPP, socket, os, os.path

print('Development server using CPPP')

port = 8000

server = CPPP.Server('0.0.0.0', port)

def create_buffer(ctx: CPPP.Context, path: str, _id):
        ctx.buffers[_id] = open(path)

def read_buffer(ctx, _id, n):
    return ctx.buffers[_id].read(n)

def close_buffer(ctx: CPPP.Context, _id):
    ctx.buffers[_id].close()

@server
def init(ctx):
    ctx.path = os.getcwd() 
    ctx.value = "hi mom"
    ctx.buffers = {}

@server.handler('GET')
def f(sock: socket.socket, msg: CPPP.Message, ctx: CPPP.Context):
    result = CPPP.Message.response(bytes(ctx.value, 'utf-8'))

    return  result

@server.handler('PUT')
def g(sock: socket.socket, msg: CPPP.Message, ctx: CPPP.Context):
    ctx.value = msg.body.decode('utf-8')

    result = CPPP.Message.response(bytes('PUT was succesful', 'utf-8'))

    return result

@server.handler('PIPE')
def pipe(sock: socket.socket, msg: CPPP.Message, ctx: CPPP.Context):
    path = msg.head['localization']
    whoami = msg.head['whoami']

    print(whoami)
    if not ctx.buffers.get(whoami, None): create_buffer(ctx, path, whoami)

    print(os.path.join(ctx.path, path))

    return CPPP.Message.response(read_buffer(ctx, whoami, 10))


try: server.serve()
except KeyboardInterrupt: print('Server stopped!')