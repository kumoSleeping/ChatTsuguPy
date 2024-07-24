from typing import List

from ...utils import get_user, text_response, User, server_id_2_server_name, server_names_2_server_ids, get_user_async
import tsugu_api
import tsugu_api_async

from arclet.alconna import Alconna, Option, Subcommand, Args, CommandMeta, Empty, Namespace, namespace, command_manager, \
    MultiVar
from tsugu_api_core._typing import _ServerName, _PartialTsuguUser, _ChangeUserDataResponse
from tsugu.utils import get_user_account_list_msg

alc = Alconna(
    ["交换绑定顺序", "交换账号顺序"],
    Args["accountList;?#使用空格两个索引。", List[int]],
    meta=CommandMeta(
        compact=True,
        description="设定信息显示中的账号排序",
        example="""交换绑定顺序 1 2 : 将第一个账号和第二个账号交换顺序。"""

    )
)


def handler(message: str, user_id: str, platform: str):
    res = alc.parse(message)

    if res.matched:
        if not res.accountList or len(res.accountList) != 2:
            user = get_user(user_id, platform)
            account_list_msg = get_user_account_list_msg(user)
            return text_response(f'''请提供两个账号的索引。
{account_list_msg}''')

        user = get_user(user_id, platform)
        index_1, index_2 = res.accountList
        if any([index < 1 for index in res.accountList]):
            return text_response('账号索引不正确。')

        user.user_player_list[index_1 - 1], user.user_player_list[index_2 - 1] = user.user_player_list[index_2 - 1], \
        user.user_player_list[index_1 - 1]
        update = {'userPlayerList': user.user_player_list}
        try:
            tsugu_api.change_user_data(platform, user.user_id, update)
            return text_response('账号顺序已交换！')
        except Exception as e:
            return text_response(str(e))

    return res


async def handler_async(message: str, user_id: str, platform: str):
    res = alc.parse(message)

    if res.matched:
        if not res.accountList or len(res.accountList) != 2:
            user = await get_user_async(user_id, platform)
            account_list_msg = get_user_account_list_msg(user)
            return text_response(f'''请提供两个账号的索引。
{account_list_msg}''')

        user = await get_user_async(user_id, platform)
        index_1, index_2 = res.accountList
        if any([index < 1 for index in res.accountList]):
            return text_response('账号索引不正确。')

        user.user_player_list[index_1 - 1], user.user_player_list[index_2 - 1] = user.user_player_list[index_2 - 1], \
        user.user_player_list[index_1 - 1]
        update = {'userPlayerList': user.user_player_list}
        try:
            await tsugu_api_async.change_user_data(platform, user.user_id, update)
            return text_response('账号顺序已交换！')
        except Exception as e:
            return text_response(str(e))

