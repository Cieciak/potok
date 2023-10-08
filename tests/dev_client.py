import CPPP

print('CPPP-Client example')

address = '127.0.0.1'
port    = 8000

client = CPPP.Client()



while True:
    user_input   = input('Enter body: ')
    method       = input('Method: ')
    localization = input('Localization: ')

    msg = CPPP.Message(
        head = {
            'method': method,
            'localization': localization,
        },
        body = bytearray(
            user_input,
            'utf-8'
        )
    )

    response = client.request(address, port, msg)

    print(response)