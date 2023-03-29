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

    def __init__(self, api_id, api_hash, phone_number):
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone_number = phone_number
        self.client = TelegramClient(phone_number, self.api_id, self.api_hash)
        t = threading.Thread(target = self.run)
        t.start()

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
        
    def run(self):
        self.receive_msg_asyncio = asyncio.new_event_loop()
        asyncio.set_event_loop(self.receive_msg_asyncio)
        with self.client:
            while(True):
                if self.readmyself==True:
                    self.client.loop.run_until_complete(self.readMySelf_process())
                self.client.loop.run_until_complete(self.receiveMessage())
                time.sleep(1)

    async def receiveMessage(self):
        async for message in self.client.iter_messages('me'):
            with open('AlreadyReadMessageID', 'r') as file:
                contents = file.read()
                if str(message.id) not in contents:
                    self.messageList.append(message)

    def readMySelf(self):
        self.readmyself = True
    async def readMySelf_process(self):
        me = self.client.get_me()
        print(me.stringify())
        self.readmyself = False

    async def sendmessage(self, target, message):
        await self.client.send_message(target, message)
