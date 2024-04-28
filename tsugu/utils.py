from typing import List
import re
import json
import sqlite3
import os
import sys
import random
import urllib3
from urllib3.exceptions import HTTPError
from loguru import logger

from .config import config


class DatabaseManager:
    def __init__(self, path):
        self.path = path
        self.conn = None
        self.cursor = None
        self.init_db(self.path)

    def init_db(self, path):
        if path:
            self.conn = sqlite3.connect(path, check_same_thread=False)
            logger.success(f'数据库连接成功，路径: {path}')
            self.cursor = self.conn.cursor()
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT UNIQUE,
                    platform TEXT,
                    server_mode INTEGER,
                    default_server TEXT,
                    car INTEGER,
                    game_ids TEXT,
                    verify_code TEXT
                )
            ''')
            self.conn.commit()
        else:
            # 如果不使用数据库，设置连接为 None
            self.conn = None
            # logger.info('不使用数据库')

    def close_db(self):
        if self.conn:
            self.conn.close()

    def execute_query(self, query):
        if self.cursor:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        else:
            return []


db_manager = DatabaseManager(config.user_database_path)


def database(path: str | None = None):
    '''
    初始化数据库
    :return:
    '''
    if not path:
        path = (os.path.dirname(sys.modules['__main__'].__file__))
    config.user_database_path = path
    db_manager.init_db(path)


def text_response(string):
    return [{"type": "string", "string": string}]


def convert_server_names_to_indices(server_names: str) -> list:
    indices_list = [config.server_name_to_index.get(name, "Unknown") for name in server_names.split(" ")]
    result = [index for index in indices_list if index != "Unknown"]
    # 转化成数字，例如 ["0", "1"] -> [0, 1]
    return [int(i) for i in result]


def query_server_info(server_name: str) -> int:
    server = convert_server_names_to_indices(server_name)[0] if convert_server_names_to_indices(server_name) else None
    return server


def server_exists(server):
    if server or server == 0:
        return True
    return False


def requests_post_for_user(url, data):
    if config.user_data_backend_use_proxy:
        http = urllib3.ProxyManager(config.proxy_url, cert_reqs='CERT_NONE')
    else:
        http = urllib3.PoolManager(cert_reqs='CERT_NONE')
    try:
        response = http.request('POST', url, headers={'Content-Type': 'application/json'}, body=json.dumps(data))
        # 检查响应的状态码是否为 200
        if response.status == 200:
            return json.loads(response.data.decode('utf-8'))
        elif response.status == 400:
            return json.loads(response.data.decode('utf-8'))
        else:
            # 处理其他状态码
            return {"status": "error", "message": "服务器出现了问题，请稍后再试。"}

    except HTTPError as http_err:
        logger.error(f'HTTP 错误：{http_err}')
        return {"status": "error", "message": "服务器出现了问题，请稍后再试。"}

    except Exception as e:
        logger.error(f'发生异常：{e}')
        return {"status": "error", "message": "发生了未知错误。"}


def requests_post_for_backend(url, data):
    if config.backend_use_proxy:
        http = urllib3.ProxyManager(config.proxy_url, cert_reqs='CERT_NONE')
    else:
        http = urllib3.PoolManager(cert_reqs='CERT_NONE')
    try:
        response = http.request('POST', url, headers={'Content-Type': 'application/json'}, body=json.dumps(data))

        # 检查响应的状态码是否为 200
        if response.status == 200:
            return json.loads(response.data.decode('utf-8'))
        else:
            # 处理其他状态码
            return text_response("服务器出现了问题，请稍后再试。")

    except HTTPError as http_err:
        logger.error(f'HTTP 错误：{http_err}')
        return text_response("服务器出现了问题，请稍后再试。")

    except Exception as e:
        logger.error(f'发生异常：{e}')
        return text_response("发生了未知错误。")


def v2api_from_backend(api, text, default_servers: List[int] = None, server=3):
    if default_servers is None:
        default_servers = [3, 0]
    path = f"/v2/{api}"
    data = {
        "default_servers": default_servers,
        "server": server,
        "text": text,
        "useEasyBG": config.use_easy_bg,
        "compress": config.compress
    }
    res = requests_post_for_backend(f"{config.backend}{path}", data)
    return res


def v2_api_command(message, command_matched, api, platform, user_id, channel_id):
    text = message[len(command_matched):].strip()

    if api in ['cardIllustration', 'ycm']:  # 无需验证server信息
        return v2api_from_backend(api, text)

    if api == 'gachaSimulate':
        if channel_id in config.ban_gacha_simulate_group_data:
            return text_response('此群禁止使用模拟抽卡功能')

    # 获取用户数据
    import logging
    logging.debug(config.user_database_path)
    user_data = get_user_data(platform, user_id) if config.user_database_path else Remote.get_user_data(platform, user_id)
    try:
        if user_data['status'] != 'success':
            return text_response('获取用户数据失败：内部错误')
        return v2api_from_backend(api, text, user_data['data']['default_server'], user_data['data']['server_mode'])
    except Exception as e:
        return text_response('获取用户数据失败：网络 / 前端错误')


def submit_car_number_msg(message, user_id, platform=None):
    # 检查car_config['car']中的关键字
    for keyword in config.car_config["car"]:
        if str(keyword) in message:
            break
    else:
        return False
    # 检查car_config['fake']中的关键字
    for keyword in config.car_config["fake"]:
        if str(keyword) in message:
            return False
    pattern = r"^\d{5}(\D|$)|^\d{6}(\D|$)"
    if not re.match(pattern, message):
        return False

    # 获取用户数据
    try:
        if platform:
            user_data = get_user_data(platform, user_id) if config.user_database_path else Remote.get_user_data(platform, user_id)
            if not user_data['data']['car']:
                return True
    except Exception as e:
        logger.error('unknown user')
        # 默认不开启关闭车牌，继续提交
        pass

    try:
        car_id = message[:6]
        if not car_id.isdigit() and car_id[:5].isdigit():
            car_id = car_id[:5]

        # 构建 URL
        url = f"https://api.bandoristation.com/index.php?function=submit_room_number&number={car_id}&user_id={user_id}&raw_message={message}&source={config.token_name}&token={config.bandori_station_token}"

        if config.submit_car_number_use_proxy:
            http = urllib3.ProxyManager(config.proxy_url, cert_reqs='CERT_NONE')
        else:
            http = urllib3.PoolManager(cert_reqs='CERT_NONE')

        # 发送请求
        response = http.request('GET', url)

        # 检查响应的状态码是否为 200
        if response.status == 200:
            return True
        else:
            logger.error(f"[Tsugu] 提交车牌失败，HTTP响应码: {response.status}")
            return True  # 虽然提交失败，但是确定了是车牌消息

    except Exception as e:
        logger.error(f"[Tsugu] 发生异常: {e}")
        return True  # 虽然提交失败，但是确定了是车牌消息


def match_command(message, cmd_dict):
    for command, api_value in cmd_dict.items():
        if message.startswith(command):
            return command, api_value
    return None, None


def load_commands_from_config(data):
    # 初始化一个空字典来存储命令到操作的映射
    cmd_dict = {}
    for item in data:
        api = item['api']
        for command_name in item['command_name']:
            cmd_dict[command_name] = api
    return cmd_dict



def get_user_data(platform: str, user_id: str):

    cursor = db_manager.conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ? AND platform = ?", (user_id, platform))
    row = cursor.fetchone()

    if row:
        data = {
            "user_id": row[1],
            "platform": row[2],
            "server_mode": row[3],
            "default_server": list(json.loads(row[4])),
            "car": row[5],
            "game_ids": row[6],
            "verify_code": row[7]
        }
    else:
        data = {
            "user_id": user_id,
            "platform": platform,
            "server_mode": 3,
            "default_server": [3, 0],
            "car": 1,
            "game_ids": json.dumps([]),
            "verify_code": ""
        }
        cursor.execute('''
        INSERT INTO users (user_id, platform, server_mode, default_server, car, game_ids)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, platform, 3, json.dumps([3, 0]), 1, json.dumps([])))
        db_manager.conn.commit()
    result = {
        "status": "success",
        "data": data
    }
    return result


