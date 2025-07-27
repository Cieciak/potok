import pypotok


msg = pypotok.Message.fromBytes(b'-BEGIN-\nPOTOK\n0.1\nGET\n-HEAD-\nOrigin: here\nTarget: there\n')

