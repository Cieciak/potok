import CPPP

server = CPPP.CP3Server('127.0.0.1', 8001)

@server
def handle(x: list[bytearray]):
    response = []
    for msg in x:
        print(msg)
        response.append(msg)

    return response


server.listen()
try:
    server.serve()
except KeyboardInterrupt:
    server.close()
    print('Server closed')

