import CPPP

socket = CPPP.CPPP()

socket.connect('127.0.0.1', 8001)

messages = []
msg = input('>>> ')

while msg:
    messages.append(msg)
    msg = input('>>> ')

socket.send_string(*messages)

print(socket.raw_recv(filter = lambda x: x.decode('utf-8')))