import time

from ..utils import server_exists, text_response, config
from ..command_matcher import match_command
from ..universal import universal_api_handler

from . import router
from ..user_data import remote_db


def remote_api_handler(user_id: str, message: str,  platform: str, channel_id: str):
    for i in config.user_commands:
        if res := match_command(message, commands=i['command_name']):
            api = i['api']
            user = remote_db.get_user(user_id, platform)
            return router.api_handler(user, res, api, platform, channel_id)

    return None


def handler(message: str, user_id: str, platform: str, channel_id: str):
    # 进行 api 命令匹配
    result = universal_api_handler(user_id, message, platform, channel_id, loacl=False)
    if result:
        return result

    # 远程命令
    result = remote_api_handler(user_id, message, platform, channel_id)
    if result:
        return result

