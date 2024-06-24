from ...utils import get_user, text_response, User, server_id_2_server_name, server_name_2_server_id, get_user_async
import tsugu_api
import tsugu_api_async

from arclet.alconna import Alconna, Option, Subcommand, Args, CommandMeta, Empty, Namespace, namespace, command_manager
from tsugu_api_core._typing import _ServerName


alc = Alconna(
        ["验证绑定"],
        Args["playerID#你的玩家ID(数字)", int]["serverName#服务器名(字母缩写)", _ServerName],
        meta=CommandMeta(
            compact=True,
            description="验证绑定",)
    )


def handler(message: str, user_id: str, platform: str, channel_id: str):
    res = alc.parse(message)

    if res.matched:
        user = get_user(user_id, platform)
        server = server_name_2_server_id(res.serverName)
        r = tsugu_api.bind_player_verification(platform, user.user_id, server, res.playerID, True)
        if r.get('status') != 'success':
            return text_response(r.get('data'))
        return text_response(f'绑定成功！现在可以使用 玩家状态 {len(user.game_ids) + 1} 查看绑定的玩家状态')
    return res


async def handler_async(message: str, user_id: str, platform: str, channel_id: str):
    res = alc.parse(message)

    if res.matched:
        user = await get_user_async(user_id, platform)
        server = server_name_2_server_id(res.serverName)
        r = await tsugu_api_async.bind_player_verification(platform, user.user_id, server, res.playerID, True)
        if r.get('status') != 'success':
            return text_response(r.get('data'))
        return text_response(f'绑定成功！现在可以使用 玩家状态 {len(user.game_ids) + 1} 查看绑定的玩家状态')
    return res



