from ...utils import text_response, User, server_id_2_server_name, server_name_2_server_id, server_exists
import tsugu_api_async
from ...config import config
from arclet.alconna import Alconna, Option, Subcommand, Args, CommandMeta, Empty, Namespace, namespace, command_manager
from tsugu_api_core._typing import _ServerName

alc = Alconna(
        ["验证绑定"],
    Args["playerID#你的玩家ID(数字)", int]["serverName#服务器名(字母缩写)", _ServerName],
        meta=CommandMeta(
            compact=config.compact, description="验证绑定",)
    )


async def handler(message: str, user: User, platform: str, channel_id: str):
    res = alc.parse(message)

    if res.matched:
        server = server_name_2_server_id(res.serverName)
        r = await tsugu_api_async.bind_player_verification(platform, user.user_id, server, res.playerID, True)
        if r.get('status') != 'success':
            return text_response(r.get('data'))
        return text_response('绑定成功！现在可以使用 玩家状态 {len(user.game_ids) + 1} 查看绑定的玩家状态')
    elif res.head_matched:
        return text_response(res.error_info)
    return None
