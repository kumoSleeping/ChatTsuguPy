import typing
import re
import json
import urllib3
from urllib3.exceptions import HTTPError
from loguru import logger

from ..config import config


def text_response(string):
    return [{"type": "string", "string": string}]


def convert_server_names_to_indices(server_names: str) -> list:
    indices_list = [config._server_name_to_index.get(name, "Unknown") for name in server_names.split(" ")]
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


def v2api_from_backend(api, text, default_servers: typing.List[int] = None, server=3):
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


