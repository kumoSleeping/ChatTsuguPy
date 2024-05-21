from ...utils import text_response, User, server_id_2_server_name, server_name_2_server_id, server_exists, config
import tsugu_api
from arclet.alconna import Alconna, Option, Subcommand, Args, CommandMeta, Empty, Namespace, namespace, command_manager
from tsugu_api_core._typing import _ServerName


def handler(message: str, user: User, platform: str, channel_id: str):
    res = Alconna(
        ["ycx", "预测线"],
        Args['tier', int]['eventId;?#活动ID，省略时查询当前活动。', int]
            ['serverName#省略服务器名时，默认从你当前的主服务器查询。活动ID不存在时，也可以作为第二个参数。', _ServerName.__args__, None],
        meta=CommandMeta(
            compact=config.compact, description="查询指定档位的预测线",
            usage='查询指定档位的预测线。',
            example='''ycx 1000 :返回默认服务器当前活动1000档位的档线与预测线。
ycx 1000 177 jp:返回日服177号活动1000档位的档线与预测线。'''
        )
    ).parse(message)

    if res.matched:
        server = server_name_2_server_id(res.serverName) if res.serverName else user.server_mode
        return tsugu_api.ycx(server, res.tier, res.eventId)

    return res

