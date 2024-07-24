from ...utils import get_user, text_response, User, server_id_2_server_name, server_name_2_server_id, get_user_async
from tsugu_api_core._typing import _ServerName
import tsugu_api
from arclet.alconna import Alconna, Option, Subcommand, Args, CommandMeta, Empty, Namespace, namespace, command_manager
import tsugu_api_async


alc = Alconna(
        ["查玩家", "查询玩家"],
        Args["playerId#你的游戏账号(数字)", int]["serverName;?#省略服务器名时，默认从你当前的主服务器查询。", _ServerName.__args__],
        meta=CommandMeta(
            compact=True,
            description="查询玩家信息",
            usage='查询指定ID玩家的信息。查询指定ID玩家的信息。',
            example='查玩家 40474621 jp : 查询日服玩家ID为40474621的玩家信息。\n查玩家 10000000 : 查询你当前默认服务器中，玩家ID为10000000的玩家信息。',
        )
    )


def handler(message: str, user_id: str, platform: str):
    res = alc.parse(message)

    if res.matched:
        user = get_user(user_id, platform)
        if res.serverName:
            server = server_name_2_server_id(res.serverName)
        else:
            server = user.main_server
        print(res.playerId, server)
        if str(res.playerId).startswith('4') and server == 3:
            return text_response('Bestdori 暂不支持渠道服相关功能。')
        try:
            return tsugu_api.search_player(res.playerId, server)
        except Exception as e:
            return text_response(e)

    return res


async def handler_async(message: str, user_id: str, platform: str):
    res = alc.parse(message)

    if res.matched:
        user = await get_user_async(user_id, platform)
        if res.serverName:
            server = server_name_2_server_id(res.serverName)
        else:
            server = user.main_server
        if str(res.playerId).startswith('4') and server == 3:
            return text_response('Bestdori 暂不支持渠道服相关功能。')
        try:
            return await tsugu_api_async.search_player(res.playerId, server)
        except Exception as e:
            return text_response(e)

    return res



