import typing
import re
import json
import urllib3
from urllib3.exceptions import HTTPError
from loguru import logger
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
    def __init__(self, user_id: str, platform: str, server_mode: _ServerId, default_server: List[_ServerId], car: bool, server_list: list, game_ids: dict, verify_code: str):
        super().__init__(user_id, platform, server_mode, default_server, car, server_list)
        self.game_ids = game_ids
        self.verify_code = verify_code


def text_response(string):
    return [{"type": "string", "string": string}]


def convert_server_names_to_indices(server_names: str) -> typing.List[_ServerId]:
    '''
    将服务器名称转化为索引
    例如 "cn jp" -> [0, 1]
    如果其中存在未知服务器，会无视
    如果参数为空，返回 None
    :param server_names:
    :return:
    '''
    indices_list = [config._server_name_to_index.get(name, "Unknown") for name in server_names.split(" ")]
    result = [index for index in indices_list if index != "Unknown"]
    # 转化成数字，例如 ["0", "1"] -> [0, 1]
    return [int(i) for i in result]


def convert_server_name_to_index(server_name: str) -> typing.Optional[_ServerId]:
    '''
    把服务器名称转化为索引
    如果其中存在未知服务器，会无视
    如果参数多余，会无视
    如果参数为空，返回 None
    :param server_name:
    :return:
    '''
    server = convert_server_names_to_indices(server_name)[0] if convert_server_names_to_indices(server_name) else None
    return server


def ns_2_is(server_name: list) -> list:
    return [config._s_i[code] for code in server_name]

def is_2_ns(index: list) -> list:
    return [config._i_s[code] for code in index]

def n_2_i(server_name: str) -> int:
    return config._s_i[server_name] if server_name in config._s_i else None

def i_2_n(index: int) -> str:
    return config._i_s[index] if index in config._i_s else None

def server_exists(server):
    if server or server == 0:
        return True
    if not server:
        return False
    return False


def load_commands_from_config(data):
    # 初始化一个空字典来存储命令到操作的映射
    cmd_dict = {}
    for item in data:
        api = item['api']
        for command_name in item['command_name']:
            cmd_dict[command_name] = api
    return cmd_dict


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


