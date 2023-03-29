from TeleramMessageAPIConnection import TeleramMessageAPIConnection
import Common 
import time
import asyncio

api_id = 21463150
api_hash = 'eb755521625b4a8b40f3d9c07a208624'
phonenumber = '85254944646'
Common.initLogging(phonenumber)
tgAPIc = TeleramMessageAPIConnection(api_id, api_hash, phonenumber)
tgAPIc.readMySelf()
while(True):
    for message in tgAPIc.getMessage():
        Common.print_and_logging( "[" + str(message.id) + "]" + message.text )
        #asyncio.run(tgAPIc.sendmessage('85264302639', message.text))
    print("-------------------------------------------------")
    time.sleep(1)