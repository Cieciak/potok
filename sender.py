import CPPP

test = CPPP.CPPP()


test.connect('127.0.0.1', 1024)


test.send('1')
print('T')
head, body = test.raw_recv()

print(body)