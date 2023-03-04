# The simplest echo server
import CPPP, time

server = CPPP.CPPPServer('0.0.0.0', 8000)

@server
def handler(msg: CPPP.CPPPMessage):
    recv = time.time()
    time.sleep(2)
    resp = time.time()
    msg = CPPP.CPPPMessage(header = {'method': 'RETURN'}, body = f'{recv}, {resp}')

    return msg


try: server.serve()
except KeyboardInterrupt: print('Server stopped!')