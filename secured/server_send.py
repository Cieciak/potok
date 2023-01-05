import CPPP, sys

name, address, port = sys.argv
print(f'Address: {address}\nPort: {port}')

ATOMS = {
    3: 55,
    4: 113,
}

socket = CPPP._SCP3(out_atoms = ATOMS, out_key = 1, inc_atoms = ATOMS, inc_threshold = 4)

socket.connect(address, int(port))

messages = []
msg = input('>>> ')

while msg:
    messages.append(msg)
    msg = input('>>> ')

socket.send_string(*messages)

print(socket.raw_recv(filter = lambda x: x.decode('utf-8')))