import requests
import re
import json
from pathlib import Path

# import os
# import time
# import base64, io
# from PIL import Image

BACKEND_URL = 'http://tsugubot.com:8080'  # 后端地址
default_use_easy_bg = True  # 是否使用简易背景
default_servers = ["3", "0"]   # 默认服务器顺序
BindPlayer_url = ''  # 请填写玩家绑定数据库API
self_id = 'tsugu'  # bot称呼，后面会用到 swc off 称呼 来关闭bot
help_word = 'help'  # help 触发词（不能有空格）

folder_path = Path('tsugu_config')  # 配置文件存储位置，可以不管
bandoriStationToken = 'ZtV4EX2K9Onb'
source = 'Tsugu'
ban_group_file = folder_path / 'ban_group.json'
administrator_file = folder_path / 'administrator.json'

if not folder_path.exists():
    folder_path.mkdir()


def load_json_file(file, default_data):
    if not file.exists():
        with open(file, 'w', encoding='utf-8') as f:
            json.dump(default_data, f)
            return default_data
    else:
        with open(file, 'r', encoding='utf-8') as f:
            return json.load(f)


ban_group_data = load_json_file(ban_group_file, [])
administrator_data = load_json_file(administrator_file, ["ALL"])
# print(ban_group_data, administrator_data)

# cmd_dict 可以用来设置别名
cmd_dict = {
    # （不支持换服务器优先级）
    help_word: "Help",
    "swc": "Swc",
    "查曲": "/searchSong",
    "查活动": "/searchEvent",
    "查谱面": "/songChart",
    "查铺面": "/songChart",  # 别名
    "查卡面": "/getCardIllustration",
    "查角色": "/searchCharacter",
    "查卡池": "/searchGacha",
    "查卡": "/searchCard",  # 查卡一定要放在 查卡面 查卡池 后面，原因自己想
    "查玩家": "/searchPlayer",
    "玩家状态": "PlayerStatus",
    "日服玩家状态": "JPlayerStatus",
    "绑定玩家": "BindPlayer",  # （使用自建数据库api，只支持日服，国服）
    # （支持自动车牌转发）
    "查询分数表": "/songMeta",
    "查分数表": "/songMeta",  # 别名 # 别名放在后面
    "ycm": "/roomList",  # （只支持官方车站的车）
    "ycxall": "/ycxAll",
    "ycx": "/ycx",   # ycx一定要放在 ycxall 后面，原因自己想
    "lsycx": "/lsycx",
    "抽卡模拟": "/gachaSimulate",

    # ⬇还没做，暂时不打算在本插件支持
    # '开启抽卡模拟': 'gachaSimulate_ON',
    # '关闭抽卡模拟': 'gachaSimulate_OFF',
    # '开启个人车牌转发': 'BD_STATION_ON_PERSONAL',
    # '关闭个人车牌转发': 'BD_STATION_OFF_PERSONAL',
    # '开启本群车牌转发': 'BD_STATION_ON_GROUP',
    # '关闭本群车牌转发': 'BD_STATION_OFF_GROUP',
}

