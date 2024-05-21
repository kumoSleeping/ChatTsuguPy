from ...utils import text_response, User, server_id_2_server_name, server_name_2_server_id, server_exists, config
import tsugu_api
from arclet.alconna import Alconna, Option, Subcommand, Args, CommandMeta, Empty, Namespace, namespace, command_manager, MultiVar


def handler(message: str, user: User, platform: str, channel_id: str):
    res = Alconna(
        ["查卡", "查卡牌"],
        Args["word#请输入卡面ID，角色等查询参数，使用空格隔开", MultiVar(str)],
        meta=CommandMeta(
            compact=config.compact, description="查询卡片信息。",
            usage='根据关键词或卡牌ID查询卡片信息。',
            example='''查卡 1399 :返回1399号卡牌的信息。
    查卡面 1399 :返回1399号卡牌的插画。
    查卡 红 ars 5x :返回角色 ars 的 5x 卡片的信息。'''
        )
    ).parse(message)

    if res.matched:
        return tsugu_api.search_card(user.default_server, " ".join(res.word))

    return res

