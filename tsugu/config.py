import json


class Config:
    def __init__(self):
        self.user_database_path = None
        # 设置默认值
        self.backend = "http://tsugubot.com:8080"
        self.user_data_backend = "http://tsugubot.com:8080"
        self.backend_use_proxy = False
        self.user_data_backend_use_proxy = False
        self.submit_car_number_use_proxy = False
        self.verify_player_bind_use_proxy = False
        self.proxy_url = "http://localhost:7890"
        self.token_name = "Tsugu"
        self.bandori_station_token = "ZtV4EX2K9Onb"

        self.use_easy_bg = True
        self.compress = True

        self.ban_gacha_simulate_group_data = []

        self.server_list = {0: "日服", 1: "国际服", 2: "台服", 3: "国服", 4: "韩服"}
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

        self.features = {
                "car_number_forwarding": True,
                "change_main_server": True,
                "switch_car_forwarding": True,
                "bind_player": True,
                "change_server_list": True,
                "player_status": True,
                "help": True,
            }

        self.commands = [
            {"api": "cardIllustration", "command_name": ["查插画", "查卡面"]},
            {"api": "player", "command_name": ["查玩家", "查询玩家"]},
            {"api": "gachaSimulate", "command_name": ["抽卡模拟", "卡池模拟"]},
            {"api": "gacha", "command_name": ["查卡池"]},
            {"api": "event", "command_name": ["查活动"]},
            {"api": "song", "command_name": ["查歌曲", "查曲"]},
            {"api": "songMeta", "command_name": ["查询分数表", "查分数表"]},
            {"api": "character", "command_name": ["查角色"]},
            {"api": "chart", "command_name": ["查铺面", "查谱面"]},
            {"api": "ycxAll", "command_name": ["ycxall", "ycx all"]},
            {"api": "ycx", "command_name": ["ycx", "预测线"]},
            {"api": "lsycx", "command_name": ["lsycx"]},
            {"api": "ycm", "command_name": ["ycm", "车来"]},
            {"api": "card", "command_name": ["查卡"]},
        ]

        self.car_config = {
            "car": [
                "q1",
                "q2",
                "q3",
                "q4",
                "Q1",
                "Q2",
                "Q3",
                "Q4",
                "缺1",
                "缺2",
                "缺3",
                "缺4",
                "差1",
                "差2",
                "差3",
                "差4",
                "3火",
                "三火",
                "3把",
                "三把",
                "打满",
                "清火",
                "奇迹",
                "中途",
                "大e",
                "大分e",
                "exi",
                "大分跳",
                "大跳",
                "大a",
                "大s",
                "大分a",
                "大分s",
                "长途",
                "生日车",
                "军训",
                "禁fc",
            ],
            "fake": [
                "114514",
                "野兽",
                "恶臭",
                "1919",
                "下北泽",
                "粪",
                "糞",
                "臭",
                "11451",
                "xiabeize",
                "雀魂",
                "麻将",
                "打牌",
                "maj",
                "麻",
                "[",
                "]",
                "断幺",
                "qq.com",
                "腾讯会议",
                "master",
                "疯狂星期四",
                "离开了我们",
                "日元",
                "av",
                "bv",
            ],
        }
        self.help_doc_dict = {
            "玩家状态": """
查询指定玩家的状态信息。
使用示例：
    玩家状态 : 查询你当前默认服务器的玩家状态
    玩家状态  jp : 查询日服玩家状态
    玩家状态 2 : 查询您的第二个绑定玩家的状态(*此功能需要BOT支持)
        
""",
            "开关车牌转发": """
开启或关闭车牌转发功能，针对个人
使用示例：
    开启车牌转发 : 开启车牌转发功能
    关闭车牌转发 : 关闭车牌转发功能
""",
            "绑定玩家": """
绑定玩家ID到当前账号
使用示例：
    绑定玩家 : 绑定玩家开始绑定玩家流程(*请根据BOT的提示进行操作)
""",
            "解除绑定": """
解除绑定玩家ID
使用示例：
    解除绑定 : 解除绑定玩家开始解绑玩家流程(*请根据BOT的提示进行操作)
""",
            "切换主服务器": """
切换主服务器
使用示例：
    主服务器 jp : 切换主服务器到日服
    国服模式 : 切换主服务器到国服
""",
            "设置默认服务器": """
可以改变查询时的资源优先顺序
设置默认服务器，使用空格分隔服务器列表
使用示例：
    设置默认服务器 国服 日服 : 将国服设置为第一服务器，日服设置为第二服务器
""",
            "查卡面": """
根据卡片ID查询卡片插画
使用示例：
    查卡面 1399 :返回1399号卡牌的插画
""",
            "查询玩家": """
查询指定ID玩家的信息。省略服务器名时，默认从你当前的主服务器查询
使用示例：
    查玩家 10000000 : 查询你当前默认服务器中，玩家ID为10000000的玩家信息
    查玩家 40474621 jp : 查询日服玩家ID为40474621的玩家信息
""",
            "卡池模拟": """
模拟抽卡，如果没有卡池ID的话，卡池为当前活动的卡池
使用示例：
    抽卡模拟:模拟抽卡10次
    抽卡模拟 300 922 :模拟抽卡300次，卡池为922号卡池
""",
            "查卡池": """
根据卡池ID查询卡池信息
""",
            "查活动": """
根据关键词或活动ID查询活动信息
使用示例：
    查活动 177 :返回177号活动的信息
    查活动 绿 tsugu :返回所有属性加成为pure，且活动加成角色中包括羽泽鸫的活动列表
    查活动 >255 :返回所有活动ID大于255的活动列表
    查活动 255-256 :返回所有活动ID在255到256之间的活动列表
    查活动 ppp :匹配到 PPP 乐队的活动信息
""",
            "查曲": """
根据关键词或曲目ID查询曲目信息
使用示例：
    查曲 1 :返回1号曲的信息
    查曲 ag lv27 :返回所有难度为27的ag曲列表
    查曲 1 ex :返回1号曲的expert难度曲目信息
    查曲 滑滑蛋 :匹配到 ふわふわ時間 的曲目信息
""",
            "查分数表": """
查询指定服务器的歌曲分数表，如果没有服务器名的话，服务器为用户的默认服务器
""",
            "查角色": """
根据关键词或角色ID查询角色信息
使用示例：
    查角色 10 :返回10号角色的信息
    查角色 吉他 :返回所有角色模糊搜索标签中包含吉他的角色列表
""",
            "查谱面": """
根据曲目ID与难度查询铺面信息
使用示例：
    查谱面 1 :返回1号曲的所有铺面
    查谱面 1 expert :返回1号曲的expert难度铺面
""",
            "ycxall": """
查询所有档位的预测线，如果没有服务器名的话，服务器为用户的默认服务器。如果没有活动ID的话，活动为当前活动
可用档线:
20, 30, 40, 50, 100, 200, 300, 400, 500, 1000, 2000, 5000, 10000, 20000, 30000, 50000, 

使用示例：
    ycxall :返回默认服务器当前活动所有档位的档线与预测线
    ycxall 177 jp:返回日服177号活动所有档位的档线与预测线
""",
            "ycx": """
查询指定档位的预测线，如果没有服务器名的话，服务器为用户的默认服务器。如果没有活动ID的话，活动为当前活动
可用档线:
20, 30, 40, 50, 100, 200, 300, 400, 500, 1000, 2000, 5000, 10000, 20000, 30000, 50000, 
使用示例：
    ycx 1000 :返回默认服务器当前活动1000档位的档线与预测线
    ycx 1000 177 jp:返回日服177号活动1000档位的档线与预测线
""",
            "lsycx": """
与ycx的区别是，lsycx会返回与最近的4期活动类型相同的活动的档线数据
查询指定档位的预测线，与最近的4期活动类型相同的活动的档线数据，如果没有服务器名的话，服务器为用户的默认服务器。如果没有活动ID的话，活动为当前活动
可用档线:
20, 30, 40, 50, 100, 200, 300, 400, 500, 1000, 2000, 5000, 10000, 20000, 30000, 50000, 

使用示例：
    lsycx 1000 :返回默认服务器当前活动的档线与预测线，与最近的4期活动类型相同的活动的档线数据
    lsycx 1000 177 jp:返回日服177号活动1000档位档线与最近的4期活动类型相同的活动的档线数据
""",
            "ycm": """
获取所有车牌车牌
使用示例：
    ycm : 获取所有车牌
""",
            "查卡": """
根据关键词或卡牌ID查询卡片信息，请使用空格隔开所有参数
使用示例：
    查卡 1399 :返回1399号卡牌的信息
    查卡 绿 tsugu :返回所有属性为pure的羽泽鸫的卡牌列表
    查卡 kfes ars :返回所有为kfes的ars的卡牌列表
""",
        }

    def show_docs(self):

        pass
        return None

    def output_config_json(self, path="./config.json"):
        config_pre_json = {
            # 不输出数据库路径
            "backend": "http://tsugubot.com:8080",
            "user_data_backend": "http://tsugubot.com:8080",
            "backend_use_proxy": False,
            "user_data_backend_use_proxy": False,
            "submit_car_number_use_proxy": False,
            "verify_player_bind_use_proxy": False,
            "proxy_url": "http://localhost:7890",
            "token_name": "Tsugu",
            "bandori_station_token": "ZtV4EX2K9Onb",
            "use_easy_bg": True,
            "compress": True,
            "ban_gacha_simulate_group_data": [],
            "server_list": {
                "0": "日服",
                "1": "国际服",
                "2": "台服",
                "3": "国服",
                "4": "韩服",
            },
            "server_name_to_index": {
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
            },
            "server_index_to_name": {
                "0": "日服",
                "1": "国际服",
                "2": "台服",
                "3": "国服",
                "4": "韩服",
            },
            "server_index_to_s_name": {
                "0": "jp",
                "1": "en",
                "2": "tw",
                "3": "cn",
                "4": "kr",
            },
            "features": {
                "car_number_forwarding": True,
                "change_main_server": True,
                "switch_car_forwarding": True,
                "bind_player": True,
                "change_server_list": True,
                "player_status": True,
                "help": True,
            },
            "commands": [
                {"api": "cardIllustration", "command_name": ["查插画", "查卡面"]},
                {"api": "player", "command_name": ["查玩家", "查询玩家"]},
                {"api": "gachaSimulate", "command_name": ["抽卡模拟", "卡池模拟"]},
                {"api": "gacha", "command_name": ["查卡池"]},
                {"api": "event", "command_name": ["查活动"]},
                {"api": "song", "command_name": ["查歌曲", "查曲"]},
                {"api": "songMeta", "command_name": ["查询分数表", "查分数表"]},
                {"api": "character", "command_name": ["查角色"]},
                {"api": "chart", "command_name": ["查铺面", "查谱面"]},
                {"api": "ycxAll", "command_name": ["ycxall", "ycx all"]},
                {"api": "ycx", "command_name": ["ycx", "预测线"]},
                {"api": "lsycx", "command_name": ["lsycx"]},
                {"api": "ycm", "command_name": ["ycm", "车来"]},
                {"api": "card", "command_name": ["查卡"]},
            ],
            "car_config": {
                "car": [
                    "q1",
                    "q2",
                    "q3",
                    "q4",
                    "Q1",
                    "Q2",
                    "Q3",
                    "Q4",
                    "缺1",
                    "缺2",
                    "缺3",
                    "缺4",
                    "差1",
                    "差2",
                    "差3",
                    "差4",
                    "3火",
                    "三火",
                    "3把",
                    "三把",
                    "打满",
                    "清火",
                    "奇迹",
                    "中途",
                    "大e",
                    "大分e",
                    "exi",
                    "大分跳",
                    "大跳",
                    "大a",
                    "大s",
                    "大分a",
                    "大分s",
                    "长途",
                    "生日车",
                    "军训",
                    "禁fc",
                ],
                "fake": [
                    "114514",
                    "野兽",
                    "恶臭",
                    "1919",
                    "下北泽",
                    "粪",
                    "糞",
                    "臭",
                    "11451",
                    "xiabeize",
                    "雀魂",
                    "麻将",
                    "打牌",
                    "maj",
                    "麻",
                    "[",
                    "]",
                    "断幺",
                    "qq.com",
                    "腾讯会议",
                    "master",
                    "疯狂星期四",
                    "离开了我们",
                    "日元",
                    "av",
                    "bv",
                ],
            },
            "help_doc_dict": {
                "玩家状态": """
查询指定玩家的状态信息。
使用示例：
    玩家状态 : 查询你当前默认服务器的玩家状态
    玩家状态  jp : 查询日服玩家状态
    玩家状态 2 : 查询您的第二个绑定玩家的状态(*此功能需要BOT支持)
        
""",
                "开关车牌转发": """
开启或关闭车牌转发功能，针对个人
使用示例：
    开启车牌转发 : 开启车牌转发功能
    关闭车牌转发 : 关闭车牌转发功能
""",
                "绑定玩家": """
绑定玩家ID到当前账号
使用示例：
    绑定玩家 : 绑定玩家开始绑定玩家流程(*请根据BOT的提示进行操作)
""",
                "解除绑定": """
解除绑定玩家ID
使用示例：
    解除绑定 : 解除绑定玩家开始解绑玩家流程(*请根据BOT的提示进行操作)
""",
                "切换主服务器": """
切换主服务器
使用示例：
    主服务器 jp : 切换主服务器到日服
    国服模式 : 切换主服务器到国服
""",
                "设置默认服务器": """
可以改变查询时的资源优先顺序
设置默认服务器，使用空格分隔服务器列表
使用示例：
    设置默认服务器 国服 日服 : 将国服设置为第一服务器，日服设置为第二服务器
""",
                "查卡面": """
根据卡片ID查询卡片插画
使用示例：
    查卡面 1399 :返回1399号卡牌的插画
""",
                "查询玩家": """
查询指定ID玩家的信息。省略服务器名时，默认从你当前的主服务器查询
使用示例：
    查玩家 10000000 : 查询你当前默认服务器中，玩家ID为10000000的玩家信息
    查玩家 40474621 jp : 查询日服玩家ID为40474621的玩家信息
""",
                "卡池模拟": """
模拟抽卡，如果没有卡池ID的话，卡池为当前活动的卡池
使用示例：
    抽卡模拟:模拟抽卡10次
    抽卡模拟 300 922 :模拟抽卡300次，卡池为922号卡池
""",
                "查卡池": """
根据卡池ID查询卡池信息
""",
                "查活动": """
根据关键词或活动ID查询活动信息
使用示例：
    查活动 177 :返回177号活动的信息
    查活动 绿 tsugu :返回所有属性加成为pure，且活动加成角色中包括羽泽鸫的活动列表
    查活动 >255 :返回所有活动ID大于255的活动列表
    查活动 255-256 :返回所有活动ID在255到256之间的活动列表
    查活动 ppp :匹配到 PPP 乐队的活动信息
""",
                "查曲": """
根据关键词或曲目ID查询曲目信息
使用示例：
    查曲 1 :返回1号曲的信息
    查曲 ag lv27 :返回所有难度为27的ag曲列表
    查曲 1 ex :返回1号曲的expert难度曲目信息
    查曲 滑滑蛋 :匹配到 ふわふわ時間 的曲目信息
""",
                "查分数表": """
查询指定服务器的歌曲分数表，如果没有服务器名的话，服务器为用户的默认服务器
""",
                "查角色": """
根据关键词或角色ID查询角色信息
使用示例：
    查角色 10 :返回10号角色的信息
    查角色 吉他 :返回所有角色模糊搜索标签中包含吉他的角色列表
""",
                "查谱面": """
根据曲目ID与难度查询铺面信息
使用示例：
    查谱面 1 :返回1号曲的所有铺面
    查谱面 1 expert :返回1号曲的expert难度铺面
""",
                "ycxall": """
查询所有档位的预测线，如果没有服务器名的话，服务器为用户的默认服务器。如果没有活动ID的话，活动为当前活动
可用档线:
20, 30, 40, 50, 100, 200, 300, 400, 500, 1000, 2000, 5000, 10000, 20000, 30000, 50000, 

使用示例：
    ycxall :返回默认服务器当前活动所有档位的档线与预测线
    ycxall 177 jp:返回日服177号活动所有档位的档线与预测线
""",
                "ycx": """
查询指定档位的预测线，如果没有服务器名的话，服务器为用户的默认服务器。如果没有活动ID的话，活动为当前活动
可用档线:
20, 30, 40, 50, 100, 200, 300, 400, 500, 1000, 2000, 5000, 10000, 20000, 30000, 50000, 
使用示例：
    ycx 1000 :返回默认服务器当前活动1000档位的档线与预测线
    ycx 1000 177 jp:返回日服177号活动1000档位的档线与预测线
""",
                "lsycx": """
与ycx的区别是，lsycx会返回与最近的4期活动类型相同的活动的档线数据
查询指定档位的预测线，与最近的4期活动类型相同的活动的档线数据，如果没有服务器名的话，服务器为用户的默认服务器。如果没有活动ID的话，活动为当前活动
可用档线:
20, 30, 40, 50, 100, 200, 300, 400, 500, 1000, 2000, 5000, 10000, 20000, 30000, 50000, 

使用示例：
    lsycx 1000 :返回默认服务器当前活动的档线与预测线，与最近的4期活动类型相同的活动的档线数据
    lsycx 1000 177 jp:返回日服177号活动1000档位档线与最近的4期活动类型相同的活动的档线数据
""",
                "ycm": """
获取所有车牌车牌
使用示例：
    ycm : 获取所有车牌
""",
                "查卡": """
根据关键词或卡牌ID查询卡片信息，请使用空格隔开所有参数
使用示例：
    查卡 1399 :返回1399号卡牌的信息
    查卡 绿 tsugu :返回所有属性为pure的羽泽鸫的卡牌列表
    查卡 kfes ars :返回所有为kfes的ars的卡牌列表
""",
            },
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(config_pre_json, f, ensure_ascii=False, indent=4)
        print(f"Config data has been output to '{path}'.")

    def reload_from_json(self, path):
        """Reloads configuration data from a JSON string or a JSON file path."""
        with open(path, "r", encoding="utf-8") as file:
            config_data = json.load(file)
        # Iterate over all keys in the input JSON and update the config attributes
        for key, value in config_data.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                print(f"Warning: {key} is not a recognized configuration attribute.")


config = Config()
