from ...utils import get_user, text_response, User, server_id_2_server_name, server_name_2_server_id, get_user_async
import tsugu_api
import tsugu_api_async
from arclet.alconna import Alconna, Option, Subcommand, Args, CommandMeta, Empty, Namespace, namespace, command_manager, MultiVar
from tsugu_api_core._typing import _ServerName


alc = Alconna(
        ["主服务器", "设置主服务器"],
        Args["serverName#服务器名", _ServerName],
        meta=CommandMeta(
            compact=True,
            description="主服务器",
            usage="将指定的服务器设置为你的主服务器。",
            example="""主服务器 cn : 将国服设置为主服务器。"""

        )
    )


def handler(message: str, user_id: str, platform: str, channel_id: str):
    res = alc.parse(message)

    if res.matched:
        user = get_user(user_id, platform)
        r = tsugu_api.change_user_data(platform, user.user_id, {'server_mode': server_name_2_server_id(res.serverName)})
        if r.get('status') != 'success':
            return text_response(r.get('data'))
        return text_response('主服务器已设置为 ' + res.serverName)
    return res


async def handler_async(message: str, user_id: str, platform: str, channel_id: str):
    res = alc.parse(message)

    if res.matched:
        user = await get_user_async(user_id, platform)
        r = await tsugu_api_async.change_user_data(platform, user.user_id, {'server_mode': server_name_2_server_id(res.serverName)})
        if r.get('status') != 'success':
            return text_response(r.get('data'))
        return text_response('主服务器已设置为 ' + res.serverName)
    return res


