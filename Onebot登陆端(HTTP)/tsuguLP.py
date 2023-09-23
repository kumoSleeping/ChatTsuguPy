import requests
import re
import json
from typing import Optional, Union, List, Dict, Any
from pydantic import BaseModel
from pathlib import Path

# 下面导入的包用于本文件结尾被注释掉的测试部分
# from PIL import Image
# import io, base64

# 这个 我真不想用（哭）
# class JsonDataStorage:
#     """基于 Pydantic 的 JSON 数据读写方法"""
#
#     def __init__(
#         self,
#         model: Union[BaseModel, List[BaseModel]] = None,
#         file_path: Union[str, Path] = "",
#     ):
#         """基于 Pydantic 的 JSON 数据读写方法
#
#         参数:
#         - model (Union[BaseModel, List[BaseModel]], optional): 父类为 BaseModel 的模型
#         - file_path (Union[str, Path]): 要保存数据的文件路径
#         """
#         if not file_path:
#             raise ValueError("File path is required.")
#         self.model = model
#         self.file_path = file_path
#
#     def load(self) -> "JsonDataStorage.model":
#         """
#         从指定的文件路径加载 JSON 数据并将其转换为模型对象
#
#         返回:
#         - BaseModel: 解析后的模型对象
#         """
#         return self.model.parse_file(self.file_path)
#
#     def load_as_list(self) -> List["JsonDataStorage.model"]:
#         """
#         从指定的文件路径加载 JSON 数据并将其转换为模型对象列表
#
#         返回:
#         - List[BaseModel]: 解析后的模型对象列表
#         """
#         with open(self.file_path, "r", encoding="UTF-8") as file:
#             data: List[Dict[Any, Any]] = json.load(file)
#         return [self.model.parse_obj(d) for d in data]
#
#     def save(self, data: BaseModel) -> None:
#         """
#         将模型对象转换为 JSON 数据并保存到指定的文件路径
#
#         参数:
#         - data (BaseModel): 要保存的模型对象
#         """
#         with open(self.file_path, "w", encoding="UTF-8") as file:
#             json.dump(data.dict(), file, indent=4)
#
#     def save_as_list(self, data: List[BaseModel]) -> None:
#         """
#         将模型对象转换为列表 JSON 数据并保存到指定的文件路径
#
#         参数:
#         - data (List[BaseModel]): 要保存的模型对象列表
#         """
#         if type(data) != list:
#             raise ValueError("Only list-like object is suitable for this method.")
#         with open(self.file_path, "w", encoding="UTF-8") as file:
#             json.dump([d.dict() for d in data], file, indent=4)
#

current_dir = Path.cwd()

folder_path = Path(current_dir / "tsugu_config")
if not folder_path.exists():
    folder_path.mkdir()
config_file_path = f"{folder_path}/config.json"  # 配置文件路径


class Config(BaseModel):
    同意免责声明: Optional[str] = "同意"
    BACKEND_URL_RCD: Optional[str] = "http://tsugubot.com:8080"
    USE_EASY_BG: Optional[bool] = True
    DEFAULT_SERVERS: Optional[List[str]] = ["3", "0"]
    BIND_PLAYER_URL: Optional[str] = "不填写没玩家状态用("
    BOT_NAME: Optional[str] = "tsugu"
    HELP_TRIGGER: Optional[str] = "help"
    BANDORI_STATION_TOKEN: Optional[str] = "ZtV4EX2K9Onb"
    TOKEN_NAME: Optional[str] = "Tsugu"
    ADMIN_LIST: Optional[List[str]] = ["ALL"]
    BAN_GROUP_DATA: Optional[List[str]] = ["114514", "114513"]
    BAN_GACHA_SIMULATE_GROUP_DATA: Optional[List[str]] = ["114514", "114513"]
    BAN_GROUP_CAR_STATION_SEND: Optional[List[str]] = ["114514", "114513"]
    STATUS_ON_ECHO: Optional[str] = "喜多喜多"
    STATUS_OFF_ECHO: Optional[str] = "呜呜zoule"