def player_status(user_id, platform, args: str | int | None = None):
    user_data = get_user_data(platform, user_id)
    game_ids = user_data['data']['game_ids']
    if game_ids == "[]" or not game_ids:
        return text_response(f'未绑定玩家，请发送 绑定玩家 进行绑定')
    game_ids = json.loads(game_ids)
    text = ''
    if args is None:
        # 先查找默认服务器对应的记录
        server: int = user_data['data']['server_mode']
        for i in game_ids:
            if i.get("server") == server:
                player_id = str(i.get("game_id"))
                server = int(i.get("server"))

                text = f'已查找默认服务器 {config.server_index_to_name[str(server)]} 的记录'
                break
        else:
            # 再查找第一个记录
            if game_ids:
                return text_response(f'未在 {len(game_ids)} 条记录中找到 {config.server_index_to_name[str(server)]} 的记录')
            else:
                pass  # 前面已经判断过了没绑定任何的情况
    elif isinstance(args, int):
        # 查找对应数字的记录
        if args == 0:
            return text_response('哪来的0（')
        if args > len(game_ids) or args < 1:
            return text_response(f'总共绑定了 {len(game_ids)} 条记录')
        player_id, server = str(game_ids[args - 1].get("game_id")), game_ids[args - 1].get("server")
        text = f'已为查找第{args}条记录'
        if not player_id:
            return text_response(f'未找到此服务器的记录，请检查是否绑定过此服务器')

    elif isinstance(args, str):
        server = query_server_info(args)
        # 查找对应服务器的记录
        for i in game_ids:
            if i.get("server") == server:
                player_id = str(i.get("game_id"))
                text = f'已查找服务器 {config.server_index_to_name[str(server)]} 的记录'
                break
        else:
            return text_response(f'未找到记录，请检查是否绑定过此服务器')
    else:
        return text_response('参数错误，的服务器可能不合法')
    result: list = v2api_from_backend('player', player_id, server=server)
    new_item = {"type": "string", "string": text}
    result.append(new_item)
    return result


