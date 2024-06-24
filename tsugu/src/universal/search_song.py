from ...utils import get_user, text_response, User, server_id_2_server_name, server_name_2_server_id, get_user_async
import tsugu_api
from arclet.alconna import Alconna, Option, Subcommand, Args, CommandMeta, Empty, Namespace, namespace, AllParam
import tsugu_api_async


alc = Alconna(
        ["查曲"],
        Args["word#歌曲信息，名称，乐队，难度等。", AllParam],
        meta=CommandMeta(
            compact=True,
            description="查曲",
            usage='根据关键词或曲目ID查询曲目信息。',
            example='''查曲 1 :返回1号曲的信息
查曲 ag lv27 :返回所有难度为27的ag曲列表
查曲 >27 :查询大于27的曲目
查曲 滑滑蛋 :匹配歌曲 fuwa fuwa time'''
        )
    )


def handler(message: str, user_id: str, platform: str, channel_id: str):
    res = alc.parse(message)

    if res.matched:
        user = get_user(user_id, platform)
        return tsugu_api.search_song(user.default_server, " ".join(res.word))

    return res


async def handler_async(message: str, user_id: str, platform: str, channel_id: str):
    res = alc.parse(message)

    if res.matched:
        user = await get_user_async(user_id, platform)
        return await tsugu_api_async.search_song(user.default_server, " ".join(res.word))

    return res


