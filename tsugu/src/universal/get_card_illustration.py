from ...utils import get_user, text_response, User, server_id_2_server_name, server_name_2_server_id
import tsugu_api
from arclet.alconna import Alconna, Option, Subcommand, Args, CommandMeta, Empty, Namespace, namespace, command_manager
import tsugu_api_async


alc = Alconna(
        ["查卡面", "查插画"],
        Args["cardId", int],
        meta=CommandMeta(
            compact=True,
            description="查卡面",
            usage='根据卡片ID查询卡片插画',
            example='查卡面 1399 :返回1399号卡牌的插画'
        )
    )


def handler(message: str, user_id: str, platform: str):
    res = alc.parse(message)

    if res.matched:
        try:
            return tsugu_api.get_card_illustration(res.cardId)
        except Exception as e:
            return text_response(e)

    return res


async def handler_async(message: str, user_id: str, platform: str):
    res = alc.parse(message)

    if res.matched:
        try:
            return await tsugu_api_async.get_card_illustration(res.cardId)
        except Exception as e:
            return text_response(e)

    return res


