import pypotok

addr = input('[ADDR] <<< ')
port = int(input('[PORT] <<< '))

while True:

    method = input('[METHOD]  <<< ')
    data =   input('[PAYLOAD] <<< ')

    msg = pypotok.Message(
        pypotok.BeginSegment(method=method),
        pypotok.HeaderSegment({'dev': 'True'}),
        pypotok.BodySegment.from_bytes(bytes(data, 'utf-8'))
    )
    
    rsp = pypotok.request(addr, port, msg)
    print(rsp.body)