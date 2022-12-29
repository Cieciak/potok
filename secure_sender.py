import CPPP

ATOMS = {
    4: 842,
    5: 2643,
    6: 6724,
}

socket = CPPP.SCP3(atoms = ATOMS, threshold = 6, key = -2)

socket.connect('127.0.0.1', 8001)

messages = []
msg = input('>>> ')

while msg:
    messages.append(msg)
    msg = input('>>> ')

socket.send_string(*messages)

#print(socket.raw_recv(filter = lambda x: x.decode('utf-8')))