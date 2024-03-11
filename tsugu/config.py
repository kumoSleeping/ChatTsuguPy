
class Config:
    def __init__(self):
        # 设置默认值
        self.backend = "http://tsugubot.com:8080"
        self.user_data_backend = "http://tsugubot.com:8080"
        self.user_database_path = None

        self.use_proxies = False
        self.proxies = {
            "http": "http://127.0.0.1:7890",
            "https": "http://127.0.0.1:7890"
        }

        self.token_name = "Tsugu"
        self.bandori_station_token = "ZtV4EX2K9Onb"

        self.use_easy_bg = True
        self.compress = True

        self.ban_gacha_simulate_group_data = []

        self.server_list = {
            0: "日服",
            1: "国际服",
            2: "台服",
            3: "国服",
            4: "韩服"
        }
        self.server_name_to_index = {
            "日服": "0",
            "国际服": "1",
            "台服": "2",
            "国服": "3",
            "韩服": "4",
            "jp": "0",
            "en": "1",
            "tw": "2",
            "cn": "3",
            "kr": "4",
        }

        self.server_index_to_name = {
            "0": "日服",
            "1": "国际服",
            "2": "台服",
            "3": "国服",
            "4": "韩服",
        }

        self.server_index_to_s_name = {
            "0": "jp",
            "1": "en",
            "2": "tw",
            "3": "cn",
            "4": "kr",
        }

        self.commands = [
            {"api": "cardIllustration", "command_name": ["查插画", "查卡面"]},
            {"api": "card", "command_name": ["查卡"]},
            {"api": "player", "command_name": ["查玩家", "查询玩家"]},
            {"api": "gachaSimulate", "command_name": ["抽卡模拟", "卡池模拟"]},
            {"api": "event", "command_name": ["查活动"]},
            {"api": "song", "command_name": ["查歌曲", "查曲"]},
            {"api": "songMeta", "command_name": ["查询分数表", "查分数表"]},
            {"api": "character", "command_name": ["查角色"]},
            {"api": "chart", "command_name": ["查铺面", "查谱面"]},
            {"api": "ycxAll", "command_name": ["ycxall", "ycx all"]},
            {"api": "ycx", "command_name": ["ycx", "预测线"]},
            {"api": "lsycx", "command_name": ["lsycx"]},
            {"api": "ycm", "command_name": ["ycm", "车来"]}
        ]

        self.car_config = {
            "car": ["q1", "q2", "q3", "q4", "Q1", "Q2", "Q3", "Q4", "缺1", "缺2", "缺3", "缺4", "差1", "差2", "差3", "差4",
                    "3火", "三火", "3把", "三把", "打满", "清火", "奇迹", "中途", "大e", "大分e", "exi", "大分跳", "大跳", "大a", "大s",
                    "大分a", "大分s", "长途", "生日车", "军训", "禁fc"],
            "fake": ["114514", "野兽", "恶臭", "1919", "下北泽", "粪", "糞", "臭", "11451", "xiabeize", "雀魂", "麻将", "打牌",
                     "maj", "麻", "[", "]", "断幺", "qq.com", "腾讯会议", "master", "疯狂星期四", "离开了我们", "日元", "av", "bv"]
        }

    def show_docs(self):
        '''
Config 属性文档:

backend (str)
    默认值: "http://tsugubot.com:8080"
    描述: 应用程序的后端服务地址，需要 v2 API 。

user_data_backend (str)
    默认值: "http://tsugubot.com:8080"
    描述: 应用程序的后端服务地址，需要 v2 API ， 需要启动数据库服务。

utils_backend (str)
    默认值: "http://tsugubot.com:8080"
    描述: utils api 的后端地址，需要 v2 API 。

use_proxies (bool)
    默认值: False
    描述: 是否通过代理服务器访问网络服务。

proxies (dict)
    默认值: {"http": "http://127.0.0.1:7890", "https": "http://127.0.0.1:7890"}
    描述: 代理服务器的地址配置，use_proxies 为 True 时生效。

token_name (str)
    默认值: "Tsugu"
    描述: Bandori 车站 的上传令牌名称，通常需要和 bandori_station_token 一对应。

bandori_station_token (str)
    默认值: "ZtV4EX2K9Onb"
    描述: Bandori 车站 的上传令牌，通常需要和 token_name 一对应。

use_easy_bg (bool)
    默认值: True
    描述: 是否使用简易背景模式。

compress (bool)
    默认值: True
    描述: 是否开启数据压缩。

ban_gacha_simulate_group_data (list)
    默认值: []
    描述: 禁止抽卡模拟的群组数据列表。
    事例: ["114514", "1919810"]

server_list (dict)
    默认值: {1: "日服", 2: "国际服", 3: "台服", 4: "韩服"}
    描述: 服务器列表及其对应的名称。

server_index_to_name (dict)
    默认值: {"1": "日服", "2": "国际服", "3": "台服", "4": "韩服"}
    描述: 服务器索引到名称的映射。

server_index_to_s_name (dict)
    默认值: {"1": "jp", "2": "en", "3": "tw", "4": "kr"}
    描述: 服务器索引到简称的映射。

name_to_server_index (dict)
    默认值: {"日服": "1", "国际服": "2", "台服": "3", "韩服": "4"}
    描述: 服务器名称到索引的映射。

commands (list[dict])
    默认值: 包含多个字典，每个字典包含api和command_name键。
    描述: 应用程序支持的命令列表及其对应的API接口。
    查看默认值: https://github.com/kumoSleeping/tsugu-bangdream-bot-lite-py/blob/main/tsugu/config.py#L29
    可用函数: add_command_name, remove_command_name

car_config (dict)
    默认值: 包含两个键car和fake，每个键对应一个字符串列表。
    描述: 车辆配置，包含车辆相关的命令及排除词汇。
    查看默认值: https://github.com/kumoSleeping/tsugu-bangdream-bot-lite-py/blob/main/tsugu/config.py#L45
        '''
        print(self.show_docs.__doc__)
        return self.__doc__

    def add_command_name(self, api: str, command_name: str):
        """
        添加指令名
        """
        for command in self.commands:
            if command['api'] == api:
                if command_name not in command['command_name']:
                    command['command_name'].append(command_name)
                else:
                    print(f"command_name '{command_name}' already exists in api '{api}'.")
                break
        else:
            print(f"command_name '{command_name}' not found.")
        print(f"command_name '{command_name}' added to api '{api}'.")
        return self

    def remove_command_name(self, api: str, command_name: str):
        """
        删除指令名 (如果全删了则不会触发此命令)
        """
        for command in self.commands:
            if command['api'] == api:
                if command_name in command['command_name']:
                    command['command_name'].remove(command_name)
                else:
                    print(f"command_name '{command_name}' does not exist in api '{api}'.")
                break
        else:
            print(f"api '{api}' not found.")
        print(f"command_name '{command_name}' removed from api '{api}'.")


config = Config()


