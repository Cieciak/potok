import CPPP, sys

name, address, port = sys.argv
print(f'Address: {address}\nPort: {port}')


ATOMS = {
    1: 7,
    2: 64,
    5: 3907,
}
socket = CPPP._SCP3(out_key = 2, out_atoms = ATOMS, inc_atoms = ATOMS, inc_threshold = 6)
#socket = CPPP.SCP3(atoms = ATOMS, threshold = 6, key = 2)

socket.connect(address, int(port))

messages = []
msg = input('>>> ')

while msg:
    messages.append(msg)
    msg = input('>>> ')

socket.send_string(*messages)

#print(socket.raw_recv(filter = lambda x: x.decode('utf-8')))