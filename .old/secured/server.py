import CPPP, sys

ATOMS = {
    1: 5,
    2: 21,
}

name, address, port = sys.argv
print(f'Address: {address}\nPort: {port}')

server = CPPP._SCP3Server(out_key = 1,
                          out_atoms = ATOMS,
                          inc_atoms = ATOMS,
                          inc_threshold = 4,
                          address = address,
                          port = int(port))

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