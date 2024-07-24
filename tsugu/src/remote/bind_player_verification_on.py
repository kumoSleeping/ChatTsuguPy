from ...utils import get_user, text_response, User, server_id_2_server_name, server_name_2_server_id, get_user_async
import tsugu_api
import tsugu_api_async

from arclet.alconna import Alconna, Option, Subcommand, Args, CommandMeta, Empty, Namespace, namespace, command_manager
from tsugu_api_core._typing import _ServerName


alc = Alconna(
        ["验证绑定"],
        Args["playerId#你的玩家ID(数字)", int]["serverName#服务器名(字母缩写)", _ServerName],
        meta=CommandMeta(
            compact=True,
            description="验证绑定",)
    )


def handler(message: str, user_id: str, platform: str):
    res = alc.parse(message)

    if res.matched:
        user = get_user(user_id, platform)
        server = server_name_2_server_id(res.serverName)
        if str(res.playerId).startswith('4') and server == 3:
            return text_response('Bestdori 暂不支持渠道服相关功能。')
        try:
            r = tsugu_api.bind_player_verification(platform, user.user_id, server, res.playerId, 'bind')
            return text_response(f'绑定成功！现在可以使用 玩家状态 {len(user.user_player_list) + 1} 查看绑定的玩家状态')
        except Exception as e:
            return text_response(str(e))

    return res


async def handler_async(message: str, user_id: str, platform: str):
    res = alc.parse(message)

    if res.matched:
        user = await get_user_async(user_id, platform)
        server = server_name_2_server_id(res.serverName)
        if str(res.playerId).startswith('4') and len(str(res.playerId)) == 10 and server == 3:
            return text_response('Bestdori 暂不支持渠道服相关功能。')
        try:
            r = await tsugu_api_async.bind_player_verification(platform, user.user_id, server, res.playerId, 'bind')
            return text_response(f'绑定成功！现在可以使用 玩家状态 {len(user.user_player_list) + 1} 查看绑定的玩家状态')
        except Exception as e:
            return text_response(str(e))

    return res



