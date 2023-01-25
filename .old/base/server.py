import CPPP, sys

name, address, port = sys.argv
print(f'Address: {address}\nPort: {port}')

server = CPPP.CP3Server(address, int(port))

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