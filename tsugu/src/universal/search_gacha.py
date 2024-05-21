from ...utils import get_user, text_response, User, server_id_2_server_name, server_name_2_server_id
import tsugu_api
from arclet.alconna import Alconna, Option, Subcommand, Args, CommandMeta, Empty, Namespace, namespace, command_manager
import tsugu_api_async


alc = Alconna(
        ["查卡池"],
        Args["gachaId#可以通过查活动、查卡等获取", str],
        meta=CommandMeta(
            compact=True,
            description="查卡池",
            usage='根据卡池ID查询卡池信息',
        )
    )


def handler(message: str, user_id: str, platform: str, channel_id: str):
    res = alc.parse(message)

    if res.matched:
        user = get_user(user_id, platform)
        return tsugu_api.search_gacha(user.default_server, res.gachaId)

    return res


async def handler_async(message: str, user_id: str, platform: str, channel_id: str):
    res = alc.parse(message)

    if res.matched:
        user = get_user(user_id, platform)
        return await tsugu_api_async.search_gacha(user.default_server, res.gachaId)

    return res


