import base64
from typing import List, Union, Dict
import tarina

from .utils import *
from loguru import logger
from . import src


def handler(message: str, user_id: str, platform: str) -> List[Union[bytes, str]]:
    '''
    Tsugu Handler
    处理用户输入的自然语言，返回处理后的结果

    :param message: 用户消息
    :param user_id: 用户ID
    :param platform: 平台名称 一般为 red
    :return: List[Union[bytes, str]]
    '''
    try:
        data = handler_raw(message, user_id, platform)
        response = []
        if not data:
            return response
        for item in data:
            response.append(item['string']) if item['type'] == 'string' else None
            response.append(base64.b64decode(item['string'].encode('utf-8')) if item['type'] == 'base64' else None)
        return response
    except Exception as e:
        raise e


def handler_raw(message: str, user_id: str, platform: str) -> List[Dict[str, str]]:
    '''
    handler_raw 除了返回的数据类型不同外，其他与 handler 函数一致
    返回格式为 Tsugu 标准数据格式
    :param message: 用户消息
    :param user_id: 用户ID
    :param platform: 平台名称 一般为 red
    :return: List[Dict[str, str]]
    '''
    try:
        return r if (r := src.handler(message, user_id, platform)) else None
    except Exception as e:
        logger.error(f'Error: {e}')
        raise e


async def handler_async(message: str, user_id: str, platform: str) -> List[Union[bytes, str]]:
    '''
    Tsugu Handler Async
    异步支持
    处理用户输入的自然语言，返回处理后的结果

    :param message: 用户消息
    :param user_id: 用户ID
    :param platform: 平台名称 一般为 red
    :return: List[Union[bytes, str]]
    '''
    try:
        data = await handler_raw_async(message, user_id, platform)
        response = []
        if not data:
            return response
        for item in data:
            response.append(item['string']) if item['type'] == 'string' else None
            response.append(base64.b64decode(item['string'].encode('utf-8')) if item['type'] == 'base64' else None)
        return response
    except Exception as e:
        raise e


async def handler_raw_async(message: str, user_id: str, platform: str) -> List[Dict[str, str]]:
    '''
    handler_raw_async 除了返回的数据类型不同外，其他与 handler_async 函数一致
    返回格式为 Tsugu 标准数据格式
    :param message: 用户消息
    :param user_id: 用户ID
    :param platform: 平台名称 一般为 red
    :return: List[Dict[str, str]]
    '''
    try:
        return r if (r := await src.handler_async(message, user_id, platform)) else None
    except Exception as e:
        logger.error(f'Error: {e}')
        raise e