# 此列表键与 cmd_dict 保持一致
cmd_help_dict = {
    "swc": f"swc off {self_id} ·关闭本群Tsugu\nswc on {self_id} ·开启本群Tsugu",
    "查曲": "查曲 信息 ·列表查曲\n查曲 ID ·查寻单曲信息",
    "查活动": "查活动 信息 ·列表查活动\n查活动 ID ·查寻活动信息",
    "查谱面": "查谱面 ID 难度 ·输出谱面预览",
    "查铺面": "查谱面 ID 难度 ·输出谱面预览",  # 别名
    "查卡面": "查卡面 ID ·查询卡片插画",
    "查角色": "查角色 ID/关键词 ·查询角色的信息",
    "查卡池": "查卡池 ID 查询卡池信息",
    "查卡": "查卡 信息 ·列表查卡面\n查卡 ID ·查询卡面信息",  # 查卡一定要放在 查卡面 查卡池 后面，原因自己想
    "查玩家": "查玩家 UID 服务器 ·查询对应玩家信息",
    "玩家状态": "玩家状态 ·查询自己的玩家状态\n玩家状态 jp/日服 ·查询自己的日服玩家状态",
    "日服玩家状态": "日服玩家状态 ·查询自己的日服玩家状态",
    "绑定玩家": "发送 绑定玩家 uid ·绑定国服\n发送 绑定玩家 jp uid ·绑定日服",  # （使用自建数据库api，只支持日服，国服）
    # （支持自动车牌转发）
    "查询分数表": "查询分数表 服务器 ·查询歌曲分数表，服务器非必填",
    "查分数表": "查询分数表 服务器 ·查询歌曲分数表，服务器非必填",  # 别名 # 别名放在后面
    "ycm": "ycm ·获取所有车牌车牌",  # （只支持官方车站的车）
    "ycxall": "ycxAll 活动ID ·查询所有档位的预测线，只支持国服，活动ID非必填",
    "ycx": "ycx 档位 活动ID ·查询预测线，只支持国服，活动ID非必填",   # ycx一定要放在 ycxall 后面，原因自己想
    "lsycx": "lsycx 活动ID ·返回档线、预测线、近4期同类活动的档线，只支持国服，活动ID非必填",
    "抽卡模拟": "抽卡模拟 次数 卡池ID ·抽卡模拟，次数、卡池ID非必填",

}
non_arg_cmd = [
    "/songMeta",
    "PlayerStatus",
    "JPlayerStatus",
    "/roomList",
    "/gachaSimulate",
    "BindPlayer",
    "Help",
]

language_mapping = {"jp": 0, "en": 1, "tw": 2, "cn": 3, "kr": 4}

config = {
    "car": ["车", "w", "W", "国", "日", "火", "q", "开", "Q", "万", "缺", "来", "差", "奇迹", "冲", "途", "分", "禁"],
    "fake": ["114514", "假车", "测试", "野兽", "恶臭", "1919", "下北泽", "粪", "糞", "臭", "雀魂", "麻将", "打牌", "maj", "麻", "[", "]", "断幺", "11451", "xiabeize", "qq.com", "@", "q0", "q5", "q6", "q7", "q8", "q9", "q10", "腾讯会议", "master", "疯狂星期四", "离开了我们", "日元", "av", "bv"]
}


def get_data(user_id: str, server: str):
    url = f"{BindPlayer_url}/api/data?mode=get&user_id={user_id}&server={server}"
    try:
        with requests.Session() as session:
            response = session.get(url)
            response.raise_for_status()
            return response.text
    except requests.exceptions.RequestException as e:
        # 处理请求异常
        print(f"Error during HTTP request: {e}")
        return None


def save_data(user_id: str, uid: str, server: str):
    url = f"{BindPlayer_url}/api/data?mode=save&user_id={user_id}&uid={uid}&server={server}"
    try:
        with requests.Session() as session:
            response = session.get(url)
            response.raise_for_status()
            return response.text
    except requests.exceptions.RequestException as e:
        # 处理请求异常
        print(f"Error during HTTP request: {e}")
        return None


def process_message(user_id: str, text: str):
    server = "jp" if "日服" in text or "jp" in text else "cn"
    uid = text.replace("绑定玩家", "").replace("日服", "").replace("jp", "").strip()
    ret_sav = save_data(user_id, uid, server)
    return [{"type": "string", "string": ret_sav}]


def remove_none_value(d: dict):
    return {k: v for k, v in d.items() if v}


def try_int(x):
    try:
        return int(x)
    except:
        return 0


def send_post_request(url, data):
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()  # 如果发生HTTP错误，将引发异常
        return response.json()
    except requests.exceptions.RequestException as e:
        return [{"type": "string", "string": f"后端服务器连接出错, {e}, {data}"}]
    except Exception as e:
        return [{"type": "string", "string": f"内部错误: {e}"}]