def get_config():
    """
    读取配置文件，如果文件不存在则创建默认配置并写入文件
    """
    config_data = Config()
    if Path(config_file_path).exists():
        config_data = Config.parse_file(config_file_path)
        print(f"配置文件已读取: {config_file_path}")
    else:
        with open(f"{folder_path}/help_config.txt", "w", encoding="utf-8") as file:
            text = """HELP：
- `BACKEND_URL`: 后端地址，默认为 Tsugu 官方的地址。
- `USE_EASY_BG`: 是否使用简化背景，建议为 true，否则可能导致速度变慢且可能出现 bug。
- `DEFAULT_SERVERS`: 默认服务器顺序，3 表示国服，0 表示日服。
- `BIND_PLAYER_URL`: 绑定玩家状态的 API 地址，欢迎找 kumoSleeping 获取。
- `BOT_NAME`: Bot 的名字，默认为 "tsugu"。
- `HELP_TRIGGER`: 触发帮助的指令名，默认为 "help"。
- `BANDORI_STATION_TOKEN`: 车站 Token，默认为 Tsugu 的 Token。
- `TOKEN_NAME`: Token 名称，与车站 Token 绑定。
- `ADMIN_LIST`: 管理员列表，"ALL" 表示所有人，"114514" 是一个示例管理员 ID。
- `BAN_GROUP_DATA`: 停用 tsugu 的群聊列表，初始为空列表，可以使用 swc 指令控制，也可以手动修改。
- `BAN_GACHA_SIMULATE_GROUP_DATA`: 禁用抽卡模拟的群聊，因历史遗留保留此项，请管理员自己添加后重启，不单独提供指令。
- `BAN_GROUP_CAR_STATION_SEND`: 禁用车牌转发的群聊，因历史遗留保留此项，请管理员自己添加后重启，不单独提供指令。
- `STATUS_ON_ECHO`: bot被启用发出的提示。
- `STATUS_OFF_ECHO`: bot被停用发出的提示。
            """
            file.write(text)
        # 写入默认配置到文件
        personal_config_file_path = f"{folder_path}/personal_config.json"  # 配置文件路径
        with open(personal_config_file_path, "w", encoding="utf-8") as file:
            json.dump([], file, indent=4, ensure_ascii=False)
        print(f'已创建personal_config文件{personal_config_file_path}')
        with open(config_file_path, "w", encoding="utf-8") as file:
            json.dump(Config().dict(), file, indent=4, ensure_ascii=False)
            disclaimer ="""
            这里是免责声明。🍊
            前面忘了
            总之这个项目是山本推荐的的，非常简单好用，后面忘了。
            真好用，出错了一定是山本的问题（x）
            有问题、建议、困难，需求找 zhaomaoniu 就行。
            这个项目只支持cn，jp服务，因为其他没人用，也没人给我们做测试（悲）真有需求未来会同步更新。
            提issue或者来开发小群都是可以的～
            （这真的是免责声明吗？）
                                            ————kumoSleeping
            """
            print(f"默认配置已写入到: {config_file_path}\n请修改配置后重启。\n免责声明：\n{disclaimer}")
            exit()

    return config_data


# 在此处调用 get_config() 来获取配置信息
config = get_config()

# 使用配置信息
BACKEND_URL = config.BACKEND_URL_RCD
USE_EASY_BG = config.USE_EASY_BG
DEFAULT_SERVERS = config.DEFAULT_SERVERS
BIND_PLAYER_URL = config.BIND_PLAYER_URL
BOT_NAME = config.BOT_NAME
HELP_TRIGGER = config.HELP_TRIGGER
BANDORI_STATION_TOKEN = config.BANDORI_STATION_TOKEN
TOKEN_NAME = config.TOKEN_NAME
ADMIN_LIST = config.ADMIN_LIST
BAN_GROUP_DATA = config.BAN_GROUP_DATA
BAN_GACHA_SIMULATE_GROUP_DATA = config.BAN_GACHA_SIMULATE_GROUP_DATA
BAN_GROUP_CAR_STATION_SEND = config.BAN_GROUP_CAR_STATION_SEND
STATUS_ON_ECHO = config.STATUS_ON_ECHO
STATUS_OFF_ECHO = config.STATUS_OFF_ECHO


