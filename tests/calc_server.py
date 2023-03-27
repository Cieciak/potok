import CPPP, time

print('Calculator server using CPPP')

port = int(input('Enter port: '))

server = CPPP.CPPPServer('0.0.0.0', port)

@server
def setup(ctx):
    ctx.n = 0

@server
def handler(msg: CPPP.CPPPMessage, ctx):
    ctx.n += 1
    response = CPPP.CPPPMessage(header = {'method': 'RETURN'})
    match msg.header['method']:
        case 'GET':
            print(msg.body)
            response.add_body(bytearray(str(eval(msg.body))+ f', Operation number: {ctx.n}', 'utf-8'))
        case _:
            response.add_body(b'')

    return response



try: server.serve()
except KeyboardInterrupt: print('Server stopped!')