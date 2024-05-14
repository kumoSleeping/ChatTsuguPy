from ..utils import server_exists, text_response, config, get_user
from ..command_matcher import match_command
from . import remote
from . import universal
from .help import help_command
from .rooms_forward import submit_rooms


async def universal_api_handler(user_id: str, message: str,  platform: str, channel_id: str):
    for i in config.commands:
        if res := match_command(message, commands=i['command_name']):
            api = i['api']
            user = await get_user(user_id, platform)
            return await universal.api_handler(user, res, api, platform, channel_id)

    # 开始匹配 help
    if res := match_command(message, commands=['help']):
        return await help_command(res)

    # 开始上传车牌
    if res := match_command(message, commands=['上传车牌', '']):
        await submit_rooms(res, user_id, platform)
    return None


async def remote_api_handler(user_id: str, message: str,  platform: str, channel_id: str):
    for i in config.user_commands:
        if res := match_command(message, commands=i['command_name']):
            api = i['api']
            user = await get_user(user_id, platform)
            return await remote.api_handler(user, res, api, platform, channel_id)

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

