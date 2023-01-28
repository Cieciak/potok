import CPPP, time

msg = CPPP.CPPPMessage(header = {'method': 'GET', 'localiztion': '/'}, body = b'Hello World!')
response = CPPP.send_request('127.0.0.1', 8000, msg)
print(response.decode('utf-8'))

response = CPPP.send_request('127.0.0.1', 8000, msg)
print(response.decode('utf-8'))