def get_data_from_backend(backend_url, api, data):
    try:
        result = send_post_request(f"{backend_url}{api}", data)
        return result
    except Exception as e:
        return [{"type": "string", "string": f"后端服务器连接出错, {e}, {data}"}]


# 调用示例
def tsugu_main(message: str, user_id: str, group_id: str):
    """
    接口函数，输入 消息 ID ，触发成员ID，群ID
    """

    # 检查是否是车牌 # 折叠此函数获得更好的浏览体验
    def check_message_isCar():
        """接受发来的原是消息
        检查是否是 合法 车牌
        返回布尔值"""
        isCar = False

        # 检查config['car']中的关键字
        for keyword in config["car"]:
            if keyword in message:
                isCar = True
                break

        # 检查config['fake']中的关键字
        for keyword in config["fake"]:
            if keyword in message:
                isCar = False
                break
        pattern = r"^\d{5}(\D|$)|^\d{6}(\D|$)"
        if re.match(pattern, message):
            pass
        else:
            isCar = False

        return isCar

    # 1.车牌方法 # 折叠此函数获得更好的浏览体验
    def car_way():
        """
        直接根据收到的原始信息切出车牌，将内容上传车站
        """
        try:
            car_id = message[:6]

            if not car_id.isdigit() and car_id[:5].isdigit():
                car_id = car_id[:5]

            # 构建URL
            url = f"https://api.bandoristation.com/index.php?function=submit_room_number&number={car_id}&user_id={user_id}&raw_message={message}&source={source}&token={bandoriStationToken}"

            # 发送请求
            response = requests.get(url)

            if response.status_code != 200:
                print(f"提交车牌失败，HTTP响应码: {response.status_code}")
        except Exception as e:
            print(f"发生异常: {e}")

    # 2.非原生方法 # 折叠此函数获得更好的浏览体验
    def non_native_way(text: str):
        if api == "Help":
            if text.strip() == '0':
                # unique_values = set(cmd_dict.values())  # 获取所有不重复的值
                unique_keys = {}  # 用于存储不同键对应的值

                for key, value in cmd_dict.items():
                    if value not in unique_keys:
                        unique_keys[value] = key

                result = '\n>> '.join(unique_keys.values())  # 用换行连接不同键对应的值
                result = f"当前可用的Tsugu指令有：\n>> {result}\n发送 {message}+指令 查看帮助"
                return [
                    {
                        "type": "string",
                        "string": result,
                    }
                ]
            if text in cmd_help_dict:
                return [
                    {
                        "type": "string",
                        "string": '>> ' + cmd_help_dict[text],
                    }
                ]
            else:
                return None

        elif api == "Swc":

            # 验权
            if 'ALL' not in administrator_data:
                if user_id in administrator_data:
                    pass
                else:
                    return [
                    {
                        "type": "string",
                        "string": '权限不足',
                    }
                ]

            # 默认值
            if text.strip().startswith("off") and self_id in message:
                if group_id not in ban_group_data:
                    ban_group_data.append(group_id)
                else:
                    return None
                with open(ban_group_file, 'w', encoding='utf-8') as f:
                    json.dump(ban_group_data, f)
                return [
                {
                    "type": "string",
                    "string": '呜呜，zoule',
                }
            ]
            '''
            '''
            if text.strip().startswith("on") and self_id in message:
                try:
                    ban_group_data.remove(group_id)
                except:
                    return None
                with open(ban_group_file, 'w', encoding='utf-8') as f:
                    json.dump(ban_group_data, f)
                return [
                    {
                        "type": "string",
                        "string": '喜多喜多～',
                    }
                ]

        elif api == "PlayerStatus":
            server = "jp" if "日服" in text or "jp" in text else "cn"

            uid = get_data(user_id, server)
            if uid == "找不到用户":
                return [
                    {
                        "type": "string",
                        "string": "发送 绑定玩家 <uid> ·绑定国服\n发送 绑定玩家 jp <uid> ·绑定日服",
                    }
                ]
            server = language_mapping.get(server, 3)
            data = {
                "server": server,
                "useEasyBG": True,
                "playerId": int(uid),
            }

            return get_data_from_backend(
                backend_url=BACKEND_URL, api="/searchPlayer", data=data
            )
        elif api == "JPlayerStatus":
            server = "jp"
            uid = get_data(user_id, server)
            if uid == "找不到用户":
                return [
                    {
                        "type": "string",
                        "string": "发送 绑定玩家 jp <uid> ·绑定日服",
                    }
                ]
            server = language_mapping.get(server, 3)
            data = {
                "server": server,
                "useEasyBG": True,
                "playerId": int(uid),
            }

            return get_data_from_backend(
                backend_url=BACKEND_URL, api="/searchPlayer", data=data
            )
        elif api == "BindPlayer":
            if not text or text.strip() == '0':
                # 因为前面写了help，所以下面的语句不会被触发了（）
                return [{'type': 'string', 'string': '发送 绑定玩家 <uid> ·绑定国服\n发送 绑定玩家 jp <uid> ·绑定日服'}]
            if text.strip() == "绑定玩家":
                return [
                    {
                        "type": "string",
                        "string": "发送 绑定玩家 <uid> ·绑定国服\n发送 绑定玩家 jp <uid> ·绑定日服",
                    }
                ]

            return process_message(user_id, text)

        return None

    # 3.原生方法（url获取数据） # 折叠此函数获得更好的浏览体验
    def native_way(text: str, default_servers=default_servers):
        if api == "/searchEvent":
            data = {
                "default_servers": default_servers,
                "text": text,
                "useEasyBG": default_use_easy_bg,
            }
        elif api == "/searchSong":
            data = {
                "default_servers": default_servers,
                "text": text,
                "useEasyBG": default_use_easy_bg,
            }
        elif api == "/searchCard":
            data = {
                "default_servers": default_servers,
                "text": text,
                "useEasyBG": default_use_easy_bg,
            }
        elif api == "/songMeta":
            if not text:
                data = {
                    "default_servers": default_servers,
                    "useEasyBG": default_use_easy_bg,
                    "server": default_servers[0],
                }
            else:
                data = {
                    "default_servers": default_servers,
                    "useEasyBG": default_use_easy_bg,
                    "server": language_mapping.get(text, 3),
                }
        elif api == "/getCardIllustration":
            data = {
                "cardId": text,
            }
        elif api == "/searchGacha":
            data = {
                "default_servers": default_servers,
                "useEasyBG": default_use_easy_bg,
                "gachaId": text,
            }
        elif api == "/searchPlayer":
            data = {
                "server": language_mapping["jp" if "jp" in text else "cn"],
                "useEasyBG": True,
                "playerId": try_int(text.replace("cn", "").replace("jp", "").strip()),
            }
        elif api == "/lsycx":
            data = remove_none_value(
                {
                    "server": 3,
                    "tier": int(text.split()[0]),
                    "eventId": int(text.split()[1]) if len(text.split()) >= 2 else None,
                }
            )
        elif api == "/ycxAll":
            data = {
                "server": 3,
                "eventId": text,
            }
        elif api == "/ycx":
            data = remove_none_value(
                {
                    "server": 3,
                    "tier": int(text.split()[0]),
                    "eventId": int(text.split()[1]) if len(text.split()) >= 2 else None,
                }
            )
        elif api == "/songChart":
            if not text.split()[0].isdigit():
                return [{"type": "string", "string": "不和规范的歌曲ID"}]
            data = {
                "default_servers": default_servers,
                "songId": int(text.split()[0]),
                "difficultyText": text.split()[1] if len(text.split()) >= 2 else "ex",
            }
        elif api == "/gachaSimulate":
            data = remove_none_value(
                {
                    "server_mode": 3,
                    "status": True,
                    "times": int(text.split()[0]) if text and int(text.split()[0]) < 10000 else 10,
                    "gachaId": int(text.split()[1]) if len(text.split()) >= 2 else None,
                }
            ) if text else {"server_mode": 3, "status": True, "times": 10}

        elif api == "/roomList":
            try:
                response = requests.get(
                    "https://api.bandoristation.com/?function=query_room_number"
                )
                response.raise_for_status()
                response_json = response.json()
                response_list = response_json.get("response", [])

                room_list = [
                    {
                        "number": int(item.get("number", 0)),
                        "rawMessage": item.get("raw_message", ""),
                        "source": item.get("source_info", {}).get("name", ""),
                        "userId": str(item.get("user_info", {}).get("user_id", "")),
                        # "time": "{:.1f}".format(int(time.time())),
                        # "time": item['time'] - 3600,
                        "time": item['time'],
                        "avanter": item.get("user_info", {}).get("avatar", None),
                        "userName": item.get("user_info", {}).get("username", "Bob"),
                    }
                    for item in response_list
                ]
                if room_list == []:
                    return [{"type": "string", "string": "myc"}]

                data = {"roomList": room_list}

            except Exception as e:
                return [{"type": "string", "string": f"错误：{e}"}]
        else:
            data = None

        # print('data:', data)

        return get_data_from_backend(backend_url=BACKEND_URL, api=api, data=data)
    # 先检查本群是否被ban
    if group_id in ban_group_data:
        if message.startswith('swc'):
            pass
        else:
            return None

    # 先检查是否为车牌，如果是直接用 1.车牌方法
    result_car = check_message_isCar()
    if result_car:
        return car_way()

    command_name = None
    # 检查用户输入是否以一个指令开头
    for key in cmd_dict.keys():
        if message.startswith(key):
            api = cmd_dict[key]
            # api 是 /songMeta 这样的url组成部分 或 自定义字符串（区别在于有没有'/'）
            if api == "/roomList" and message != key:
                # 防止误触发，如“ycm是不是有bug”
                return None
            command_name = key
            # command_name 是玩家发送的消息的 指令名
            break
    else:
        # 如果不是直接结束此次会话
        return None

    # 拆出参数，没有则 None 或 '' （不清楚）
    text = message.replace(command_name, "").strip()

    # 容许一些无参数指令
    if text == "" and api not in non_arg_cmd:  # 不需要参数的指令
        return [{"type": "string", "string": "请添加参数"}]

    if len(text.split()) < 1:
        # 占位
        text += " 0"

    # 2.非原生方法
    if "/" not in api:
        return non_native_way(text)

    # 3.原生方法（网络获取）
    return native_way(text)

