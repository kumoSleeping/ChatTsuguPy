from ...universal_utils import requests_post_for_user
from ...universal_utils import config
from ...universal_utils import text_response
from ...universal_utils import v2api_from_backend

import urllib3
import re
from loguru import logger


def v2_api_command(message, command_matched, api, platform, user_id, channel_id):
    text = message[len(command_matched):].strip()

    if api in ['cardIllustration', 'ycm']:  # 无需验证server信息
        return v2api_from_backend(api, text)

    if api == 'gachaSimulate':
        if channel_id in config.ban_gacha_simulate_group_data:
            return text_response('此群禁止使用模拟抽卡功能')

    # 获取用户数据
    # logger.debug(config._user_database_path)
    user_data = get_user_data(platform, user_id)
    try:
        if user_data['status'] != 'success':
            return text_response('获取用户数据失败：内部错误')
        return v2api_from_backend(api, text, user_data['data']['default_server'], user_data['data']['server_mode'])
    except Exception as e:
        return text_response('获取用户数据失败：网络错误')


def get_user_data(platform: str, user_id: str):
    data = {
        'platform': platform,
        'user_id': user_id
    }
    result = requests_post_for_user(f"{config.user_data_backend}/user/getUserData", data)
    logger.debug(result)
    return result


def bind_player_request(platform: str, user_id: str, server: int, bind_type: bool):
    data = {
        'platform': platform,
        'user_id': user_id,
        'server': server,
        'bindType': bind_type  # 布尔，表示绑定还是解绑
    }
    result = requests_post_for_user(f"{config.user_data_backend}/user/bindPlayerRequest", data)
    return result


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


def player_status(user_id, platform, server=None):
    user_data = get_user_data(platform, user_id)
    if user_data['status'] != 'success':
        return text_response('获取用户数据失败')
    if server is None:
        server = user_data['data']['server_mode']
    player_id = user_data['data']['server_list'][server]['playerId']
    if player_id == 0:
        return text_response(f'未绑定玩家，请使用 绑定玩家 进行绑定')
    return v2api_from_backend('player', str(player_id), server=server)


def set_car_forward(platform, user_id, status):
    data = {
        'platform': platform,
        'user_id': user_id,
        'status': status
    }
    result = requests_post_for_user(f"{config.user_data_backend}/user/changeUserData/setCarForwarding", data)
    return result


def set_default_server(platform, user_id, text):
    data = {
        'platform': platform,
        'user_id': user_id,
        'text': text
    }
    result = requests_post_for_user(f"{config.user_data_backend}/user/changeUserData/setDefaultServer", data)
    return result


def set_server_mode(platform, user_id, text):
    data = {
        'platform': platform,
        'user_id': user_id,
        'text': text
    }
    result = requests_post_for_user(f"{config.user_data_backend}/user/changeUserData/setServerMode", data)
    return result


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
            user_data = get_user_data(platform, user_id)
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
