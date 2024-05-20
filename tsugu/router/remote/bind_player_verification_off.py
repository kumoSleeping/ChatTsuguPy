from ...utils import text_response, User, server_id_2_server_name, server_name_2_server_id, server_exists
import tsugu_api
from ...config import config
from arclet.alconna import Alconna, Option, Subcommand, Args, CommandMeta, Empty, Namespace, namespace, command_manager
from tsugu_api_core._typing import _ServerName


alc = Alconna(
        ["验证解绑"],
    Args["index#要解绑的绑定编号", int],
        meta=CommandMeta(
            compact=config.compact, description="验证解绑",
            usage="验证解绑 记录编号(数字)",
            example="验证解绑 1 : 解绑第一个记录"
        ),
    )


def handler(message: str, user: User, platform: str, channel_id: str):
    res = alc.parse(message)

    if res.matched:
        if len(user.game_ids) < int(res.index):
            return text_response('未找到记录')
        player_id = user.game_ids[int(res.index) - 1].get("game_id")
        server_mode = user.game_ids[int(res.index) - 1].get("server")
        r = tsugu_api.bind_player_verification(platform, user.user_id, server_mode, player_id, False)
        if r.get('status') != 'success':
            return text_response(r.get('data'))
        return text_response('解绑成功！')
    elif res.head_matched:
        return text_response(res.error_info)
    return None


# def handler(user: User, res: MC, platform: str, channel_id: str):
#     if not res.args or len(res.args) > 1:
#         return text_response('请输入正确的格式：验证解绑 记录编号(数字)')
#     if not res.args[0].isdigit():
#         return text_response('请输入正确的格式：验证解绑 记录编号(数字)')
#     if int(res.text) <= 0:
#         return text_response('请输入正确的格式：验证解绑 记录编号(数字)，编号从1开始')
#     if len(user.game_ids) < int(res.text):
#         return text_response('未找到记录')
#     player_id = user.game_ids[int(res.args[0]) - 1].get("game_id")
#     server_mode = user.game_ids[int(res.args[0]) - 1].get("server")
#     r = tsugu_api.bind_player_verification(platform, user.user_id, server_mode, player_id, False)
#     if r.get('status') != 'success':
#         return text_response(r.get('data'))
#     return text_response('解绑成功！')
#
#