personal_config_file_path = f"{folder_path}/personal_config.json"  # 个人配置文件路径

with open(personal_config_file_path, 'r', encoding='utf-8') as config_file:
    personal_config = json.load(config_file)
print("读取本地个人配置项成功.")

# cmd_dict 可以用来设置别名
cmd_dict = {
    # （不支持换服务器优先级）
    HELP_TRIGGER: "Help",
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
    "ycx": "/ycx",  # ycx一定要放在 ycxall 后面，原因自己想
    "lsycx": "/lsycx",
    "抽卡模拟": "/gachaSimulate",
    '开启个人车牌转发': 'BD_STATION_ON_PERSONAL',
    '关闭个人车牌转发': 'BD_STATION_OFF_PERSONAL',
    '国服模式': 'SET_cn_mode',
    '日服模式': 'SET_jp_mode',
}

# 此列表键与 cmd_dict 保持一致
cmd_help_dict = {
    "swc": f"swc off {BOT_NAME} ·关闭本群Tsugu\nswc on {BOT_NAME} ·开启本群Tsugu",
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
    "ycx": "ycx 档位 活动ID ·查询预测线，只支持国服，活动ID非必填",  # ycx一定要放在 ycxall 后面，原因自己想
    "lsycx": "lsycx 活动ID ·返回档线、预测线、近4期同类活动的档线，只支持国服，活动ID非必填",
    "抽卡模拟": "抽卡模拟 次数 卡池ID ·抽卡模拟，次数、卡池ID非必填",
    '开启个人车牌转发': '开启个人车牌转发',
    '关闭个人车牌转发': '开启个人车牌转发',
    '国服模式': '国服模式',
    '日服模式': '日服模式',
}
non_arg_cmd = [
    "/songMeta",
    "PlayerStatus",
    "JPlayerStatus",
    "/roomList",
    "/gachaSimulate",
    "BindPlayer",
    "Help",
    "/ycxAll",
    "SET_jp_mode",
    "SET_cn_mode",
    "BD_STATION_OFF_PERSONAL",
    "BD_STATION_ON_PERSONAL",
]

language_mapping = {"jp": 0, "en": 1, "tw": 2, "cn": 3, "kr": 4}

car_config = {
    "car": [
        "车",
        "w",
        "W",
        "国",
        "日",
        "火",
        "q",
        "开",
        "Q",
        "万",
        "缺",
        "来",
        "差",
        "奇迹",
        "冲",
        "途",
        "分",
        "禁",
    ],
    "fake": [
        "114514",
        "假车",
        "测试",
        "野兽",
        "恶臭",
        "1919",
        "下北泽",
        "粪",
        "糞",
        "臭",
        "雀魂",
        "麻将",
        "打牌",
        "maj",
        "麻",
        "[",
        "]",
        "断幺",
        "11451",
        "xiabeize",
        "qq.com",
        "@",
        "q0",
        "q5",
        "q6",
        "q7",
        "q8",
        "q9",
        "q10",
        "腾讯会议",
        "master",
        "疯狂星期四",
        "离开了我们",
        "日元",
        "av",
        "bv",
    ],
}


# 获取personal数据
def get_personal_config(user_id: str):
    for config in personal_config:
        if config["user_id"] == user_id:
            return config["main_server_list"], config["STOP_car_retransmission"]

    return None, None


