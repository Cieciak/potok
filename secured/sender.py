import CPPP, sys

name, address, port = sys.argv
print(f'Address: {address}\nPort: {port}')


ATOMS = {
    4: 842,
    5: 2643,
    6: 6724,
}

socket = CPPP.SCP3(atoms = ATOMS, threshold = 6, key = -2)

socket.connect(address, int(port))

messages = []
msg = input('>>> ')

while msg:
    messages.append(msg)
    msg = input('>>> ')

socket.send_string(*messages)

#print(socket.raw_recv(filter = lambda x: x.decode('utf-8')))