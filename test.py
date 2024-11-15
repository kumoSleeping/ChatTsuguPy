import tsugu_api
from tsugu import cmd_generator
import os
from PIL import Image
import io

from tsugu_api_core import settings

import asyncio
import base64
import io
from PIL import Image

tsugu_test_all = [
    # '查试炼',
    # '查试炼 -m',
    # '抽卡模拟',
    # '抽卡模拟 10',
    # '抽卡模拟 10 947',
    # '查卡面',
    # '查卡面 1399',
    # 'lsycx 1000',
    # 'lsycx 1000 177 jp',
    # '查卡池 947',
    # '查角色 ksm',
    # '查角色 吉他',
    # '查活动 绿 tsugu',
    # '查活动 177',
    # '查卡 1399',
    # '查卡 红 ars 5x',
    # '查玩家 1003282233',
    # '查玩家 40474621 jp',
    # '随机曲 lv27',
    # '随机曲 ag',
    # '查曲 1',
    # '查曲 ag lv27',
    # '查谱面 1',
    # '查谱面 128 special',
    # '查询分数表 cn',
    # 'ycxall 177',
    # 'ycxall 177 jp',
    # 'ycx 1000',
    # 'ycx 1000 177 jp',
    # '绑定玩家',
    # '绑定玩家 0',
    # '设置默认服务器 cn jp',
    # '主服务器 cn',
    # '关闭车牌转发',
    # '开启车牌转发',
    # '绑定玩家',
    # '玩家状态',
    '主账号',
    '主账号 2',
    '解除绑定 1',
    # 'ycm',
    
    # '上传车牌 12345',
]

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
                # img.show()
                print(f"[图像大小: {len(i) / 1024:.2f}KB]")

    test_count = 0
    user_id='114514'

    for i in tsugu_test_all:
        msg = await cmd_generator(message=i, user_id=user_id)
        await show_back_msg(msg)
    

# 启动测试
if __name__ == '__main__':
    asyncio.run(test_tsugu())