import CPPP, sys

name, address, port = sys.argv
print(f'Address: {address}\nPort: {port}')

socket = CPPP.CPPP()
socket.bind(address, int(port))
socket.listen()

try:
    print(socket.recv())
except KeyboardInterrupt:
    print("Stopping")

socket.close()