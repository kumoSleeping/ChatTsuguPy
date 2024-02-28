import requests
import re
import yaml
import os


def load_yaml(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file)
        return data


# 获取当前文件夹，组合config.yaml的路径
config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')


# 从config.yaml中加载配置
config = load_yaml(config_path)
USER_DATA_BACKEND = config['USER_DATA_BACKEND']
useEasyBG = config['useEasyBG']
compress = config['compress']
BACKEND = config['BACKEND']
TOKEN_NAME = config['TOKEN_NAME']
BANDORI_STATION_TOKEN = config['BANDORI_STATION_TOKEN']
car_config = config['car_config']
UTILS_BACKEND = config['UTILS_BACKEND']
USE_PROXIES = config['USE_PROXIES']
PROXIES = config['PROXIES']
server_list = config['server_list']
BAN_GACHA_SIMULATE_GROUP_DATA = config['BAN_GACHA_SIMULATE_GROUP_DATA']
USE_DEFAULT_SERVER = config['USE_DEFAULT_SERVER']


def text_response(string):
    return [{"type": "string", "string": string}]


def server_exists(server):
    if server or server == 0:
        return True
    return False


def requests_post(url, data):
    try:
        if USE_PROXIES:
            response = requests.post(url, json=data, proxies=PROXIES)
        else:
            response = requests.post(url, json=data)
        return response.json()
    except Exception as e:
        print(f"发生异常: {e}")
        return text_response("发生异常")


def get_user_data(platform: str, user_id: str):
    data = {
        'platform': platform,
        'user_id': user_id
    }
    result = requests_post(f"{USER_DATA_BACKEND}/user/getUserData", data)
    return result


def bind_player_request(platform: str, user_id: str, server: int, bind_type: bool):
    data = {
        'platform': platform,
        'user_id': user_id,
        'server': server,
        'bindType': bind_type  # 布尔，表示绑定还是解绑
    }
    result = requests_post(f"{USER_DATA_BACKEND}/user/bindPlayerRequest", data)
    return result


def bind_player_verification(platform: str, user_id: str, server: int, player_id: str, bind_type: bool):
    data = {
        'platform': platform,
        'user_id': user_id,
        'server': server,
        'playerId': player_id,
        'bindType': bind_type  # 布尔，表示绑定还是解绑
    }
    result = requests_post(f"{USER_DATA_BACKEND}/user/bindPlayerVerification", data)
    return result


def v2api_from_backend(api, text, default_servers=None, server=3):
    if default_servers is None:
        default_servers = [3, 0]
    path = f"/v2/{api}"
    data = {
        "default_servers": default_servers,
        "server": server,
        "text": text,
        "useEasyBG": useEasyBG,
        "compress": compress
    }
    res = requests_post(f"{BACKEND}{path}", data)
    return res


def v2_api_command(message, command_matched, api, platform, user_id, channel_id):
    text = message[len(command_matched):].strip()

    print(f"command: {command_matched}, api: {api}, text: {text}")
    if USE_DEFAULT_SERVER:
        # 使用默认服务器列表
        return v2api_from_backend(api, text)

    if api in ['cardIllustration', 'ycm']:  # 无需验证server信息
        return v2api_from_backend(api, text)

    if api == 'gachaSimulate':
        if channel_id in BAN_GACHA_SIMULATE_GROUP_DATA:
            return text_response('此群禁止使用模拟抽卡功能')

    # 获取用户数据
    user_data = get_user_data(platform, user_id)
    print(user_data)
    try:
        if user_data['status'] != 'success':
            return text_response('获取用户数据失败')
        return v2api_from_backend(api, text, user_data['data']['default_server'], user_data['data']['server_mode'])
    except:
        return text_response('获取用户数据失败')


