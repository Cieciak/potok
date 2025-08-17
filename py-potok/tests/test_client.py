import pypotok

addr = 'localhost'
port = 8001

while True:

    data = input('>>>')

    msg = pypotok.Message(
        pypotok.BeginSegment(method='GET'),
        pypotok.HeaderSegment({'dev': 'True'}),
        pypotok.BodySegment(bytes(data, 'utf-8'))
    )
    
    rsp = pypotok.request('localhost', 8000, msg)
    print(rsp)