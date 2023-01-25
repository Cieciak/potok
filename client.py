import CPPP, time

mesage = 'head{method:GET,location:"/",}body["Hello","World"]'

msg = bytearray(mesage, 'UTF-8')

CPPP.send_request('127.0.0.1', 8000, msg)
CPPP.send_request('127.0.0.1', 8000, msg)