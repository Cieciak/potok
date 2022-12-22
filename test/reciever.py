import CPPP

socket = CPPP.CPPP()

socket.bind('127.0.0.1', 1024)
socket.listen()

print(socket.recv())

socket.close()