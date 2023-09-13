import asyncio
import json
import websockets
import aiohttp
import base64
import re
import threading

from c_p_3 import process_message  # 引入处理消息的函数
from c_p_3 import Msg  # 引入send_message函数，目的是IP和TOKEN

import os
current_dir = os.path.dirname(__file__)
# 切换到当前文件所在的目录
os.chdir(current_dir)


IP = Msg.IP
PORT = Msg.PORT
TOKEN = Msg.TOKEN


class CatBot:
    def __init__(self, token, ws_url):
        self.token = token
        self.ws_url = ws_url
        self.session = aiohttp.ClientSession()

    # 创建连接到猫猫
    async def connect(self):
        self.websocket = await websockets.connect(self.ws_url)
        await self.send_connect_packet()

    # 被上面的connect调用，发送连接信息
    async def send_connect_packet(self):
        connect_packet = {
            "type": "meta::connect",
            "payload": {
                "token": self.token
            }
        }
        await self.websocket.send(json.dumps(connect_packet))
        print("\033[93m 猫猫，启动！ \033[0m")

    # 接受来自猫猫的消息
    async def receive_message(self):
        while True:
            try:
                message = await self.websocket.recv()
                data = json.loads(message)
                await self.handle_message(data)
            except websockets.ConnectionClosed:
                print("猫猫 closed.")
                break

    async def handle_message(self, data):
        # 这里开了一个线程，用于处理消息，process_message在隔壁c_p.py里面，相当于利用外部文件劫持了本线程的函数，本身不影响ws线程整体运行
        thread = threading.Thread(target=process_message, args=(data,))
        thread.start()

    async def run(self):
        try:
            await self.connect()
            await self.receive_message()
        finally:
            await self.session.close()


if __name__ == "__main__":
    WS_URL = f"ws://{IP}:{PORT}/"  # 请将WebSocket服务器的URL替换为实际的地址

    cat_bot = CatBot(TOKEN, WS_URL)
    asyncio.get_event_loop().run_until_complete(cat_bot.run())

