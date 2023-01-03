import CPPP, sys

name, address, port = sys.argv
print(f'Address: {address}\nPort: {port}')

ATOMS = {
    3: 41,
    4: 86,
}

socket = CPPP.SCP3(atoms = ATOMS, threshold = 4, key = 2)

socket.connect(address, int(port))

messages = []
msg = input('>>> ')

while msg:
    messages.append(msg)
    msg = input('>>> ')

socket.send_string(*messages)

print(socket.raw_recv(filter = lambda x: x.decode('utf-8')))