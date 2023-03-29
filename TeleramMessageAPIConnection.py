import time
import threading
import asyncio
import numpy as np
from telethon import TelegramClient


class TeleramMessageAPIConnection:
    api_id = None
    api_hash = None
    client = None
    messageList = []

    def __init__(self, api_id, api_hash, phone_number):
        self.api_id = api_id
        self.api_hash = api_hash
        self.client = TelegramClient(phone_number, self.api_id, self.api_hash)
        t = threading.Thread(target = self.run)
        t.start()

    def getMessage(self):
        if(len(self.messageList)>0):
            data = ""
            for message in self.messageList:
                data += str(message[0]) + "\n"
            with open('AlreadyReadMessageID', 'a') as file:
                file.write(data)
            reversed_messageLst = self.messageList[::-1]
            self.messageList = []
            return reversed_messageLst
        else:
            return ""
        
    def run(self):
        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(new_loop)
        with self.client:
            while(True):
                self.client.loop.run_until_complete(self.main())
                time.sleep(1)

    async def main(self):
        async for message in self.client.iter_messages('me'):
            with open('AlreadyReadMessageID', 'r') as file:
                contents = file.read()
                if str(message.id) not in contents:
                    self.messageList.append([str(message.id), message.text])
