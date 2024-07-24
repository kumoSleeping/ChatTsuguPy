from typing import List

from ...utils import get_user, text_response, User, server_id_2_server_name, server_names_2_server_ids, get_user_async
import tsugu_api
import tsugu_api_async

from arclet.alconna import Alconna, Option, Subcommand, Args, CommandMeta, Empty, Namespace, namespace, command_manager, MultiVar
from tsugu_api_core._typing import _ServerName, _PartialTsuguUser, _ChangeUserDataResponse
from tsugu.utils import get_user_account_list_msg


alc = Alconna(
    ["主账号"],
    Args["accountIndex#主账号，从1开始", int],
    meta=CommandMeta(
        compact=True,
        description="设定默认玩家状态、车牌展示中的主账号使用第几个账号",
        example="""主账号 2 : 将第二个账号设置为主账号。"""
    )
)


def handler(message: str, user_id: str, platform: str):
    res = alc.parse(message)

    if res.matched:
        user = get_user(user_id, platform)
        if len(user.user_player_list) < res.accountIndex or res.accountIndex < 1:
            return text_response('账号数量不正确。')

        update = {'userPlayerIndex': res.accountIndex - 1}
        try:
            tsugu_api.change_user_data(platform, user.user_id, update)
            return text_response('主账号已设置为账号 ' + str(res.accountIndex))
        except Exception as e:
            return text_response(str(e))

    return res


async def handler_async(message: str, user_id: str, platform: str):
    res = alc.parse(message)

    if res.matched:
        user = await get_user_async(user_id, platform)
        if len(user.user_player_list) < res.accountIndex or res.accountIndex < 1:
            return text_response('账号数量不正确。')

        update = {'userPlayerIndex': res.accountIndex - 1}
        try:
            await tsugu_api_async.change_user_data(platform, user.user_id, update)
            return text_response('主账号已设置为账号 ' + str(res.accountIndex))
        except Exception as e:
            return text_response(str(e))

    return res
