from ...utils import text_response, User, server_id_2_server_name, server_name_2_server_id, server_exists
import tsugu_api
from ...config import config
from arclet.alconna import Alconna, Option, Subcommand, Args, CommandMeta, Empty, Namespace, namespace, command_manager, MultiVar, AllParam
from tsugu_api_core._typing import _ServerName


alc = Alconna(
        ["绑定玩家"],
    Args["args;?", AllParam],
    meta=CommandMeta(
            compact=config.compact, description="绑定玩家",
            usage="只需发送‘绑定玩家’。",
        ),
    )


def handler(message: str, user: User, platform: str, channel_id: str):
    res = alc.parse(message)

    if res.matched:
        r = tsugu_api.bind_player_request(platform, user.user_id, user.server_mode, False)
        if r.get('status') != 'success':
            return text_response(r.get('data'))
        return text_response(
            f'''正在绑定账号，请将 评论(个性签名) 或者 当前使用的 乐队编队名称改为\n{r.get('data')['verifyCode']}\n稍等片刻等待同步后，发送\n验证绑定 你的玩家ID(数字) 服务器名(字母缩写)\n例如：验证绑定 114****514 cn''')
    elif res.head_matched:
        return text_response(res.error_info)
    return None

