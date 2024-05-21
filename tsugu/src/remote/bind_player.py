from ...utils import get_user, text_response, User, server_id_2_server_name, server_name_2_server_id
import tsugu_api
from arclet.alconna import Alconna, Option, Subcommand, Args, CommandMeta, Empty, Namespace, namespace, command_manager, MultiVar, AllParam
import tsugu_api_async


alc = Alconna(
        ["绑定玩家"],
        Args["args;?", AllParam],
        meta=CommandMeta(
            compact=True,
            description="绑定玩家",
            usage="只需发送‘绑定玩家’。",
        ),
    )


def handler(message: str, user_id: str, platform: str, channel_id: str):
    res = alc.parse(message)

    if res.matched:
        user = get_user(user_id, platform)
        r = tsugu_api.bind_player_request(platform, user_id, user.server_mode, True)
        if r.get('status') != 'success':
            return text_response(r.get('data'))
        return text_response(
            f'''正在绑定账号，请将 评论(个性签名) 或者 当前使用的 乐队编队名称改为\n{r.get('data')['verifyCode']}\n稍等片刻等待同步后，发送\n验证绑定 你的玩家ID(数字) 服务器名(字母缩写)\n例如：验证绑定 114****514 cn''')

    return res


async def handler_async(message: str, user_id: str, platform: str, channel_id: str):
    res = alc.parse(message)

    if res.matched:
        user = get_user(user_id, platform)
        r = await tsugu_api_async.bind_player_request(platform, user.user_id, user.server_mode, False)
        if r.get('status') != 'success':
            return text_response(r.get('data'))
        return text_response(
            f'''正在绑定账号，请将 评论(个性签名) 或者 当前使用的 乐队编队名称改为\n{r.get('data')['verifyCode']}\n稍等片刻等待同步后，发送\n验证绑定 你的玩家ID(数字) 服务器名(字毝缩写)\n例如：验证绑定 114****514 cn''')

    return res