# 删除personal数据
def remove_personal_config(user_id: str):
    global personal_config

    # 查找并删除指定用户的配置项
    for config in personal_config:
        if config["user_id"] == user_id:
            personal_config.remove(config)
            break


# 添加personal数据 并保存
def add_personal_config_and_save(user_id: str, main_server_list: list, STOP_car_retransmission: bool):
    global personal_config
    personal_config.append({
        "user_id": user_id,
        "main_server_list": main_server_list,
        "STOP_car_retransmission": STOP_car_retransmission
    })
    with open(personal_config_file_path, 'w', encoding='utf-8') as f:
        json.dump(personal_config, f, indent=4, ensure_ascii=False)


# 获取玩家状态绑定数据
def get_data(user_id: str, server: str):
    url = f"{BIND_PLAYER_URL}/api/data?mode=get&user_id={user_id}&server={server}"
    try:
        with requests.Session() as session:
            response = session.get(url)
            response.raise_for_status()
            return response.text
    except requests.exceptions.RequestException as e:
        # 处理请求异常
        print(f"Error during HTTP request: {e}")
        return None


# 保存玩家状态绑定数据
def save_data(user_id: str, uid: str, server: str):
    url = f"{BIND_PLAYER_URL}/api/data?mode=save&user_id={user_id}&uid={uid}&server={server}"
    try:
        with requests.Session() as session:
            response = session.get(url)
            response.raise_for_status()
            return response.text
    except requests.exceptions.RequestException as e:
        # 处理请求异常
        print(f"Error during HTTP request: {e}")
        return None


# 处理玩家发送的 "绑定玩家 jp 114514" 类似的消息，调用上面的 save_data
def process_message(user_id: str, text: str):
    server = "jp" if "日服" in text or "jp" in text else "cn"
    uid = text.replace("绑定玩家", "").replace("日服", "").replace("jp", "").strip()
    ret_sav = save_data(user_id, uid, server)
    return [{"type": "string", "string": ret_sav}]


# 删除空值，因为python没有undefined
def remove_none_value(d: dict):
    return {k: v for k, v in d.items() if v}


# 发送data到Tsugu后端
def send_post_request(url, data):
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()  # 如果发生HTTP错误，将引发异常
        return response.json()
    except requests.exceptions.RequestException as e:
        return [{"type": "string", "string": f"后端服务器连接出错, {e}, {data}"}]
    except Exception as e:
        return [{"type": "string", "string": f"内部错误: {e}"}]


# 上面函数的具体实现，具体为什么这么写我也忘了
def get_data_from_backend(backend_url, api, data):
    try:
        result = send_post_request(f"{backend_url}{api}", data)
        return result
    except Exception as e:
        return [{"type": "string", "string": f"后端服务器连接出错, {e}, {data}"}]


