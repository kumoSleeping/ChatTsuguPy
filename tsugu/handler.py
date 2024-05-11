import base64
from typing import List, Union, Dict

from .universal_utils import *
from .universal_utils import text_response
from . import remote
from . import local
from .universal_utils import config


def handler(message: str, user_id: str, platform: str, channel_id: str) -> List[Union[bytes, str]]:
    '''
    Tsugu Handler
    处理用户输入的自然语言，返回处理后的结果

    :param message: 用户消息
    :param user_id: 用户ID
    :param platform: 平台名称 一般为 red
    :param channel_id: 频道ID / 群号
    :return: List[Union[bytes, str]]
    '''
    data = handler_old(message, user_id, platform, channel_id)
    response = []
    if not data:
        return response
    for item in data:
        if item['type'] == 'string':
            response.append(item['string'])
        elif item['type'] == 'base64':
            bytes_data = base64.b64decode(item['string'].encode('utf-8'))
            response.append(bytes_data)
    return response


def handler_old(message: str, user_id: str, platform: str, channel_id: str) -> List[Dict[str, str]]:
    '''
    old 除了返回的数据类型不同外，其他与 handler 函数一致
    返回格式为 Tsugu 标准数据格式
    :param message: 用户消息
    :param user_id: 用户ID
    :param platform: 平台名称 一般为 red
    :param channel_id: 频道ID / 群号
    :return: List[Dict[str, str]]
    '''
    try:
        def tsugu_handler(message: str, user_id: str, platform: str, channel_id: str):
            message = message.strip()
            # help
            if config.features.get('help', True):
                if message.startswith('帮助'):
                    return help_command()
                if message.startswith('help'):
                    arg_text = message[4:].strip()
                    return help_command(arg_text)
                if message.endswith('-h'):
                    arg_text = message[:-2].strip()
                    return help_command(arg_text)
            # 如果启用了本地数据库
            if config._user_database_path:
                return local.handler(message, user_id, platform, channel_id)
            # 否则使用远程服务器
            else:
                return remote.handler(message, user_id, platform, channel_id)
        data = tsugu_handler(message, user_id, platform, channel_id)
        if not data:
            return []
        return data
    except Exception as e:
        logger.error(f'Error: {e}')
        raise e




