from ..utils import server_exists, text_response, config, UserLocal

from ..universal import universal_api_handler
from ..utils import text_response, server_exists
from ..command_matcher import match_command
from . import router
from ..storage import db
from tsugu_api._typing import _ServerId
import json


def local_api_handler(user_id: str, message: str,  platform: str, channel_id: str):
    for i in config.user_commands:
        if res := match_command(message, commands=i['command_name']):
            user = db.get_user(user_id, platform)
            api = i['api']
            return router.api_handler(user, res, api, platform, channel_id)

    return None


def handler(message, user_id, platform, channel_id):
    # 进行 api 命令匹配
    result = universal_api_handler(user_id, message, platform, channel_id, local=True)
    if result:
        return result

    # 远程命令
    result = local_api_handler(user_id, message, platform, channel_id)
    if result:
        return result

    return None
