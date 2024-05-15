from typing import List, Union, Dict, Optional
from ..config import config
import tsugu_api
from loguru import logger
import time
from tsugu_api._typing import _ServerId


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


def text_response(string):
    return [{"type": "string", "string": string}]


def server_names_2_server_ids(server_name: List[str]) -> List[_ServerId]:
    return [config._s_i[code] for code in server_name]


def server_name_2_server_id(server_name: str) -> _ServerId:
    return config._s_i[server_name] if server_name in config._s_i else None


def server_ids_2_server_names(index: List[_ServerId]) -> List[str]:
    return [config._i_s[code] for code in index]


def server_id_2_server_name(index: _ServerId) -> str:
    return config._i_s[index] if index in config._i_s else None


def server_exists(server):
    if server or server == 0:
        return True
    if not server:
        return False
    return False


def get_user(user_id: str, platform: str) -> Optional[User]:

    for i in range(0, config.get_remote_user_data_max_retry):
        try:
            user_data_res = tsugu_api.get_user_data(platform, user_id)
            if user_data_res.get('status') == 'failed':
                return None
            break
        except Exception as e:
            logger.error(f'Error: {e}')
            time.sleep(0.5)
            continue
    else:
        return None

    # 旧数据兼容
    user_data = user_data_res.get('data')
    if user_data.get('game_ids') is None:

        user_data['game_ids'] = []
        for i in range(0, 5):
            if user_data.get('server_list')[i]['playerId'] != 0:# type: ignore
                new_game_id = {"game_id": user_data.get('server_list')[i]['playerId'], "server": i}# type: ignore
                user_data['game_ids'].append(new_game_id)# type: ignore
        verify_code_all = []
        for i in range(0, 5):
            if user_data.get('server_list')[i].get('verifyCode') is not None:
                verify_code_all.append(i)
        # 有一说一，下面这行没有实际意义
        user_data['verify_code'] = '或'.join([str(user_data.get('server_list')[i].get('verifyCode')) for i in verify_code_all]) if len(verify_code_all) > 1 else verify_code_all[0] if verify_code_all else ''

    # 构建用户对象
    user = User(user_id=user_id,
                platform=platform,
                server_mode=user_data.get('server_mode'),# type: ignore
                default_server=user_data.get('default_server'),# type: ignore
                car=user_data.get('car'),# type: ignore
                server_list=user_data.get('server_list', None),# type: ignore
                game_ids=user_data.get('game_ids', []),# type: ignore
                verify_code=user_data.get('verify_code'))# type: ignore
    return user


