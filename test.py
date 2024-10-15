import tsugu_api
from tsugu import cmd_generator
import os
from PIL import Image
import io

from tsugu_api_core import settings
# settings.backend_url = 'http://127.0.0.1:8010'
# settings.backend_url = 'http://1.tsugubot.com:58080'
# settings.userdata_backend_url = 'http://1.tsugubot.com:58081'

import asyncio
import base64
import io
from PIL import Image

async def test_tsugu():
    async def show_back_msg(data):
        if not data:
            print("没有返回数据")
            return
        for item in data:
            if item['type'] == 'string':
                print(f"[文字信息] {item['string']}")
            elif item['type'] == 'base64':
                print("[图片信息]")
                i = base64.b64decode(item['string'])
                img = Image.open(io.BytesIO(i))
                img.show()
                print(f"[图像大小: {len(i) / 1024:.2f}KB]")

    test_count = 0
    user_id='1528593481'
    
    msg = await cmd_generator(message='查试炼 -h', user_id=user_id)
    await show_back_msg(msg)
    
    # while True:
    #     test_count += 1
    #     continue_test = input(f"{user_id}:（{test_count}）>>")
    #     msg1 = await cmd_generator(message=continue_test, user_id=user_id)
    #     await show_back_msg(msg1)
        

# 启动测试
if __name__ == '__main__':
    asyncio.run(test_tsugu())
