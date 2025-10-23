import pypotok

addr = '0.0.0.0'
port = 8100


class DNS_Server(pypotok.Server):

    def __init__(self, address, port):
        super().__init__(address, port)

        self.entries: dict[str, str] = {}

dns_server = DNS_Server(addr, port)

@dns_server.method('DNSGET')
def get_entry(msg: pypotok.Message, srv: DNS_Server):
    
    query = msg.body.raw.decode('utf-8')

    entry = srv.entries.get(query, 'NONE')

    rsp = pypotok.Message.response(bytes(entry, 'utf-8'))

    return rsp

@dns_server.method('DNSPUT')
def put_entry(msg: pypotok.Message, srv: DNS_Server):

    name, addr = msg.body.raw.decode('utf-8').split(':', 1)

    srv.entries[name] = addr

    return pypotok.Message.response(bytes(srv.entries[name], 'utf-8'))

try: dns_server.serve()
except KeyboardInterrupt: print('Server stopped!')