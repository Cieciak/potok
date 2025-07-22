import pypotok


begin = pypotok.BeginSegment('POTOK', '0.1', 'GET')
print(begin)
head = pypotok.HeaderSegment({'Origin': 'here', 'Target': 'example', 'Location': 'home'})
print(head)
body = pypotok.BodySegment(b'hello there')
print(body)