def player_status(user_id, platform, server=None):
    user_data = get_user_data(platform, user_id)
    if user_data['status'] != 'success':
        return text_response('获取用户数据失败')
    if server is None:
        server = user_data['data']['server_mode']
    player_id = user_data['data']['server_list'][server]['playerId']
    if player_id == 0:
        return text_response(f'未绑定玩家，请使用 绑定玩家 {server_list[server]} 进行绑定')
    return v2api_from_backend('player', str(player_id), server=server)


def set_car_forward(platform, user_id, status):
    data = {
        'platform': platform,
        'user_id': user_id,
        'status': status
    }
    result = requests_post(f"{USER_DATA_BACKEND}/user/changeUserData/setCarForwarding", data)
    return result


def set_default_server(platform, user_id, text):
    data = {
        'platform': platform,
        'user_id': user_id,
        'text': text
    }
    result = requests_post(f"{USER_DATA_BACKEND}/user/changeUserData/setDefaultServer", data)
    return result


def set_server_mode(platform, user_id, text):
    data = {
        'platform': platform,
        'user_id': user_id,
        'text': text
    }
    result = requests_post(f"{USER_DATA_BACKEND}/user/changeUserData/setServerMode", data)
    return result


def submit_car_number_msg(message, user_id, platform):
    # 检查car_config['car']中的关键字
    for keyword in car_config["car"]:
        if str(keyword) in message:
            break
    else:
        return False
    # 检查car_config['fake']中的关键字
    for keyword in car_config["fake"]:
        if str(keyword) in message:
            return False
    pattern = r"^\d{5}(\D|$)|^\d{6}(\D|$)"
    if not re.match(pattern, message):
        return False
    # 获取用户数据
    user_data = get_user_data(platform, user_id)
    if not user_data['data']['car']:
        return True
    try:
        car_id = message[:6]
        if not car_id.isdigit() and car_id[:5].isdigit():
            car_id = car_id[:5]
        # 构建URL
        url = f"https://api.bandoristation.com/index.php?function=submit_room_number&number={car_id}&user_id={user_id}&raw_message={message}&source={TOKEN_NAME}&token={BANDORI_STATION_TOKEN}"
        # 发送请求
        response = requests.get(url)
        if response.status_code != 200:
            print(f"[Tsugu] 提交车牌失败，HTTP响应码: {response.status_code}")
            return True  # 虽然提交失败，但是确定了是车牌消息
        return True
    except Exception as e:
        print(f"[Tsugu] 发生异常: {e}")
        return True  # 虽然提交失败，但是确定了是车牌消息


def match_command(message, cmd_dict):
    for command, api_value in cmd_dict.items():
        if message.startswith(command):
            return command, api_value
    return None, None


def load_commands_from_yaml(data):
    # 初始化一个空字典来存储命令到操作的映射
    cmd_dict = {}
    for item in data['commands']:
        action = item['action']
        for key in item['keys']:
            cmd_dict[key] = action
    return cmd_dict


def query_server_info(msg):
    print(f"请求服务器信息: {msg}")
    try:
        # 假设 _post 是已定义的发送POST请求的函数
        r = requests_post(UTILS_BACKEND + '/v2/utils', {'text': msg})
        if [{'type': 'string', 'string': '发生异常'}] == r:
            return None
        if not r['servers']:
            return None
        server = r['servers'][0]
        # 根据需要处理并返回服务器信息
        return server  # 或者根据需要格式化返回的信息
    except Exception as e:
        raise e


def test(data):
    import base64
    from PIL import Image
    import io

    if not data:
        return text_response("无反馈数据")
    else:
        for item in data:
            if item["type"] == "string":
                e_message = item["string"]
                print(f"解释文字:\n{e_message}")
            elif item["type"] == "base64":
                # 处理Base64编码的图像数据
                base64_data = item["string"]
                # 解码Base64数据
                image_data = base64.b64decode(base64_data)
                # 输出MB字节大小
                print(f"图像大小: {len(image_data) / 1024:.2f}KB")
                # 将二进制数据转换为 PIL 图像对象
                image = Image.open(io.BytesIO(image_data))
                # 保存图像文件
                image.show()
            else:
                print(item)


