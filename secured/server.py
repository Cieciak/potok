import CPPP, sys

ATOMS = {
    1: 5,
    2: 16,
}

name, address, port = sys.argv
print(f'Address: {address}\nPort: {port}')

server = CPPP.SCP3Server(address, int(port), atoms = ATOMS, threshold = 4, key = 2)

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