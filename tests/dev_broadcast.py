import CPPP, socket

print('Broadcast server using CPPP')
port = 8000
server = CPPP.Server('0.0.0.0', port)

@server
def init(ctx: CPPP.Context):
    ...

@server.handler('GET')
def get(sock: socket.socket, msg: CPPP.Message, ctx: CPPP.Server):
    print(ctx.connections.__len__())

server.serve()