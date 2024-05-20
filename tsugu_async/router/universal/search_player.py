from ...utils import text_response, User
from tsugu_api_core._typing import _ServerName
import tsugu_api_async
from ...config import config
from arclet.alconna import Alconna, Option, Subcommand, Args, CommandMeta, Empty, Namespace, namespace, command_manager


alc = Alconna(
    ["查玩家", "查寻玩家"],
    Args["playerId#你的游戏账号(数字)", int]["serverName;?#省略服务器名时，默认从你当前的主服务器查询。", _ServerName.__args__],
    meta=CommandMeta(
        compact=config.compact, description="查询玩家信息",
        usage='查询指定ID玩家的信息。查询指定ID玩家的信息。',
        example='查玩家 40474621 jp : 查询日服玩家ID为40474621的玩家信息。\n查玩家 10000000 : 查询你当前默认服务器中，玩家ID为10000000的玩家信息。',
    )
)


async def handler(message: str, user: User, platform: str, channel_id: str):
    res = alc.parse(message)

    if res.matched:
        if res.serverName:
            server = res.serverName
        else:
            server = user.server_mode
        return await tsugu_api_async.search_player(res.playerId, server)
    elif res.head_matched:
        return text_response(res.error_info)
    return None



