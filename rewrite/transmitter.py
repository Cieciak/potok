from main import CPPP

socket = CPPP()

socket.connect('0.0.0.0', 8001)
socket.send('12345678Hello')

print(socket.raw_recive())