from ...utils import text_response, User
import tsugu_api
from ...config import config
from arclet.alconna import Alconna, Option, Subcommand, Args, CommandMeta, Empty, Namespace, namespace, command_manager


alc = Alconna(
        ["查卡面", "查插画"],
        Args["cardId", int],
        meta=CommandMeta(
            compact=config.compact, description="查卡面",
            usage='根据卡片ID查询卡片插画',
            example='查卡面 1399 :返回1399号卡牌的插画'
        )
    )


def handler(message: str, user: User, platform: str, channel_id: str):
    res = alc.parse(message)

    if res.matched:
        return tsugu_api.get_card_illustration(res.cardId)
    elif res.head_matched:
        return text_response(res.error_info)
    return None

