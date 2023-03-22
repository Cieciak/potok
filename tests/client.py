# The simplest client
import CPPP

print('CPPP Client example')

address = input('Enter IP: ')
port = int(input('Enter port: '))

user_input = input('Enter body: ')

msg = CPPP.CPPPMessage(header = {'method': 'GET', 'localiztion': '/'}, body = bytearray(user_input, 'utf-8'))
response = CPPP.send_request(address, port, msg)
print(response.decode('utf-8'))
