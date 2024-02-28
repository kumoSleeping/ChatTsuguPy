
class Config:
    def __init__(self):
        # 设置默认值
        self.backend = "http://tsugubot.com:8080"
        self.user_data_backend = "http://tsugubot.com:8080"
        self.utils_backend = "http://tsugubot.com:8080"

        self.use_proxies = False
        self.proxies = {
            "http": "http://127.0.0.1:7890",
            "https": "http://127.0.0.1:7890"
        }

        self.token_name = "Tsugu"
        self.bandori_station_token = "ZtV4EX2K9Onb"

        self.use_default_server = False
        self.use_easy_bg = True
        self.compress = True

        self.ban_gacha_simulate_group_data = []

        self.commands = [
            {"action": "cardIllustration", "keys": ["查插画", "查卡面"]},
            {"action": "card", "keys": ["查卡"]},
            {"action": "player", "keys": ["查玩家", "查询玩家"]},
            {"action": "gachaSimulate", "keys": ["抽卡模拟", "卡池模拟"]},
            {"action": "event", "keys": ["查活动"]},
            {"action": "song", "keys": ["查歌曲", "查曲"]},
            {"action": "songMeta", "keys": ["查询分数表", "查分数表"]},
            {"action": "character", "keys": ["查角色"]},
            {"action": "chart", "keys": ["查铺面", "查谱面"]},
            {"action": "ycxAll", "keys": ["ycxall", "ycx all"]},
            {"action": "ycx", "keys": ["ycx", "预测线"]},
            {"action": "lsycx", "keys": ["lsycx"]},
            {"action": "ycm", "keys": ["ycm", "车来"]}
        ]

        self.server_list = {
            0: "日服",
            1: "国际服",
            2: "台服",
            3: "国服",
            4: "韩服"
        }

        self.car_config = {
            "car": ["q1", "q2", "q3", "q4", "Q1", "Q2", "Q3", "Q4", "缺1", "缺2", "缺3", "缺4", "差1", "差2", "差3", "差4",
                    "3火", "三火", "3把", "三把", "打满", "清火", "奇迹", "中途", "大e", "大分e", "exi", "大分跳", "大跳", "大a", "大s",
                    "大分a", "大分s", "长途", "生日车", "军训", "禁fc"],
            "fake": ["114514", "野兽", "恶臭", "1919", "下北泽", "粪", "糞", "臭", "11451", "xiabeize", "雀魂", "麻将", "打牌",
                     "maj", "麻", "[", "]", "断幺", "qq.com", "腾讯会议", "master", "疯狂星期四", "离开了我们", "日元", "av", "bv"]
        }

    def set_backend(self, backend_url: str) -> None:
        self.backend = backend_url
        print(f"Backend URL set to {backend_url}")

    def set_user_data_backend(self, backend_url: str) -> None:
        self.user_data_backend = backend_url
        print(f"User data backend URL set to {backend_url}")

    def set_utils_backend(self, backend_url: str) -> None:
        self.utils_backend = backend_url
        print(f"Utils backend URL set to {backend_url}")

    def set_use_proxies(self, use: bool) -> None:
        self.use_proxies = use
        print(f"Use proxies set to {use}")

    def set_proxies(self, proxies: dict) -> None:
        self.proxies = proxies
        print(f"Proxies set to {proxies}")

    def set_token_name(self, name: str) -> None:
        self.token_name = name
        print(f"Token name set to {name}")

    def set_bandori_station_token(self, token: str) -> None:
        self.bandori_station_token = token
        print(f"Bandori Station token set to {token}")

    def set_use_default_server(self, use: bool) -> None:
        self.use_default_server = use
        print(f"Use default server set to {use}")

    def set_use_easy_bg(self, use: bool) -> None:
        self.use_easy_bg = use
        print(f"Use EasyBG set to {use}")

    def set_compress(self, compress: bool) -> None:
        self.compress = compress
        print(f"Compress set to {compress}")

    def add_ban_gacha_simulate_group_data(self, group_id: str) -> None:
        if group_id not in self.ban_gacha_simulate_group_data:
            self.ban_gacha_simulate_group_data.append(group_id)
        else:
            print(f"Group ID '{group_id}' already exists in ban gacha simulate group data.")
        print(f"Group ID '{group_id}' added to ban gacha simulate group data.")

    def add_command_key(self, action: str, key: str) -> None:
        """
        添加别名
        """
        for command in self.commands:
            if command['action'] == action:
                if key not in command['keys']:
                    command['keys'].append(key)
                else:
                    print(f"Key '{key}' already exists in action '{action}'.")
                break
        else:
            print(f"Action '{action}' not found.")
        print(f"Key '{key}' added to action '{action}'.")

    def remove_command_key(self, action: str, key: str) -> None:
        """
        删除别名
        """
        for command in self.commands:
            if command['action'] == action:
                if key in command['keys']:
                    command['keys'].remove(key)
                else:
                    print(f"Key '{key}' does not exist in action '{action}'.")
                break
        else:
            print(f"Action '{action}' not found.")
        print(f"Key '{key}' removed from action '{action}'.")

    def set_server_list(self, server_list: dict[int, str]) -> None:
        self.server_list = server_list
        print(f"Server list set to {server_list}")

    def add_car_config(self, category: str, value: str) -> None:
        """
        向car_config的特定类别（car或fake）添加一个新值。
        category填写'car'或'fake'。
        """
        if category in ['car', 'fake']:
            if value not in self.car_config[category]:
                self.car_config[category].append(value)
            else:
                print(f"Value '{value}' already exists in '{category}'.")
        else:
            print(f"Category '{category}' is not valid. Choose 'car' or 'fake'.")
        print(f"Value '{value}' added to '{category}'.")

    def remove_car_config(self, category: str, value: str) -> None:
        """
        从car_config的特定类别（car或fake）移除一个已存在的值。
        category填写'car'或'fake'。
        """
        if category in ['car', 'fake']:
            if value in self.car_config[category]:
                self.car_config[category].remove(value)
            else:
                print(f"Value '{value}' does not exist in '{category}'.")
        else:
            print(f"Category '{category}' is not valid. Choose 'car' or 'fake'.")
        print(f"Value '{value}' removed from '{category}'.")


tsugu_config = Config()


