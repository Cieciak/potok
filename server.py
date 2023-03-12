# The simplest echo server
import CPPP, time

server = CPPP.CPPPServer('0.0.0.0', 8000)
HEAD = {'method': 'RESPONSE'}

TEST = '''root[] x[20] y[20] w[10] h[100] color[123, 54, 34] name[one]0
root[] x[220] y[220] w[100] h[10] color[12, 154, 234] name[two]'''

@server
def handler(msg: CPPP.CPPPMessage):
    response = CPPP.CPPPMessage(header = HEAD)
    print(msg)
    match msg.header['method']:
        case 'GET':
            response.add_body(bytearray(TEST, 'utf-8'))
        case _:
            response.add_body(b'')
    print(response)
    return response


try: server.serve()
except KeyboardInterrupt: print('Server stopped!')
