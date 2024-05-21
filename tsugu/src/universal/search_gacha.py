from ...utils import text_response, User, server_id_2_server_name, server_name_2_server_id, server_exists, config
import tsugu_api
from arclet.alconna import Alconna, Option, Subcommand, Args, CommandMeta, Empty, Namespace, namespace, command_manager


def handler(message: str, user: User, platform: str, channel_id: str):
    res = Alconna(
        ["查卡池"],
        Args["gachaId#可以通过查活动、查卡等获取", str],
        meta=CommandMeta(
            compact=config.compact, description="查卡池",
            usage='根据卡池ID查询卡池信息',
        )
    ).parse(message)

    if res.matched:
        return tsugu_api.search_gacha(user.default_server, res.gachaId)

    return res
