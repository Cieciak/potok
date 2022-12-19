import CPPP

reciever = CPPP.CP3Server('127.0.0.1', 1024)
reciever.listen()

reciever.serve()
