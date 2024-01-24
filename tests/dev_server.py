import CPPP, socket, os, os.path

print('Development server using CPPP')

port = 8000

server = CPPP.Server('0.0.0.0', port)

@server
def init(ctx):
    ctx.path = os.getcwd() 
    ctx.value = "hi mom"
    ctx.buffers = {}

@server.handler('GET')
def f(sock: socket.socket, msg: CPPP.Message, ctx: CPPP.Context):

    return msg

try: server.serve()
except KeyboardInterrupt: print('Server stopped!')