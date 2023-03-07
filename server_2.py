# The simplest echo server
import CPPP, time

server = CPPP.CPPPServer('0.0.0.0', 8000)
PAGE = '''root[root] x[0] y[300] w[500] h[300] color[0,191,179] name[one]
root[root] x[0] y[0] w[900] h[290] color[3,181,170] name[two]
root[two] x[10] y[10] w[880] h[270] color[2,52,54]
root[one] x[10] y[10] w[480] h[100] color[3,121,113]
root[one] x[10] y[120] w[300] h[50] color[4,154,143]'''

@server
def handler(msg: CPPP.CPPPMessage):
    response = CPPP.CPPPMessage(header = {'method': 'RETURN'})
    match msg.header['method']:
        case 'GET':
            response.add_body(bytearray(PAGE, 'utf-8'))
        case _:
            response.add_body(b'')

    return response


try: server.serve()
except KeyboardInterrupt: print('Server stopped!')