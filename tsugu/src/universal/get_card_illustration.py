from ...utils import text_response, User, server_id_2_server_name, server_name_2_server_id, server_exists, config
import tsugu_api
from arclet.alconna import Alconna, Option, Subcommand, Args, CommandMeta, Empty, Namespace, namespace, command_manager


def handler(message: str, user: User, platform: str, channel_id: str):
    res = Alconna(
        ["查卡面", "查插画"],
        Args["cardId", int],
        meta=CommandMeta(
            compact=config.compact, description="查卡面",
            usage='根据卡片ID查询卡片插画',
            example='查卡面 1399 :返回1399号卡牌的插画'
        )
    ).parse(message)

    if res.matched:
        return tsugu_api.get_card_illustration(res.cardId)

    return res

