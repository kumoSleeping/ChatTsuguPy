from ...utils import text_response, User, server_name_2_server_id
import tsugu_api
from ...config import config
from arclet.alconna import Alconna, Option, Subcommand, Args, CommandMeta, Empty, Namespace, namespace, command_manager, MultiVar
from tsugu_api_core._typing import _ServerName

alc = Alconna(
        ["主服务器", "设置主服务器"],
    Args["serverName#服务器名", _ServerName],
        meta=CommandMeta(
            compact=config.compact, description="主服务器",
            usage="将指定的服务器设置为你的主服务器。",
            example="""主服务器 cn : 将国服设置为主服务器。"""

        )
    )


def handler(message: str, user: User, platform: str, channel_id: str):
    res = alc.parse(message)

    if res.matched:
        r = tsugu_api.change_user_data(platform, user.user_id, {'server_mode': server_name_2_server_id(res.serverName)})
        if r.get('status') != 'success':
            return text_response(r.get('data'))
        return text_response('主服务器已设置为 ' + res.serverName)
    elif res.head_matched:
        return text_response(res.error_info)
    return None

#
# def handler(user: User, res: MC, platform: str, channel_id: str):
#     if res.args:
#         server_mode = server_name_2_server_id(res.args[0])
#         if not server_exists(server_mode):
#             return text_response('未找到服务器，请输入正确的服务器名')
#         update: _Update = {'server_mode': server_mode, }
#         if r := tsugu_api.change_user_data(platform, user.user_id, update):
#             if r.get('status') == 'success':
#                 return text_response('主服务器已设置为 ' + server_id_2_server_name(server_mode))
#             return text_response(r.get('data'))
#
