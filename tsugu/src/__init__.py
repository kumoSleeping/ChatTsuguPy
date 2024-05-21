import importlib
from arclet.alconna import Arparma, output_manager, command_manager
from ..utils import text_response


# 主要功能
universal_list = [
    "get_card_illustration",
    "search_player",
    "gacha_simulate",
    "search_gacha",
    "search_event",
    "search_song",
    "song_meta",
    "search_character",
    "song_chart",
    "ycx_all",
    "ycx",
    "lsycx",
    "search_card",
    "event_stage",
]

# 远程数据库相关功能
remote_commands = [
    "player_status",
    "switch_car_forwarding_off",
    "switch_car_forwarding_on",
    "bind_player",
    "unbind_player",
    "change_server_mode",
    "change_default_server",
    "bind_player_verification_off",
    "bind_player_verification_on",
]

# BandoriStation 相关功能
bandoristation_commands = [
    "ycm",
    "rooms_forward",
]

# 帮助信息
help_command = [
    "help",
]


def require(module_path, cmd):
    globals()[cmd] = importlib.import_module(module_path.format(cmd=cmd), __package__)


# 导入模块
[require(f'.universal.{cmd}', cmd) for cmd in universal_list]
[require(f'.remote.{cmd}', cmd) for cmd in remote_commands]
[require(f'.bandoristation.{cmd}', cmd) for cmd in bandoristation_commands]
[require(f'.help.{cmd}', cmd) for cmd in help_command]

output_manager.set_action(lambda *_: None)


def handler(message, user_id, platform, channel_id):
    union_list = universal_list + remote_commands + bandoristation_commands + help_command

    for i in union_list:
        result = getattr(globals()[i], 'handler')(message, user_id, platform, channel_id)

        # 未生成结果
        if isinstance(result, Arparma):
            # 匹配了命令头
            if result.head_matched:

                # 帮助信息
                if result.error_data == ['-h']:
                    return getattr(globals()['help'], 'handler')('help ' + result.header_result, user_id, platform, channel_id)
                # 错误信息
                else:
                    return text_response(result.error_info)

        # 已生成结果
        if isinstance(result, list):
            return result

    return None


async def handler_async(message, user_id, platform, channel_id):
    union_list = universal_list + remote_commands + bandoristation_commands + help_command

    for i in union_list:
        result = await getattr(globals()[i], 'handler_async')(message, user_id, platform, channel_id)

        # 未生成结果
        if isinstance(result, Arparma):
            # 匹配了命令头
            if result.head_matched:

                # 帮助信息
                if result.error_data == ['-h']:
                    return await getattr(globals()['help'], 'handler_async')('help ' + result.header_result, user_id, platform, channel_id)
                # 错误信息
                else:
                    return text_response(result.error_info)

        # 已生成结果
        if isinstance(result, list):
            return result

    return None