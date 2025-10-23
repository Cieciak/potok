import pypotok

org = b'-BEGIN-\nPOTOK\n0.1\nGET\n-HEAD-\nOrigin: here\nTarget: there\n-BODY-\nhello world'

msg = pypotok.Message.fromBytes(org)

rcv = msg.toBytes()

print(org)
print(rcv)