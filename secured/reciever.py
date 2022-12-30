import CPPP, sys

name, address, port = sys.argv
print(f'Address: {address}\nPort: {port}')

ATOMS = {
    1: 12,
    2: 24,
    3: 454,
}

socket = CPPP.SCP3(atoms = ATOMS, threshold = 6)

socket.bind(address, int(port))
socket.listen()

print(socket.recv())

socket.close()