from ...utils import text_response, User
import tsugu_api_async
from ...config import config
from arclet.alconna import Alconna, Option, Subcommand, Args, CommandMeta, Empty, Namespace, namespace, MultiVar


alc = Alconna(
        ["查角色"],
        Args["word#角色名，乐队，昵称等查询参数", MultiVar(str)],
        meta=CommandMeta(
            compact=config.compact, description="查询角色信息",
            usage='根据关键词或角色ID查询角色信息',
            example='''查角色 10 :返回10号角色的信息。
查角色 吉他 :返回所有角色模糊搜索标签中包含吉他的角色列表。'''
        )
    )


async def handler(message: str, user: User, platform: str, channel_id: str):
    res = alc.parse(message)

    if res.matched:
        return await tsugu_api_async.search_character(user.default_server, " ".join(res.word))
    elif res.head_matched:
        return text_response(res.error_info)
    return None