# 核心接口
def tsugu_main(message: str, user_id: str, group_id: str):
    """
    接口函数
    接受 消息 ID ，触发成员ID，群ID
    返回 None 或者包含信息元素的 json
    """
    global config

    if config.同意免责声明.strip() != "同意":
        return [{"type": "string", "string": "请先在配置文件中同意免责声明！"}]

    # 检查是否是车牌 # 折叠此函数获得更好的浏览体验
    def check_message_isCar():
        """接受发来的原是消息
        检查是否是 合法 车牌
        返回布尔值"""
        isCar = False

        # 检查car_config['car']中的关键字
        for keyword in car_config["car"]:
            if keyword in message:
                isCar = True
                break

        # 检查car_config['fake']中的关键字
        for keyword in car_config["fake"]:
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
            url = f"https://api.bandoristation.com/index.php?function=submit_room_number&number={car_id}&user_id={user_id}&raw_message={message}&source={TOKEN_NAME}&token={BANDORI_STATION_TOKEN}"

            # 发送请求
            response = requests.get(url)

            if response.status_code != 200:
                print(f"提交车牌失败，HTTP响应码: {response.status_code}")
        except Exception as e:
            print(f"发生异常: {e}")

    # 2.非原生方法 # 折叠此函数获得更好的浏览体验
    def non_native_way(text: str, personal_server_list: list):

        if api == "Help":
            if text.strip() == "0":
                # unique_values = set(cmd_dict.values())  # 获取所有不重复的值
                unique_keys = {}  # 用于存储不同键对应的值

                for key, value in cmd_dict.items():
                    if value not in unique_keys:
                        unique_keys[value] = key

                result = "\n>> ".join(unique_keys.values())  # 用换行连接不同键对应的值
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
                        "string": ">> " + cmd_help_dict[text],
                    }
                ]
            else:
                return None

        elif api == "Swc":

            def add_or_remove_ban_group(group_id, add=True):
                global config
                """
                添加或移除 BAN_GROUP_DATA 中的群组ID。
                Args:
                    group_id (str): 要添加或移除的群组ID。
                    add (bool): True 表示添加，False 表示移除。
                """
                # 获取 BAN_GROUP_DATA
                ban_group_data = config.BAN_GROUP_DATA

                # 根据 add 参数添加或移除群组ID
                if add and group_id not in ban_group_data:
                    ban_group_data.append(group_id)
                elif not add and group_id in ban_group_data:
                    ban_group_data.remove(group_id)

                # 更新配置
                config.BAN_GROUP_DATA = ban_group_data

                # 保存回配置文件
                with open(config_file_path, "w", encoding="utf-8") as config_file:
                    json.dump(config.model_dump(), config_file, indent=4, ensure_ascii=False)

            # 验权
            if "ALL" not in ADMIN_LIST:
                if user_id in ADMIN_LIST:
                    pass
                elif user_id not in ADMIN_LIST and BOT_NAME in message.split():
                    return [
                        {
                            "type": "string",
                            "string": "权限不足",
                        }
                    ]
                else:
                    return None

            # 默认值
            if text.strip().startswith("off") and BOT_NAME in message:
                add_or_remove_ban_group(group_id, add=True)
                return [
                    {
                        "type": "string",
                        "string": STATUS_OFF_ECHO,
                    }
                ]
            if text.strip().startswith("on") and BOT_NAME in message:
                try:
                    add_or_remove_ban_group(group_id, add=False)
                except:
                    return None
                return [
                    {
                        "type": "string",
                        "string": STATUS_ON_ECHO,
                    }
                ]

        elif api == "PlayerStatus":
            if personal_server_list:
                server = int(personal_server_list[0])
                server_str = "jp" if server == 0 else "cn"
            else:
                server_str = "jp" if "日服" in text or "jp" in text else "cn"
                server = language_mapping.get(server_str, 3)

            uid = get_data(user_id, server_str)
            if uid == "找不到用户":
                return [
                    {
                        "type": "string",
                        "string": "发送 绑定玩家 uid ·绑定国服\n发送 绑定玩家 jp uid ·绑定日服",
                    }
                ]

            data = {
                "server": server,
                "useEasyBG": True,
                "playerId": int(uid),
            }
            print(data)

            return get_data_from_backend(
                backend_url=BACKEND_URL, api="/searchPlayer", data=data
            )
        elif api == "JPlayerStatus":
            server = "jp"
            uid = get_data(user_id, server)
            print(uid)
            if uid == "找不到用户":
                return [
                    {
                        "type": "string",
                        "string": "发送 绑定玩家 jp uid ·绑定日服",
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
            if text.strip() == "绑定玩家":
                return [
                    {
                        "type": "string",
                        "string": "发送 绑定玩家 uid ·绑定国服\n发送 绑定玩家 jp uid ·绑定日服\n·绑定日服一定要添加 jp 参数",
                    }
                ]

            return process_message(user_id, text)
        elif api == "BD_STATION_ON_PERSONAL":
            personal_server_list, STOP_personal_car_send = get_personal_config(user_id=user_id)
            # 因为没玩家数据会返回None，有玩家返回list，所以可以用 if存在 来判断是否要先删一下老数据
            if personal_server_list:
                remove_personal_config(user_id)
            add_personal_config_and_save(user_id=user_id, main_server_list=personal_server_list, STOP_car_retransmission=False)# 停用为假 就是开启
            return [
                {
                    "type": "string",
                    "string": "已开启个人车牌转发",
                }
            ]

        elif api == "BD_STATION_OFF_PERSONAL":
            personal_server_list, STOP_personal_car_send = get_personal_config(user_id=user_id)
            if personal_server_list:
                remove_personal_config(user_id)
            add_personal_config_and_save(user_id=user_id, main_server_list=personal_server_list, STOP_car_retransmission=True)  # 停用为真 就是关闭
            return [
                {
                    "type": "string",
                    "string": "已关闭个人车牌转发",
                }
            ]
        elif api == "SET_jp_mode":
            personal_server_list, STOP_personal_car_send = get_personal_config(user_id=user_id)
            if personal_server_list:
                remove_personal_config(user_id)
            add_personal_config_and_save(user_id=user_id, main_server_list=["0", "3"], STOP_car_retransmission=STOP_personal_car_send)
            return [
                {
                    "type": "string",
                    "string": "默认服务器已改为日服",
                }
            ]
        elif api == "SET_cn_mode":
            personal_server_list, STOP_personal_car_send = get_personal_config(user_id=user_id)
            if personal_server_list:
                remove_personal_config(user_id)
            add_personal_config_and_save(user_id=user_id, main_server_list=["3", "0"], STOP_car_retransmission=STOP_personal_car_send)
            return [
                {
                    "type": "string",
                    "string": "默认服务器已改为国服",
                }
            ]

        return None

    # 3.原生方法（url获取数据） # 折叠此函数获得更好的浏览体验
    def native_way(text: str, default_servers=DEFAULT_SERVERS):
        # 个人配置项
        if personal_server_list:
            default_servers = personal_server_list
        # 指令指定的服务器 优先级更高
        if "jp" in text.split() or "日服" in text.split():
            default_servers = ["0", "3"]
        elif "cn" in text.split() or "国服" in text.split():
            default_servers = ["3", "0"]
        else:
            pass

        text = text.replace("jp", "").replace("日服", "").strip()
        if api == "/searchEvent":
            data = {
                "default_servers": default_servers,
                "text": text,
                "useEasyBG": USE_EASY_BG,
            }
        elif api == "/searchSong":
            data = {
                "default_servers": default_servers,
                "text": text,
                "useEasyBG": USE_EASY_BG,
            }
        elif api == "/searchCard":
            data = {
                "default_servers": default_servers,
                "text": text,
                "useEasyBG": USE_EASY_BG,
            }
        elif api == "/songMeta":
            if not text:
                data = {
                    "default_servers": default_servers,
                    "useEasyBG": USE_EASY_BG,
                    "server": default_servers[0],
                }
            else:
                data = {
                    "default_servers": default_servers,
                    "useEasyBG": USE_EASY_BG,
                    "server": language_mapping.get(text, 3),
                }
        elif api == "/getCardIllustration":
            data = {
                "cardId": text,
            }
        elif api == "/searchCharacter":
            data = {"default_servers": default_servers, "text": str(text.split()[0])}
        elif api == "/searchGacha":
            data = {
                "default_servers": default_servers,
                "useEasyBG": USE_EASY_BG,
                "gachaId": text,
            }
        elif api == "/searchPlayer":
            data = {
                "server": language_mapping["jp" if "jp" in text else "cn"],
                "useEasyBG": True,
                "playerId": int(text.replace("cn", "").replace("jp", "").strip()),
            }
        elif api == "/lsycx":
            data = remove_none_value(
                {
                    "server": default_servers[0],
                    "tier": int(text.split()[0]),
                    "eventId": int(text.split()[1]) if len(text.split()) >= 2 else None,
                }
            )
        elif api == "/ycxAll":
            data = remove_none_value(
                {
                    "server": default_servers[0],
                    "eventId": text if text.strip() != "0" else None,
                }
            )
        elif api == "/ycx":
            data = remove_none_value(
                {
                    "server": default_servers[0],
                    "tier": int(text.split()[0]),
                    "eventId": int(text.split()[1]) if len(text.split()) >= 2 else None,
                }
            )
        elif api == "/songChart":
            if not text.split()[0].isdigit():
                return [{"type": "string", "string": "不合规范的歌曲ID"}]
            data = {
                "default_servers": default_servers,
                "songId": int(text.split()[0]),
                "difficultyText": text.split()[1] if len(text.split()) >= 2 else "ex",
            }
        elif api == "/gachaSimulate":
            if group_id in BAN_GACHA_SIMULATE_GROUP_DATA:
                return [{"type": "string", "string": "BOT主停用了本群的抽卡模拟功能"}]
            data = (
                remove_none_value(
                    {
                        "server_mode": default_servers[0],
                        "status": True,
                        "times": int(text.split()[0])
                        if text and int(text.split()[0]) < 10000
                        else 10,
                        "gachaId": int(text.split()[1])
                        if len(text.split()) >= 2
                        else None,
                    }
                )
                if text
                else {"server_mode": 3, "status": True, "times": 10}
            )

        elif api == "/roomList":
            try:
                response = requests.get(
                    "https://api.bandoristation.com/?function=query_room_number",
                )
                response.raise_for_status()
                response_json: dict = response.json()
                response_list: List[Dict[str, Any]] = response_json.get("response", [])

                room_dict = {}  # 用于存储最新时间的字典

                # 遍历原始列表，更新每个"number"对应的最新时间戳
                for item in response_list:
                    number = int(item.get("number", 0))
                    time = item["time"]
                    if number not in room_dict or time > room_dict.get(number)["time"]:
                        room_dict[number] = {
                            "number": number,
                            "rawMessage": item.get("raw_message", ""),
                            "source": item.get("source_info", {}).get("name", ""),
                            "userId": str(item.get("user_info", {}).get("user_id", "")),
                            "time": time,
                            "avanter": item.get("user_info", {}).get("avatar", None),
                            "userName": item.get("user_info", {}).get(
                                "username", "Bob"
                            ),
                        }
                room_list = list(room_dict.values())

                if room_list == []:
                    return [{"type": "string", "string": "myc"}]

                data = {"roomList": room_list}

            except Exception as e:
                return [{"type": "string", "string": f"错误：{e}"}]
        else:
            data = None

        print("data:", data)
        rpl = get_data_from_backend(backend_url=BACKEND_URL, api=api, data=data)
        room_list = []

        return rpl

    # 先检查本群是否被ban
    if group_id in config.BAN_GROUP_DATA:
        if message.startswith("swc"):
            pass
        else:
            return None
    personal_server_list, STOP_personal_car_send = get_personal_config(user_id=user_id)

    # 先检查是否为车牌，如果是
    result_car = check_message_isCar()
    if result_car:
        # 检查 STOP_personal_car_send ，为 Flase 或 None 时候 if STOP_personal_car_send 都不会被触发
        if STOP_personal_car_send:
            print('该用户 STOP车牌转发 True')
            return None
        if group_id in config.BAN_GROUP_CAR_STATION_SEND:
            print("该群禁止转发车牌")
            return None
        # 直接用1.车牌方法
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
        return non_native_way(text, personal_server_list)

    # 3.原生方法（网络获取）
    return native_way(text)


"""
=======================单条测试=======================
"""
# result = tsugu_main("123231 q1", "1528593481")
# result = tsugu_main("lsycx", "3274007482", '1')
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
"""
=======================循环测试=======================
"""
# user_id = "1528593481"
# group_id = "666808414"
# group_id = "114514"
# user_id = "114514"
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


