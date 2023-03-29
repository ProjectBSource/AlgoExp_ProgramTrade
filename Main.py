from TeleramMessageAPIConnection import TeleramMessageAPIConnection
import Common 
import time

api_id = 21463150
api_hash = 'eb755521625b4a8b40f3d9c07a208624'
phonenumber = '85254944646'
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