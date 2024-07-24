import typing
from typing import List
import tsugu_api
import tsugu_api_async
from loguru import logger
import time

from tsugu_api_core._typing import _ServerId, _UserPlayerInList

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


def get_user_account_list_msg(user) -> str:
    def mask_data(game_id: str):
        game_id = str(game_id)
        if len(game_id) < 6:
            return game_id[:3] + '*' * (len(game_id) - 3)
        elif len(game_id) < 3:
            return '*' * len(game_id)
        else:
            game_id = game_id[:3] + '*' * (len(game_id) - 6) + game_id[-3:]
        return game_id

    bind_record = '\n'.join(
        [f'{i + 1}. {mask_data(str(x.get("playerId")))} {server_id_2_server_name(x.get("server"))}' for i, x in
         enumerate(user.user_player_list)])

    return bind_record

class User:
    def __init__(self, user_id: str, platform: str, main_server: _ServerId, displayed_server_list: List[_ServerId],
                 share_room_number: bool, user_player_index: int, user_player_list: List[_UserPlayerInList]):
        self.user_id = user_id
        self.platform = platform
        self.main_server = main_server
        self.displayed_server_list = displayed_server_list
        self.share_room_number = share_room_number
        self.user_player_index = user_player_index
        self.user_player_list = user_player_list


def get_user(user_id: str, platform: str) -> User:
    '''
    获取用户数据
    多次尝试获取用户数据
    兼容旧版用户数据

    :param user_id:
    :param platform:
    :return:
    '''
    for i in range(3):
        try:
            user_data_res = tsugu_api.get_user_data(platform, user_id)
            user_data = user_data_res.get('data')
            user = User(user_id=user_id,
                        platform=platform,
                        main_server=user_data.get('mainServer'),
                        displayed_server_list=user_data.get('displayedServerList'),
                        share_room_number=user_data.get('shareRoomNumber'),
                        user_player_index=user_data.get('userPlayerIndex'),
                        user_player_list=user_data.get('userPlayerList'))
            return user
        except TimeoutError:
            time.sleep(0.2)
            continue
        except Exception as e:
            logger.error(f'Error: {e}')
            raise e


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
    for i in range(3):
        try:
            user_data_res = await tsugu_api_async.get_user_data(platform, user_id)
            user_data = user_data_res.get('data')
            user = User(user_id=user_id,
                        platform=platform,
                        main_server=user_data.get('mainServer'),
                        displayed_server_list=user_data.get('displayedServerList'),
                        share_room_number=user_data.get('shareRoomNumber'),
                        user_player_index=user_data.get('userPlayerIndex'),
                        user_player_list=user_data.get('userPlayerList'))
            return user
        except TimeoutError:
            time.sleep(0.2)
            continue
        except Exception as e:
            logger.error(f'Error: {e}')
            raise e


