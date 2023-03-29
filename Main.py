from TeleramMessageAPIConnection import TeleramMessageAPIConnection
import Common 
import time

api_id = 123345
api_hash = 'aaaabbbbcccceee'
phonenumber = '85255559999'
Common.initLogging(phonenumber)
tgAPIc = TeleramMessageAPIConnection(api_id, api_hash, phonenumber)
while(True):
    for message in tgAPIc.getMessage():
        if(message is None):
            break
        if(len(message)>0):
            Common.print_and_logging( message )
    print("-------------------------------------------------")
    time.sleep(1)