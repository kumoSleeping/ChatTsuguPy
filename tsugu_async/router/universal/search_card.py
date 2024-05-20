from ...utils import text_response, User
import tsugu_api_async
from ...config import config
from arclet.alconna import Alconna, Option, Subcommand, Args, CommandMeta, Empty, Namespace, namespace, command_manager, MultiVar


alc = Alconna(
        ["查卡", "查卡牌"],
        Args["word#请输入卡面ID，角色等查询参数，使用空格隔开", MultiVar(str)],
        meta=CommandMeta(
            compact=config.compact, description="查询卡片信息。",
            usage='根据关键词或卡牌ID查询卡片信息。',
            example='''查卡 1399 :返回1399号卡牌的信息。
查卡面 1399 :返回1399号卡牌的插画。
查卡 红 ars 5x :返回角色 ars 的 5x 卡片的信息。'''
        )
    )


async def handler(message: str, user: User, platform: str, channel_id: str):
    res = alc.parse(message)

    if res.matched:
        return await tsugu_api_async.search_card(user.default_server, " ".join(res.word))
    elif res.head_matched:
        return text_response(res.error_info)
    return None

