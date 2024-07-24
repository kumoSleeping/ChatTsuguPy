from ...utils import get_user, text_response, User, server_id_2_server_name, server_name_2_server_id, get_user_async
import tsugu_api
import tsugu_api_async
from arclet.alconna import Alconna, Option, Subcommand, Args, CommandMeta, Empty, Namespace, namespace, command_manager, MultiVar, AllParam


alc = Alconna(
        ["绑定玩家"],
        Args["args;?", AllParam],
        meta=CommandMeta(
            compact=True,
            description="绑定玩家",
            usage="只需发送‘绑定玩家’。",
        ),
    )


def handler(message: str, user_id: str, platform: str):
    res = alc.parse(message)

    if res.matched:
        try:
            r = tsugu_api.bind_player_request(platform, user_id)
            return text_response(
            f'''正在绑定账号，请将 评论(个性签名) 或者 当前使用的 乐队编队名称改为\n{r.get('data')['verifyCode']}\n稍等片刻等待同步后，发送\n验证绑定 你的玩家ID(数字) 服务器名(字母缩写)\n例如：验证绑定 114****514 cn''')
        except Exception as e:
            return text_response(str(e))

    return res


async def handler_async(message: str, user_id: str, platform: str):
    res = alc.parse(message)

    if res.matched:
        try:
            r = await tsugu_api_async.bind_player_request(platform, user_id)
            return text_response(
            f'''正在绑定账号，请将 评论(个性签名) 或者 当前使用的 乐队编队名称改为\n{r.get('data')['verifyCode']}\n稍等片刻等待同步后，发送\n验证绑定 你的玩家ID(数字) 服务器名(字母缩写)\n例如：验证绑定 114****514 cn''')
        except Exception as e:
            return text_response(str(e))

    return res

