from ..utils import server_exists, text_response, config, get_user
from ..command_matcher import match_command, MC
from . import remote
from . import universal
from . import bandoristation
from ..utils import text_response, User


async def handler(message: str, user_id: str, platform: str, channel_id: str):
    # 进行 api 命令匹配
    result = await universal_api_handler(user_id, message, platform, channel_id)
    if result:
        return result

    # 远程命令
    result = await remote_api_handler(user_id, message, platform, channel_id)
    if result:
        return result

    result = await bandoristation_api_handler(user_id, message, platform, channel_id)
    if result:
        return result

    # 开始匹配 help
    if res := match_command(message, commands=['help']):
        return await help_command(res)


async def help_command(res: MC):
    if not res.args:
        command_list = list(config._help_doc_dict.keys())
        command_list.sort()
        return text_response(f'当前支持的命令有：\n{" ".join(command_list)}\n请使用"help 命令名"来查看命令的详细帮助')
    if help_text := config._help_doc_dict.get(res.args[0], None):
        return text_response(help_text)
    return None


async def universal_api_handler(user_id: str, message: str,  platform: str, channel_id: str):
    for i in config.commands:
        if res := match_command(message, commands=i['command_name']):
            api = i['api']
            user = await get_user(user_id, platform)
            return await universal.api_handler(user, res, api, platform, channel_id)
    return None


async def bandoristation_api_handler(user_id: str, message: str,  platform: str, channel_id: str):
    for i in config.bandoristation_commands:
        if res := match_command(message, commands=i['command_name']):
            api = i['api']
            user = await get_user(user_id, platform)
            return await bandoristation.api_handler(user, res, api, platform, channel_id)
    return None


async def remote_api_handler(user_id: str, message: str,  platform: str, channel_id: str):
    for i in config.user_commands:
        if res := match_command(message, commands=i['command_name']):
            api = i['api']
            user = await get_user(user_id, platform)
            return await remote.api_handler(user, res, api, platform, channel_id)
    return None



