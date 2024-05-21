from ...utils import get_user, text_response, User, server_id_2_server_name, server_name_2_server_id
import tsugu_api
from arclet.alconna import Alconna, Option, Subcommand, Args, CommandMeta, Empty, Namespace, namespace, command_manager
from tsugu_api_core._typing import _ServerName
import tsugu_api_async


alc = Alconna(
        ["lsycx", "历史预测线"], ['/', ''],
        Args['tier', int]['eventId;?#活动ID，省略时查询当前活动。', int]
            ['serverName;?#省略服务器名时，默认从你当前的主服务器查询。', _ServerName.__args__],
        meta=CommandMeta(
            compact=True,
            description="查询指定档位的历史预测线。",
            usage='查询指定档位的预测线与最近的4期活动类型相同的活动的档线数据。',
            example='''lsycx 1000 
lsycx 1000 177 jp'''
        )
    )


def handler(message: str, user_id: str, platform: str, channel_id: str):
    res = alc.parse(message)

    if res.matched:
        user = get_user(user_id, platform)
        server = server_name_2_server_id(res.serverName) if res.serverName else user.server_mode
        return tsugu_api.lsycx(server, res.tier, res.eventId)

    return res


async def handler_async(message: str, user_id: str, platform: str, channel_id: str):
    res = alc.parse(message)

    if res.matched:
        user = get_user(user_id, platform)
        server = server_name_2_server_id(res.serverName) if res.serverName else user.server_mode
        return await tsugu_api_async.lsycx(server, res.tier, res.eventId)

    return res