def set_car_forward(platform, user_id, status: bool):

    if status:
        status = 1
    else:
        status = 0
    get_user_data(platform, user_id)
    cursor = db_manager.conn.cursor()
    cursor.execute("UPDATE users SET car = ? WHERE user_id = ? AND platform = ?", (status, user_id, platform))
    db_manager.conn.commit()
    return text_response('车牌转发设置成功')


def set_default_server(platform, user_id, text):
    print(text)
    for i in text.strip().split(' '):
        if server_exists(r_ := query_server_info(i)) is False:
            return text_response(f'未找到服务器 {i}')
    default_server = convert_server_names_to_indices(text)
    get_user_data(platform, user_id)
    cursor = db_manager.conn.cursor()
    cursor.execute("UPDATE users SET default_server = ? WHERE user_id = ? AND platform = ?",
                   (json.dumps(default_server), user_id, platform))
    db_manager.conn.commit()
    return text_response(f'默认服务器设置为 {text}')


def set_server_mode(platform, user_id, text):

    server = int(convert_server_names_to_indices(text)[0]) if convert_server_names_to_indices(text) else None
    if server is None:
        return text_response(f'未找到名为 {text} 的服务器信息')
    get_user_data(platform, user_id)
    cursor = db_manager.conn.cursor()
    cursor.execute("UPDATE users SET server_mode = ? WHERE user_id = ? AND platform = ?",
                   (server, user_id, platform))
    db_manager.conn.commit()
    return text_response(f'服务器模式设置为 {text}')


