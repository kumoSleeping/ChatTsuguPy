from ...utils import get_user, text_response, User, server_id_2_server_name, server_name_2_server_id, get_user_async
import tsugu_api
import tsugu_api_async

from arclet.alconna import Alconna, Option, Subcommand, Args, CommandMeta, Empty, Namespace, namespace, command_manager, AllParam
from tsugu.utils import get_user_account_list_msg


alc = Alconna(
        ["解除绑定"],
        Args["any", AllParam],
        meta=CommandMeta(
            compact=True,
            description="解除绑定",
            usage="验证解绑 记录编号(数字)",
            example="验证解绑 1 : 解绑第一个记录"
        ),
    )



def handler(message: str, user_id: str, platform: str):
    res = alc.parse(message)

    if res.matched:
        user = get_user(user_id, platform)

        try:
            bind_record = get_user_account_list_msg(user)
            r = tsugu_api.bind_player_request(platform, user.user_id)
            return text_response(f'''请先然后登陆游戏，将 评论(个性签名) 或者 当前使用的 乐队编队名称改为
{r.get('data')['verifyCode']}
稍等片刻等待同步后，选择你要解除的账号数字：
{bind_record}
对 tsugu 发送 “验证解绑 数字” 来完成本次身份验证。
例如：验证解绑 1
''')
        except Exception as e:
            return text_response(str(e))
    return res


async def handler_async(message: str, user_id: str, platform: str):
    res = alc.parse(message)

    if res.matched:
        user = await get_user_async(user_id, platform)

        try:
            bind_record = get_user_account_list_msg(user)
            r = await tsugu_api_async.bind_player_request(platform, user.user_id)
            return text_response(f'''请先然后登陆游戏，将 评论(个性签名) 或者 当前使用的 乐队编队名称改为
{r.get('data')['verifyCode']}
稍等片刻等待同步后，选择你要解除的账号数字：
{bind_record}
对 tsugu 发送 “验证解绑 数字” 来完成本次身份验证。
例如：验证解绑 1
''')
        except Exception as e:
            return text_response(str(e))
    return res

