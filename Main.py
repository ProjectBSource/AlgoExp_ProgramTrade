from TeleramMessageAPIConnection import TeleramMessageAPIConnection
import Common 
import time
import asyncio
from datetime import datetime

api_id = 21463150
api_hash = 'eb755521625b4a8b40f3d9c07a208624'
phonenumber = '85254944646'
Common.initLogging(phonenumber)
tgAPIc = TeleramMessageAPIConnection(api_id, api_hash, phonenumber)
tgAPIc.readMySelf()
#tgAPIc.listTheClient()
while(True):
    for message in tgAPIc.getMessage():
        if(message.id is not None and message.text is not None):
            Common.print_and_logging( "[" + str(message.id) + "]" + message.text )
            tgAPIc.sendMessage(phonenumber, message.text)
    print(str(datetime.now()) + "-------------------------------------------------")
    time.sleep(1)