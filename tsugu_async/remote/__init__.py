import time

from ..utils import server_exists, text_response, config
from ..command_matcher import match_command
from ..universal import universal_api_handler

from . import router
from ..user_data import remote_db


async def remote_api_handler(user_id: str, message: str,  platform: str, channel_id: str):
    for i in config.user_commands:
        if res := match_command(message, commands=i['command_name']):
            api = i['api']
            user = await remote_db.get_user(user_id, platform)
            return await router.api_handler(user, res, api, platform, channel_id)

    return None


async def handler(message: str, user_id: str, platform: str, channel_id: str):
    # 进行 api 命令匹配
    result = await universal_api_handler(user_id, message, platform, channel_id)
    if result:
        return result

    # 远程命令
    result = await remote_api_handler(user_id, message, platform, channel_id)
    if result:
        return result