def bind_player_request(platform: str, user_id: str):

    cursor = db_manager.conn.cursor()
    data = get_user_data(platform, user_id)

    bind_count = len(json.loads(data['data']['game_ids']))

    def generate_verify_code():
        while True:
            verify_code = random.randint(10000, 99999)
            if '64' not in str(verify_code) and '89' not in str(verify_code):
                return verify_code
    # 不包含64和89的随机数

    verify_code = generate_verify_code()
    # verify_code = "000000"
    rpl_true = f'正在绑定第{bind_count + 1}个记录，请将 评论(个性签名) 或者 当前使用的 乐队编队名称改为\n{verify_code}\n稍等片刻等待同步后，发送\n验证 玩家ID 来完成本次身份验证\n例如：验证 10000xxxx 国服'
    # 存入verify_code
    cursor.execute("UPDATE users SET verify_code = ? WHERE user_id = ? AND platform = ?", (verify_code, user_id, platform))
    db_manager.conn.commit()
    return text_response(rpl_true)


def unbind_player_request(platform: str, user_id: str):

     data = get_user_data(platform, user_id)
     record = json.loads(data['data']['game_ids'])
     if not record:
         return text_response('未找到绑定记录')

     return text_response(f'当前有 {len(record)} 个记录，发送"解除绑定 {len(record)}"来获解除第{len(record)}个记录，以此类推')


def bind_player_verification(platform: str, user_id: str, server: int | None, player_id: str, bind_type: bool):

    cursor = db_manager.conn.cursor()
    # 先检查verify_code是否正确
    # 使用 get
    user_data = get_user_data(platform, user_id)
    verify_code = user_data['data']['verify_code']

    if server is None:
        server = user_data['data']['server_mode']
    if verify_code == "" or not verify_code:
        return text_response('请先获取验证代码')
    # 检测重复性
    game_ids = json.loads(user_data['data']['game_ids'])
    for i in game_ids:
        if i.get("game_id") == player_id and i.get("server") == server:
            return text_response('请勿重复绑定')
    server_s_name = config.server_index_to_s_name[str(server)]

    # 构建 URL
    url = f'https://bestdori.com/api/player/{server_s_name}/{player_id}?mode=2'
    if config.verify_player_bind_use_proxy:
        http = urllib3.ProxyManager(config.proxy_url, cert_reqs='CERT_NONE')
    else:
        http = urllib3.PoolManager(cert_reqs='CERT_NONE')
    # 发送请求
    response = http.request('GET', url)
    # 检查响应的状态码是否为 200
    if response.status == 200:
        # 解析 JSON 响应数据
        data = json.loads(response.data.decode('utf-8'))
    else:
        logger.error(f"获取玩家数据失败，HTTP响应码: {response.status}")
        return None

    if data.get("data").get("profile") is None or data.get("profile") == {}:
        return text_response('玩家ID不存在，请检查输入，或服务器是否对应')
    introduction = data.get("data", {}).get("profile", {}).get("introduction")
    deck_name = data.get("data", {}).get("profile", {}).get("mainUserDeck", {}).get("deckName")
    if verify_code != introduction and verify_code != deck_name:
        return text_response('验证失败，签名或者乐队编队名称与验证代码不匹配喵，可以检查后再次尝试(无需重复发送绑定玩家)')
    # 验证成功
    game_ids = json.loads(user_data['data']['game_ids'])
    game_ids.append({"game_id": player_id, "server": server})
    cursor.execute("UPDATE users SET game_ids = ? WHERE user_id = ? AND platform = ?",
                   (json.dumps(game_ids), user_id, platform))  # 存入game_ids
    cursor.execute("UPDATE users SET verify_code = ? WHERE user_id = ? AND platform = ?",
                   ("", user_id, platform))  # 清空verify_code
    db_manager.conn.commit()
    return text_response('绑定成功！现在可以使用"玩家状态"来查询玩家信息了')


