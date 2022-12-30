import CPPP, sys

name, address, port = sys.argv
print(f'Address: {address}\nPort: {port}')

socket = CPPP.CPPP()

socket.connect(address, int(port))

messages = []
msg = input('>>> ')

while msg:
    messages.append(msg)
    msg = input('>>> ')

socket.send_string(*messages)

#print(socket.raw_recv(filter = lambda x: x.decode('utf-8')))