import CPPP, sys

name, address, port = sys.argv
print(f'Address: {address}\nPort: {port}')

ATOMS = {
    3: 365,
    4: 1366,
    6: 9332,
}

socket = CPPP._SCP3(inc_atoms = ATOMS, inc_threshold = 6)

socket.bind(address, int(port))
socket.listen()

print(socket.recv())

socket.close()