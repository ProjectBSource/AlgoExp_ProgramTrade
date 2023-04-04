import time
import threading
import asyncio
import numpy as np
from telethon import TelegramClient


class TeleramMessageAPIConnection:
    api_id = None
    api_hash = None
    phone_number = None
    client = None
    messageList = []
    receive_msg_asyncio = None
    readmyself = False
    listTheClient = False
    sendmessage = False
    sendmessage_msg = None
    sendmessage_trg = None

    def __init__(self, api_id, api_hash, phone_number):
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone_number = phone_number
        self.client = TelegramClient(phone_number, self.api_id, self.api_hash)
        t = threading.Thread(target = self.run)
        t.start()

    ############################################################################################################
    def getMessage(self):
        if(len(self.messageList)>0):
            data = ""
            for message in self.messageList:
                data += str(message.id) + "\n"
            with open('AlreadyReadMessageID', 'a') as file:
                file.write(data)
            reversed_messageLst = self.messageList[::-1]
            self.messageList = []
            return reversed_messageLst
        else:
            return ""
    
    ############################################################################################################
    def run(self):
        self.receive_msg_asyncio = asyncio.new_event_loop()
        asyncio.set_event_loop(self.receive_msg_asyncio)
        with self.client:
            while(True):
                if self.readmyself==True:
                    self.client.loop.run_until_complete(self.readMySelf_process())
                    self.readmyself = False
                if self.listTheClient==True:
                    self.client.loop.run_until_complete(self.listTheClient_process())
                    self.listTheClient = False
                if self.sendmessage==True:
                    self.client.loop.run_until_complete(self.sendmessage_process())
                    self.sendmessage = False
                    self.sendmessage_trg = None
                    self.sendmessage_msg = None
                self.client.loop.run_until_complete(self.receiveMessage())
                time.sleep(1)

    ############################################################################################################
    async def receiveMessage(self):
        async for message in self.client.iter_messages('AlgoExp Signal'):
            with open('AlreadyReadMessageID', 'r') as file:
                contents = file.read()
                if str(message.id) not in contents:
                    self.messageList.append(message)

    ############################################################################################################
    def readMySelf(self):
        self.readmyself = True
    async def readMySelf_process(self):
        me = await self.client.get_me()
        print(me.stringify())


    ############################################################################################################
    def listTheClient(self):
        self.listTheClient = True
    async def listTheClient_process(self):
        async for dialog in self.client.iter_dialogs():
            print(dialog.name, 'has ID', dialog.id)

    ############################################################################################################        
    def sendMessage(self, target, message):
        if(target is not None and message is not None):
            self.sendmessage = True
            self.sendmessage_trg = target
            self.sendmessage_msg = message
    async def sendmessage_process(self):
        await self.client.send_message(self.sendmessage_trg, self.sendmessage_msg)
    ############################################################################################################
    