'''
=======================单条测试=======================
'''
# result = tsugu_main("123231 q1", "1528593481")
# result = tsugu_main("helpg 查卡", "1528593481", '1')
#
# if not result:
#     print("[无指令]")
# else:
#     for item in result:
#         if item["type"] == "string":
#             e_message = item["string"]
#             print(f"解释文字:\n{e_message}")
#         elif item["type"] == "base64":
#             # 处理Base64编码的图像数据
#             base64_data = item["string"]
#             # 解码Base64数据
#             image_data = base64.b64decode(base64_data)
#             # 将二进制数据转换为 PIL 图像对象
#             image = Image.open(io.BytesIO(image_data))
#             # 保存图像文件
#             image.show()
#         else:
#             print(item)
'''
=======================循环测试=======================
'''
# user_id = "1528593481"
# group_id = "666808414"
# while True:
#     user_input = input(f"USER({user_id}): ")
#     result = tsugu_main(user_input, user_id, group_id)
#     if not result:
#         print("[无指令]")
#     else:
#         for item in result:
#             if item["type"] == "string":
#                 # 处理字符串类型的结果，可能是错误消息
#                 error_message = item["string"]
#                 print("解释文字:", error_message)
#             elif item["type"] == "base64":
#                 # 处理Base64编码的图像数据
#                 base64_data = item["string"]
#                 # 解码Base64数据
#                 image_data = base64.b64decode(base64_data)
#                 # 将二进制数据转换为 PIL 图像对象
#                 image = Image.open(io.BytesIO(image_data))
#                 # 保存图像文件
#                 image.show()
#             else:
#                 print(item)
#
#
#
