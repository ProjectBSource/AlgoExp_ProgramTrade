from ConnectToIBAPIandPlaceOrder import ConnectToIBAPIandPlaceOrder
from TeleramMessageAPIConnection import TeleramMessageAPIConnection
import Common 
import time
import asyncio
import sys
from datetime import datetime, time
from time import sleep


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
    still_onHold = False
    with open('TempOnHold', 'r') as file:
        contents = file.read()
        if(len(contents)>0):
            still_onHold = True
        file.close()
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
                        file.write("{},{}".format("Strategy1_call",str(qty)))
                        file.close()
                if("Strategy1_Put" in message.text):
                    action = "SELL"
                    with open("TempOnHold", "w") as file:
                        file.write("{},{}".format("Strategy1_Put",str(qty)))
                        file.close()
                if("Close_call" in message.text):
                    if(still_onHold==True):
                        continue
                    action = "SELL"
                    with open("TempOnHold", "w") as file:
                        file.write("")
                        file.close()
                if("Close_Put" in message.text):
                    if(still_onHold==True):
                        continue
                    action = "BUY"
                    with open("TempOnHold", "w") as file:
                        file.write("")
                        file.close()
                message_for_IB_trade = "{} {} MHI@{} ".format(action, str(qty), str(price))
                ibTrade.app.AlgoExpSignalStrategy(contract_YYYYMM, qty, price, action, "LimitOrder")
                ibTrade.app.AlgoExpSignalStrategy(contract_YYYYMM, qty, price, action, "StopLimit")
                ibTrade.app.AlgoExpSignalStrategy(contract_YYYYMM, qty, price, action, "MarketToLimit")
                ibTrade.app.AlgoExpSignalStrategy(contract_YYYYMM, qty, price, action, "MarketOrder")
                
            tgAPIc.sendMessage(phonenumber, message_for_IB_trade)

    ###################################################################################
    #force close all on 02:50 am
    ###################################################################################
    if(datetime.now().time() > time(2,50) and datetime.now().time() < time(2,51)):
        action = None
        price = None
        qty = None
        if(still_onHold==True):
            with open('TempOnHold', 'r') as file:
                contents = file.read()
                contents_array = contents.split(',')
                if("Strategy1_call" == contents_array[0]):
                    action = "SELL"
                    qty = int(contents_array[1])
                if("Strategy1_Put" == contents_array[0]):
                    action = "BUY"
                    qty = int(contents_array[1])
                file.close()
            message_for_IB_trade = "{} {} MHI@{} ".format(action, str(qty), "Market price")
            ibTrade.app.AlgoExpSignalStrategy(contract_YYYYMM, qty, price, action, "MarketToLimit")
            ibTrade.app.AlgoExpSignalStrategy(contract_YYYYMM, qty, price, action, "MarketOrder")
            with open("TempOnHold", "w") as file:
                file.write("")
                file.close()
    ###################################################################################
    ###################################################################################

    print(str(datetime.now()) + "------------- heartbeat from Main")
    sleep(0.1)
    
