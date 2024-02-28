import requests
import re
from .config import tsugu_config


def text_response(string):
    return [{"type": "string", "string": string}]


def server_exists(server):
    if server or server == 0:
        return True
    return False


def requests_post(url, data):
    try:
        if tsugu_config.use_proxies:
            response = requests.post(url, json=data, proxies=tsugu_config.proxies)
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
    result = requests_post(f"{tsugu_config.user_data_backend}/user/getUserData", data)
    return result


def bind_player_request(platform: str, user_id: str, server: int, bind_type: bool):
    data = {
        'platform': platform,
        'user_id': user_id,
        'server': server,
        'bindType': bind_type  # 布尔，表示绑定还是解绑
    }
    result = requests_post(f"{tsugu_config.user_data_backend}/user/bindPlayerRequest", data)
    return result


def bind_player_verification(platform: str, user_id: str, server: int, player_id: str, bind_type: bool):
    data = {
        'platform': platform,
        'user_id': user_id,
        'server': server,
        'playerId': player_id,
        'bindType': bind_type  # 布尔，表示绑定还是解绑
    }
    result = requests_post(f"{tsugu_config.user_data_backend}/user/bindPlayerVerification", data)
    return result


def v2api_from_backend(api, text, default_servers=None, server=3):
    if default_servers is None:
        default_servers = [3, 0]
    path = f"/v2/{api}"
    data = {
        "default_servers": default_servers,
        "server": server,
        "text": text,
        "useEasyBG": tsugu_config.use_easy_bg,
        "compress": tsugu_config.compress
    }
    res = requests_post(f"{tsugu_config.backend}{path}", data)
    return res


def v2_api_command(message, command_matched, api, platform, user_id, channel_id):
    text = message[len(command_matched):].strip()

    # print(f"command: {command_matched}, api: {api}, text: {text}")
    if tsugu_config.use_default_server:
        # 使用默认服务器列表
        return v2api_from_backend(api, text)

    if api in ['cardIllustration', 'ycm']:  # 无需验证server信息
        return v2api_from_backend(api, text)

    if api == 'gachaSimulate':
        if channel_id in tsugu_config.ban_gacha_simulate_group_data:
            return text_response('此群禁止使用模拟抽卡功能')

    # 获取用户数据
    user_data = get_user_data(platform, user_id)
    # print(user_data)
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
        return text_response(f'未绑定玩家，请使用 绑定玩家 {tsugu_config.server_list[server]} 进行绑定')
    return v2api_from_backend('player', str(player_id), server=server)


def set_car_forward(platform, user_id, status):
    data = {
        'platform': platform,
        'user_id': user_id,
        'status': status
    }
    result = requests_post(f"{tsugu_config.user_data_backend}/user/changeUserData/setCarForwarding", data)
    return result


def set_default_server(platform, user_id, text):
    data = {
        'platform': platform,
        'user_id': user_id,
        'text': text
    }
    result = requests_post(f"{tsugu_config.user_data_backend}/user/changeUserData/setDefaultServer", data)
    return result


def set_server_mode(platform, user_id, text):
    data = {
        'platform': platform,
        'user_id': user_id,
        'text': text
    }
    result = requests_post(f"{tsugu_config.user_data_backend}/user/changeUserData/setServerMode", data)
    return result


def submit_car_number_msg(message, user_id, platform):
    # 检查car_config['car']中的关键字
    for keyword in tsugu_config.car_config["car"]:
        if str(keyword) in message:
            break
    else:
        return False
    # 检查car_config['fake']中的关键字
    for keyword in tsugu_config.car_config["fake"]:
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
        url = f"https://api.bandoristation.com/index.php?function=submit_room_number&number={car_id}&user_id={user_id}&raw_message={message}&source={tsugu_config.token_name}&token={tsugu_config.bandori_station_token}"
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


def load_commands_from_config(data):
    # 初始化一个空字典来存储命令到操作的映射
    cmd_dict = {}
    for item in data:
        action = item['action']
        for key in item['keys']:
            cmd_dict[key] = action
    return cmd_dict


def query_server_info(msg):
    # print(f"请求服务器信息: {msg}")
    try:
        # 假设 _post 是已定义的发送POST请求的函数
        r = requests_post(tsugu_config.utils_backend + '/v2/utils', {'text': msg})
        if [{'type': 'string', 'string': '发生异常'}] == r:
            return None
        if not r['servers']:
            return None
        server = r['servers'][0]
        # 根据需要处理并返回服务器信息
        return server  # 或者根据需要格式化返回的信息
    except Exception as e:
        raise e

