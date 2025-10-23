import pypotok

print('\n###########\nTest 1')

body = pypotok.BodySegment()
print(body)

body.load_bytes(b'hello, you use the -BODY- tag.')
print(body)

msg = body.read_bytes()
print(msg)

print('\n###########\nTest 2')

body = pypotok.BodySegment.from_bytes(b'hello, you use the -BODY- tag.')
print(body)

msg = body.read_bytes()
print(msg)


print('\n###########\nTest 3')
head = pypotok.HeaderSegment()

head.add_tag('path', '/home/here')
head.add_tag('count', '10')
print(head)

head.remove_tag('count')
print(head)

print('\n###########\nTest 4')
msg = pypotok.Message()

msg.begin = pypotok.BeginSegment('POTOK', '0.1', 'SET')
msg.head  = pypotok.HeaderSegment()
msg.body  = pypotok.BodySegment.from_bytes(b'You use -BODY- segment to stansfer data')

msg.head.add_tag('path', '/home/less')
msg.head.add_tag('count', '23')

data = msg.to_bytes()

print(data.decode('utf-8'))

print('\n###########\nTest 5')
msg = pypotok.Message.from_bytes(b'-INIT-\nPOTOK\n0.1\nSET\n-HEAD-\njath: /home/less\ncount: 23\n-BODY-\nYou use \\-BODY\\- segment to stansfer data')


data = msg.to_bytes()

print(data)

print('\n###########\nTest 5')
msg = pypotok.Message.from_bytes(b'-INIT-\nPOTOK\n0.1\nSET\n-HEAD-\njath: /home/less\ncount: 23\n-BODY-\nYou use \\-BODY\\-')


data = msg.to_bytes()

print(data)