from ...utils import text_response, User, server_id_2_server_name, server_name_2_server_id, server_exists, config
import tsugu_api
from arclet.alconna import Alconna, Option, Subcommand, Args, CommandMeta, Empty, Namespace, namespace, command_manager
from tsugu_api_core._typing import _ServerName


def handler(message: str, user: User, platform: str, channel_id: str):
    res = Alconna(
        ["查询分数表", '查分数表', '查询分数榜', '查分数榜'],
        Args["serverName;?#省略服务器名时，默认从你当前的主服务器查询。", _ServerName.__args__],
        meta=CommandMeta(
            compact=config.compact, description="查询分数表",
            usage='查询指定服务器的歌曲分数表。',
            example='''查询分数表 cn :返回国服的歌曲分数表'''
        )
    ).parse(message)

    if res.matched:
        if res.serverName:
            server = server_name_2_server_id(res.serverName)
        else:
            server = user.server_mode
        return tsugu_api.song_meta(user.default_server, server)

    return res

