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
tgAPIc = TeleramMessageAPIConnection(api_id, api_hash, phonenumber)
tgAPIc.readMySelf()
tgAPIc.listTheClient()
sys.exit(0)
