import CPPP

ATOMS = {
    1: -1,
    2: 24,
    3: 193,
}

socket = CPPP.SCP3(atoms = ATOMS, threshold = 6)

socket.bind('127.0.0.1', 8001)
socket.listen()

print(socket.recv())

socket.close()