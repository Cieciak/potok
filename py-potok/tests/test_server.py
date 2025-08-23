import pypotok

addr = '0.0.0.0'
port = 8100

server = pypotok.Server(addr, port)



@server.method('GET')
def echo(msg: pypotok.Message, srv: pypotok.Server):
    return msg

try: server.serve()
except KeyboardInterrupt: print('Server stopped!')