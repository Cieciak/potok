import CPPP

server = CPPP.CP3Server('127.0.0.1', 8001)

server.listen()
try:
    server.serve()
except KeyboardInterrupt:
    server.close()
    print('Server closed')

