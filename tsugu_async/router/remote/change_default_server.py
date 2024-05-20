from ...utils import text_response, User, server_names_2_server_ids
import tsugu_api_async
from ...config import config
from arclet.alconna import Alconna, Option, Subcommand, Args, CommandMeta, Empty, Namespace, namespace, command_manager, MultiVar
from tsugu_api_core._typing import _ServerName

alc = Alconna(
        ["设置默认服务器", "默认服务器"],
    Args["serverList#使用空格分隔服务器列表。", MultiVar(_ServerName)],
        meta=CommandMeta(
            compact=config.compact, description="设定信息显示中的默认服务器排序",
            example="""设置默认服务器 cn jp : 将国服设置为第一服务器，日服设置为第二服务器。"""

        )
    )


async def handler(message: str, user: User, platform: str, channel_id: str):
    res = alc.parse(message)

    if res.matched:
        r = await tsugu_api_async.change_user_data(platform, user.user_id, {'default_server': server_names_2_server_ids(res.serverList)})
        if r.get('status') != 'success':
            return text_response(r.get('data'))
        return text_response('默认服务器已设置为 ' + ' '.join(res.serverList))
    elif res.head_matched:
        return text_response(res.error_info)
    return None
