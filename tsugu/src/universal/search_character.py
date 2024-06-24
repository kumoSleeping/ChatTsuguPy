from ...utils import get_user, text_response, User, server_id_2_server_name, server_name_2_server_id, get_user_async
import tsugu_api
from arclet.alconna import Alconna, Option, Subcommand, Args, CommandMeta, Empty, Namespace, namespace, AllParam
import tsugu_api_async

alc = Alconna(
        ["查角色"],
        Args["word#角色名，乐队，昵称等查询参数", AllParam],
        meta=CommandMeta(
            compact=True,
            description="查询角色信息",
            usage='根据关键词或角色ID查询角色信息',
            example='''查角色 10 :返回10号角色的信息。
查角色 吉他 :返回所有角色模糊搜索标签中包含吉他的角色列表。'''
        )
    )


def handler(message: str, user_id: str, platform: str, channel_id: str):
    res = alc.parse(message)

    if res.matched:
        user = get_user(user_id, platform)
        return tsugu_api.search_character(user.default_server, " ".join(res.word))

    return res


async def handler_async(message: str, user_id: str, platform: str, channel_id: str):
    res = alc.parse(message)

    if res.matched:
        user = await get_user_async(user_id, platform)
        return await tsugu_api_async.search_character(user.default_server, " ".join(res.word))

    return res


