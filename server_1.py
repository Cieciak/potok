# The simplest echo server
import CPPP, time

server = CPPP.CPPPServer('0.0.0.0', 8001)
PAGE = '''root[root] x[0] y[0] w[600] h[200] color[167,29,49] name[one]
root[root] x[0] y[210] w[30] h[300] color[213,191,134] name[two]
root[one] x[10] y[10] w[100] h[30] color[63,13,18]
root[two] x[10] y[10] w[10] h[100] color[141,119,95]
root[two] x[10] y[120] w[10] h[100] color[241,240,204]'''

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