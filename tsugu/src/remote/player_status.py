from ...utils import get_user, text_response, User, server_id_2_server_name, server_name_2_server_id, server_exists
import tsugu_api
from arclet.alconna import Alconna, Option, Subcommand, Args, CommandMeta, Empty, Namespace, namespace, command_manager
from tsugu_api_core._typing import _ServerName
import tsugu_api_async


alc = Alconna(
        ["玩家状态"],
        Args["serverName;?", _ServerName.__args__]["serverIndex;?", int],
        meta=CommandMeta(
            compact=True,
            description="查询自己的玩家状态",
            usage='根据关键词或活动ID查询活动信息',
            example='''玩家状态 :返回玩家状态(优先当前服务器下第一条记录)
玩家状态 1 :返回绑定的第一条记录的状态
玩家状态 jp :返回绑定的cn服务器的记录的状态'''
        )
    )


def handler(message: str, user_id: str, platform: str, channel_id: str):
    def _utils_search_player_by_game_id(game_id, additional_text=""):
        player_id = str(game_id.get("game_id"))
        server = int(game_id.get("server"))
        response = tsugu_api.search_player(int(player_id), server)
        return response + text_response(additional_text)

    def _case_default(user: User):
        # 优先当前服务器
        for game_id in user.game_ids:
            if game_id.get("server") == user.server_mode:
                text = f' 已查找默认服务器 {server_id_2_server_name(user.server_mode)} 的记录。'
                return _utils_search_player_by_game_id(game_id, text)
        # 兜底逻辑：使用第一个记录
        if user.game_ids:
            game_id = user.game_ids[0]
            text = f' 已查找第一个记录。'
            return _utils_search_player_by_game_id(game_id, text)
        return text_response('未绑定任何记录，可以使用 绑定玩家 进行绑定')

    def _case_server(user: User, server_name: str):
        server_id = server_name_2_server_id(server_name)
        # 服务器不存在
        if not server_exists(server_id):
            return text_response(f'服务器 {server_name} 不存在。')
        # 查找记录
        for game_id in user.game_ids:
            if game_id.get("server") == server_id:
                # 找到记录
                return _utils_search_player_by_game_id(game_id)
        # 未找到记录
        return text_response(f'未在记录中找到服务器 {server_name} 的记录。')

    def _case_index(user: User, index: int):
        if index > len(user.game_ids) or index < 1:
            return text_response(f'未找到记录 {index}。')
        return _utils_search_player_by_game_id(user.game_ids[index - 1])

    res = alc.parse(message)

    if res.matched:
        user = get_user(user_id, platform)
        if res.serverName:
            return _case_server(user, res.serverName)
        elif res.serverIndex:
            return _case_index(user, res.serverIndex)
        else:
            return _case_default(user)
    return res


async def handler_async(message: str, user_id: str, platform: str, channel_id: str):
    async def _utils_search_player_by_game_id(game_id, additional_text=""):
        player_id = str(game_id.get("game_id"))
        server = int(game_id.get("server"))
        response = await tsugu_api_async.search_player(int(player_id), server)
        return response + text_response(additional_text)

    async def _case_default(user: User):
        # 优先当前服务器
        for game_id in user.game_ids:
            if game_id.get("server") == user.server_mode:
                text = f' 已查找默认服务器 {server_id_2_server_name(user.server_mode)} 的记录。'
                return await _utils_search_player_by_game_id(game_id, text)
        # 兜底逻辑：使用第一个记录
        if user.game_ids:
            game_id = user.game_ids[0]
            text = f' 已查找第一个记录。'
            return await _utils_search_player_by_game_id(game_id, text)
        return text_response('未绑定任何记录，可以使用 绑定玩家 进行绑定')

    async def _case_server(user: User, server_name: str):
        server_id = server_name_2_server_id(server_name)
        # 服务器不存在
        if not server_exists(server_id):
            return text_response(f'服务器 {server_name} 不存在。')
        # 查找记录
        for game_id in user.game_ids:
            if game_id.get("server") == server_id:
                # 找到记录
                return await _utils_search_player_by_game_id(game_id)
        # 未找到记录
        return text_response(f'未在记录中找到服务器 {server_name} 的记录。')

    async def _case_index(user: User, index: int):
        if index > len(user.game_ids) or index < 1:
            return text_response(f'未找到记录 {index}。')
        return await _utils_search_player_by_game_id(user.game_ids[index - 1])

    res = alc.parse(message)

    if res.matched:
        user = get_user(user_id, platform)
        if res.serverName:
            return await _case_server(user, res.serverName)
        elif res.serverIndex:
            return await _case_index(user, res.serverIndex)
        else:
            return await _case_default(user)
    return res


