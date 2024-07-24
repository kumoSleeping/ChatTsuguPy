from ...utils import get_user, text_response, User, server_id_2_server_name, server_names_2_server_ids, get_user_async
import tsugu_api
import tsugu_api_async

from arclet.alconna import Alconna, Option, Subcommand, Args, CommandMeta, Empty, Namespace, namespace, command_manager, MultiVar
from tsugu_api_core._typing import _ServerName, _PartialTsuguUser, _ChangeUserDataResponse


alc = Alconna(
        ["设置默认服务器", "默认服务器"],
        Args["serverList#使用空格分隔服务器列表。", MultiVar(_ServerName)],
        meta=CommandMeta(
            compact=True,
            description="设定信息显示中的默认服务器排序",
            example="""设置默认服务器 cn jp : 将国服设置为第一服务器，日服设置为第二服务器。"""

        )
    )


def handler(message: str, user_id: str, platform: str):
    res = alc.parse(message)

    if res.matched:
        user = get_user(user_id, platform)
        try:
            tsugu_api.change_user_data(platform, user.user_id, {'displayedServerList': server_names_2_server_ids(res.serverList)})  # serverList是res的用户输入
        except Exception as e:
            return text_response(str(e))

        return text_response('默认服务器已设置为 ' + ' '.join(res.serverList))
    
    return res


async def handler_async(message: str, user_id: str, platform: str):
    res = alc.parse(message)

    if res.matched:
        user = await get_user_async(user_id, platform)
        try:
            await tsugu_api_async.change_user_data(platform, user.user_id, {'displayedServerList': server_names_2_server_ids(res.serverList)})
        except Exception as e:
            return text_response(str(e))

        return text_response('默认服务器已设置为 ' + ' '.join(res.serverList))

    return res


