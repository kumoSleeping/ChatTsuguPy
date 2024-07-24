from ...utils import get_user, text_response, User, server_id_2_server_name, server_name_2_server_id, server_exists, get_user_async
import tsugu_api
import tsugu_api_async

from arclet.alconna import Alconna, Option, Subcommand, Args, CommandMeta, Empty, Namespace, namespace, command_manager
from tsugu_api_core._typing import _ServerName


alc = Alconna(
        ["玩家状态"],
        Args["accountIndex;?", int],
        meta=CommandMeta(
            compact=True,
            description="查询自己的玩家状态",
            usage='根据关键词或活动ID查询活动信息',
            example='''玩家状态 :返回指定默认账号的玩家状态
玩家状态 1 :返回账号1的玩家状态

可以使用 交换绑定顺序 来交换绑定的玩家顺序
例如：交换绑定顺序 1 2 交换账号1和2的绑定顺序

可以使用 主账号 来设置默认查询账号
例如：主账号 2 设置账号2为默认查询账号

已取消自动跟随服务器显示不同服务器账号“玩家状态”的功能，请使用 “玩家状态 数字” 来查询。
例如：玩家状态 2
'''
        )
    )


def handler(message: str, user_id: str, platform: str):

    def _case_default():
        user_player_index = user.user_player_index
        try:
            game_id_msg = user.user_player_list[user_player_index]
            return tsugu_api.search_player(int(game_id_msg.get("playerId")), game_id_msg.get("server")) + text_response(f'已查找默认玩家状态（{user_player_index + 1}），“help 玩家状态” 了解更多。')
        except Exception as e:
            return text_response(e)

    def _case_index():
        if res.accountIndex > len(user.user_player_list) or res.accountIndex < 1:
            return text_response(f'未找到记录 {res.accountIndex}。')
        try:
            game_id_msg = user.user_player_list[res.accountIndex - 1]
            return tsugu_api.search_player(int(game_id_msg.get("playerId")), game_id_msg.get("server")) + text_response(f'已查找账号 {res.accountIndex} 玩家状态，“help 玩家状态” 了解更多。')
        except Exception as e:
            return text_response(e)

    res = alc.parse(message)

    if res.matched:
        user = get_user(user_id, platform)
        if res.accountIndex:
            return _case_index()
        else:
            return _case_default()

    return res


async def handler_async(message: str, user_id: str, platform: str):

        async def _case_default():
            user_player_index = user.user_player_index
            try:
                game_id_msg = user.user_player_list[user_player_index]
                return await tsugu_api_async.search_player(int(game_id_msg.get("playerId")), game_id_msg.get("server")) + text_response(f'已查找默认玩家状态（{user_player_index + 1}），“help 玩家状态” 了解更多。')
            except Exception as e:
                return text_response(e)

        async def _case_index():
            if res.accountIndex > len(user.user_player_list) or res.accountIndex < 1:
                return text_response(f'未找到记录 {res.accountIndex}。')
            try:
                game_id_msg = user.user_player_list[res.accountIndex - 1]
                return await tsugu_api_async.search_player(int(game_id_msg.get("playerId")), game_id_msg.get("server")) + text_response(f'已查找账号 {res.accountIndex} 玩家状态，“help 玩家状态” 了解更多。')
            except Exception as e:
                return text_response(e)

        res = alc.parse(message)

        if res.matched:
            user = await get_user_async(user_id, platform)
            if res.accountIndex:
                return _case_index()
            else:
                return _case_default()

        return res


