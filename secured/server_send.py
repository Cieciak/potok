import CPPP, sys

name, address, port = sys.argv
print(f'Address: {address}\nPort: {port}')


ATOMS = {
    4: 2568,
    5: 8976,
    6: 24112,
}

socket = CPPP.SCP3(atoms = ATOMS, threshold = 6, key = 16)

socket.connect(address, int(port))

messages = []
msg = input('>>> ')

while msg:
    messages.append(msg)
    msg = input('>>> ')

socket.send_string(*messages)

print(socket.raw_recv(filter = lambda x: x.decode('utf-8')))