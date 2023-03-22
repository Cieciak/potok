import CPPP

print('Calculator server using CPPP')

port = int(input('Enter port: '))

server = CPPP.CPPPServer('0.0.0.0', port)

@server
def handler(msg: CPPP.CPPPMessage):
    response = CPPP.CPPPMessage(header = {'method': 'RETURN'})
    match msg.header['method']:
        case 'GET':
            print(msg.body)
            response.add_body(bytearray(str(eval(msg.body)), 'utf-8'))
        case _:
            response.add_body(b'')

    return response


try: server.serve()
except KeyboardInterrupt: print('Server stopped!')