def unbind_player_verification(platform: str, user_id: str, record: int | None):
    user_data = get_user_data(platform, user_id)

    cursor = db_manager.conn.cursor()

    # 先检查verify_code是否正确
    cursor.execute("SELECT * FROM users WHERE user_id = ? AND platform = ?", (user_id, platform))
    row = cursor.fetchone()

    if row:
        # 用户存在，解析game_ids字段
        game_ids = json.loads(user_data['data']['game_ids'])  # Convert JSON string to list

        if record and 1 <= record <= len(game_ids):  # 如果record是一个有效的索引
            # 将record从1-based转换为0-based索引
            index = record - 1

            # 删除指定索引的记录
            del game_ids[index]

            # 将更新后的game_ids列表转换回JSON字符串
            updated_game_ids_json = json.dumps(game_ids)

            # 更新数据库中的game_ids字段
            cursor.execute("UPDATE users SET game_ids = ? WHERE user_id = ? AND platform = ?", (updated_game_ids_json, user_id, platform))
            db_manager.conn.commit()
            return text_response('解绑成功喵')
        return text_response(f'解绑失败，当前有 {record} 个记录，发送"解除绑定 {record}"来获解除第{record}个记录，以此类推')
    return text_response('解绑失败，请检查输入是否正确')


def help_command(command_name=None):
    if not command_name:
        # 读取 config.help_doc_dict 中的所有键
        command_list = list(config.help_doc_dict.keys())
        command_list.sort()
        print(command_list)
        return text_response(f'当前支持的命令有：\n{", ".join(command_list)}\n 请使用"help 命令名"来查看命令的详细帮助')
    else:
        # 读取 config.help_doc_dict 中的指定键
        help_text = config.help_doc_dict.get(command_name)
        if help_text:
            return text_response(help_text)
        return None


class Remote:
    @staticmethod
    def get_user_data(platform: str, user_id: str):
        data = {
            'platform': platform,
            'user_id': user_id
        }
        result = requests_post_for_user(f"{config.user_data_backend}/user/getUserData", data)
        return result

    @staticmethod
    def bind_player_request(platform: str, user_id: str, server: int, bind_type: bool):
        data = {
            'platform': platform,
            'user_id': user_id,
            'server': server,
            'bindType': bind_type  # 布尔，表示绑定还是解绑
        }
        result = requests_post_for_user(f"{config.user_data_backend}/user/bindPlayerRequest", data)
        return result

    @staticmethod
    def bind_player_verification(platform: str, user_id: str, server: int, player_id: str, bind_type: bool):
        data = {
            'platform': platform,
            'user_id': user_id,
            'server': server,
            'playerId': player_id,
            'bindType': bind_type  # 布尔，表示绑定还是解绑
        }
        result = requests_post_for_user(f"{config.user_data_backend}/user/bindPlayerVerification", data)
        return result

    @staticmethod
    def player_status(user_id, platform, server=None):
        user_data = Remote.get_user_data(platform, user_id)
        if user_data['status'] != 'success':
            return text_response('获取用户数据失败')
        if server is None:
            server = user_data['data']['server_mode']
        player_id = user_data['data']['server_list'][server]['playerId']
        if player_id == 0:
            return text_response(f'未绑定玩家，请使用 绑定玩家 进行绑定')
        return v2api_from_backend('player', str(player_id), server=server)

    @staticmethod
    def set_car_forward(platform, user_id, status):
        data = {
            'platform': platform,
            'user_id': user_id,
            'status': status
        }
        result = requests_post_for_user(f"{config.user_data_backend}/user/changeUserData/setCarForwarding", data)
        return result

    @staticmethod
    def set_default_server(platform, user_id, text):
        data = {
            'platform': platform,
            'user_id': user_id,
            'text': text
        }
        result = requests_post_for_user(f"{config.user_data_backend}/user/changeUserData/setDefaultServer", data)
        return result

    @staticmethod
    def set_server_mode(platform, user_id, text):
        data = {
            'platform': platform,
            'user_id': user_id,
            'text': text
        }
        result = requests_post_for_user(f"{config.user_data_backend}/user/changeUserData/setServerMode", data)
        return result


