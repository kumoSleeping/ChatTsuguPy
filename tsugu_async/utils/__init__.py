import typing
from typing import List

from ..config import config

from tsugu_api._typing import _ServerId


class User:
    def __init__(self, user_id: str, platform: str, server_mode: _ServerId, default_server: List[_ServerId], car: bool, server_list: list):
        self.user_id: str = user_id
        self.platform: str = platform
        self.server_mode: _ServerId = server_mode
        self.default_server: List[_ServerId] = default_server
        self.car: bool = car
        self.server_list: list = server_list


class UserLocal(User):
    def __init__(self, user_id: str, platform: str, server_mode: _ServerId, default_server: List[_ServerId], car: bool, server_list: list, game_ids: list, verify_code: str):
        super().__init__(user_id, platform, server_mode, default_server, car, server_list)
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




