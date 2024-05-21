import typing
from typing import List
import tsugu_api
import tsugu_api_async
from loguru import logger
import time

from tsugu_api_core._typing import _ServerId


_i_s = {0: "jp", 1: "en", 2: "tw", 3: "cn", 4: "kr"}
_s_i = {"jp": 0, "en": 1, "tw": 2, "cn": 3, "kr": 4}


def text_response(string):
    return [{"type": "string", "string": str(string)}]


def server_names_2_server_ids(server_name: List[str]) -> List[_ServerId]:
    return [_s_i[code] for code in server_name]


def server_name_2_server_id(server_name: str) -> _ServerId:
    return _s_i[server_name] if server_name in _s_i else None


def server_ids_2_server_names(index: List[_ServerId]) -> List[str]:
    return [_i_s[code] for code in index]


def server_id_2_server_name(index: _ServerId) -> str:
    return _i_s[index] if index in _i_s else None


def server_exists(server):
    if server or server == 0:
        return True
    if not server:
        return False
    return False


class User:
    def __init__(self, user_id: str, platform: str, server_mode: _ServerId, default_server: List[_ServerId], car: bool, server_list: list, game_ids: list, verify_code: str):
        self.user_id: str = user_id
        self.platform: str = platform
        self.server_mode: _ServerId = server_mode
        self.default_server: List[_ServerId] = default_server
        self.car: bool = car
        self.server_list: list = server_list
        self.game_ids = game_ids
        self.verify_code = verify_code


def get_user(user_id: str, platform: str) -> User:
    '''
    获取用户数据
    多次尝试获取用户数据
    兼容旧版用户数据

    :param user_id:
    :param platform:
    :return:
    '''
    for i in range(0, 3):
        try:
            user_data_res = tsugu_api.get_user_data(platform, user_id)
            if user_data_res.get('status') == 'failed':
                return text_response(user_data_res.get('data'))
            break
        except Exception as e:
            logger.error(f'Error: {e}')
            time.sleep(0.8)
            continue
    else:
        raise Exception('获取用户数据失败')

    # 获取用户数据失败
    if user_data_res.get('status') == 'failed':
        return text_response(user_data_res.get('data'))
    # 构建用户对象
    user_data = user_data_res.get('data')

    if user_data.get('game_ids') is None:

        user_data['game_ids'] = []
        for i in range(0, 5):
            if user_data.get('server_list')[i]['playerId'] != 0:
                new_game_id = {"game_id": user_data.get('server_list')[i]['playerId'], "server": i}
                user_data['game_ids'].append(new_game_id)
        verify_code_all = []
        for i in range(0, 5):
            if user_data.get('server_list')[i].get('verifyCode') is not None:
                verify_code_all.append(i)

    user = User(user_id=user_id,
                platform=platform,
                server_mode=user_data.get('server_mode'),
                default_server=user_data.get('default_server'),
                car=user_data.get('car'),
                server_list=user_data.get('server_list', None),
                game_ids=user_data.get('game_ids', []),
                verify_code=user_data.get('verify_code'))
    return user


async def get_user_async(user_id: str, platform: str) -> User:
    '''
    获取用户数据
    多次尝试获取用户数据
    兼容旧版用户数据
W
    :param user_id:
    :param platform:
    :return:
    '''
    for i in range(0, 3):
        try:
            user_data_res = await tsugu_api_async.get_user_data(platform, user_id)
            if user_data_res.get('status') == 'failed':
                return text_response(user_data_res.get('data'))
            break
        except Exception as e:
            logger.error(f'Error: {e}')
            time.sleep(0.8)
            continue
    else:
        raise Exception('获取用户数据失败')

    # 获取用户数据失败
    if user_data_res.get('status') == 'failed':
        return text_response(user_data_res.get('data'))
    # 构建用户对象
    user_data = user_data_res.get('data')

    if user_data.get('game_ids') is None:

        user_data['game_ids'] = []
        for i in range(0, 5):
            if user_data.get('server_list')[i]['playerId'] != 0:
                new_game_id = {"game_id": user_data.get('server_list')[i]['playerId'], "server": i}
                user_data['game_ids'].append(new_game_id)
        verify_code_all = []
        for i in range(0, 5):
            if user_data.get('server_list')[i].get('verifyCode') is not None:
                verify_code_all.append(i)

    user = User(user_id=user_id,
                platform=platform,
                server_mode=user_data.get('server_mode'),
                default_server=user_data.get('default_server'),
                car=user_data.get('car'),
                server_list=user_data.get('server_list', None),
                game_ids=user_data.get('game_ids', []),
                verify_code=user_data.get('verify_code'))
    return user


