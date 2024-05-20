from ...utils import text_response, User
import tsugu_api
from ...config import config
from arclet.alconna import Alconna, Option, Subcommand, Args, CommandMeta, Empty, Namespace, namespace, command_manager


alc = Alconna(
        ["查卡池"],
        Args["gachaId#可以通过查活动、查卡等获取", str],
        meta=CommandMeta(
            compact=config.compact, description="查卡池",
            usage='根据卡池ID查询卡池信息',
        )
    )


def handler(message: str, user: User, platform: str, channel_id: str):
    res = alc.parse(message)

    if res.matched:
        return tsugu_api.search_gacha(user.default_server, res.gachaId)
    elif res.head_matched:
        return text_response(res.error_info)
    return None
