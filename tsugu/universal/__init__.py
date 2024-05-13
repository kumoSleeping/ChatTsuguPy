import typing
import re
import json
import urllib3
from urllib3.exceptions import HTTPError
from loguru import logger
import tsugu_api

from ..utils import User
from ..command_matcher import match_command

from ..config import config

from tsugu_api._typing import _ServerId
from . import router


def universal_api_handler(user: User, message: str,  platform: str, channel_id: str):
    for i in config.commands:
        if res := match_command(message, commands=i['command_name']):
            #             {"api": "get_card_illustration", "command_name": ["查插画", "查卡面"]},
            api = i['api']
            logger.info(f'调用 {api} 的 handler')
            return router.api_handler(user, res, api, platform, channel_id)

    return None


