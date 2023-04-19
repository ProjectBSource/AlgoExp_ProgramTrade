from ConnectToIBAPIandPlaceOrder import ConnectToIBAPIandPlaceOrder
from TeleramMessageAPIConnection import TeleramMessageAPIConnection
import Common 
import time
import asyncio
import sys
from datetime import datetime

api_id = 21463150
api_hash = 'eb755521625b4a8b40f3d9c07a208624'
phonenumber = '85254944646'
contract_YYYYMM = "202304"
Common.initLogging(phonenumber)
ibTrade = ConnectToIBAPIandPlaceOrder()
tgAPIc = TeleramMessageAPIConnection(api_id, api_hash, phonenumber)
tgAPIc.readMySelf()
tgAPIc.listTheClient()
while(True):
    for message in tgAPIc.getMessage():
        if(message.id is not None and message.text is not None):
            Common.print_and_logging( "[" + str(message.id) + "]" + message.text )
            message_for_IB_trade = None
            if("**Algoexpsignal** [report]" in message.text):
                action = None
                price = (int((message.text[message.text.find(" at ")+4:message.text.find(" on ")]).replace(",","")))
                qty = 1
                if("Strategy1_call" in message.text):
                    action = "BUY"
                    with open("TempOnHold", "w") as file:
                        file.write("{},{},{} ".format("BUY",str(qty)))
                        file.close()
                if("Strategy1_Put" in message.text):
                    action = "SELL"
                    with open("TempOnHold", "w") as file:
                        file.write("{},{},{} ".format("SELL",str(qty)))
                        file.close()
                if("Close_call" in message.text):
                    action = "SELL"
                    with open("TempOnHold", "w") as file:
                        file.write("")
                        file.close()
                if("Close_Put" in message.text):
                    action = "BUY"
                    with open("TempOnHold", "w") as file:
                        file.write("")
                        file.close()
    print(str(datetime.now()) + "------------- heartbeat from Main")
    
    with open('AlreadyReadMessageID', 'r') as file:
        contents = file.read()
        if len(contents) > 0:
            print('initial finished')
            sys.exit(0)
            break
    time.sleep(0.1)
