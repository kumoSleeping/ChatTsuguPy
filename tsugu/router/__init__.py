from ..utils import server_exists, text_response, config, get_user
from ..command_matcher import match_command
from . import remote
from . import universal
from . import bandoristation
from ..command_matcher import match_command, MC


def handler(message: str, user_id: str, platform: str, channel_id: str):
    # 进行 api 命令匹配
    result = universal_api_handler(user_id, message, platform, channel_id)
    if result:
        return result

    # 远程命令
    result = remote_api_handler(user_id, message, platform, channel_id)
    if result:
        return result

    result = bandoristation_api_handler(user_id, message, platform, channel_id)
    if result:
        return result

    # 开始匹配 help
    if res := match_command(message, commands=['help']):
        return help_command(res)


async def help_command(res: MC):
    if not res.args:
        command_list = list(config._help_doc_dict.keys())
        command_list.sort()
        return text_response(f'当前支持的命令有：\n{" ".join(command_list)}\n请使用"help 命令名"来查看命令的详细帮助')
    if help_text := config.help_doc_dict.get(res.args[0], None):
        return text_response(help_text)
    return None


def bandoristation_api_handler(user_id: str, message: str,  platform: str, channel_id: str):
    for i in config.bandoristation_commands:
        if res := match_command(message, commands=i['command_name']):
            api = i['api']
            user = get_user(user_id, platform)
            return bandoristation.api_handler(user, res, api, platform, channel_id)
    return None


def universal_api_handler(user_id: str, message: str,  platform: str, channel_id: str):
    for i in config.commands:
        if res := match_command(message, commands=i['command_name']):
            api = i['api']
            user = get_user(user_id, platform)
            return universal.api_handler(user, res, api, platform, channel_id)
    return None


def remote_api_handler(user_id: str, message: str,  platform: str, channel_id: str):
    for i in config.user_commands:
        if res := match_command(message, commands=i['command_name']):
            api = i['api']
            user = get_user(user_id, platform)
            return remote.api_handler(user, res, api, platform, channel_id)
    return None



