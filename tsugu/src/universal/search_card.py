from ...utils import get_user, text_response, User, server_id_2_server_name, server_name_2_server_id, get_user_async
import tsugu_api
from arclet.alconna import Alconna, Option, Subcommand, Args, CommandMeta, Empty, Namespace, namespace, command_manager, AllParam
import tsugu_api_async


alc = Alconna(
        ["查卡", "查卡牌"],
        Args["word#请输入卡面ID，角色等查询参数，使用空格隔开", AllParam],
        meta=CommandMeta(
            compact=True,
            description="查询卡片信息。",
            usage='根据关键词或卡牌ID查询卡片信息。',
            example='''查卡 1399 :返回1399号卡牌的信息。
    查卡面 1399 :返回1399号卡牌的插画。
    查卡 红 ars 5x :返回角色 ars 的 5x 卡片的信息。'''
        )
    )

def handler(message: str, user_id: str, platform: str, channel_id: str):
    res = alc.parse(message)

    if res.matched:
        user = get_user(user_id, platform)
        return tsugu_api.search_card(user.default_server, " ".join(res.word))

    return res


async def handler_async(message: str, user_id: str, platform: str, channel_id: str):
    res = alc.parse(message)

    if res.matched:
        user = await get_user_async(user_id, platform)
        return await tsugu_api_async.search_card(user.default_server, " ".join(res.word))

    return res

