from ...config import config
import tsugu_api
from ...utils import server_exists, n_2_i, i_2_n, ns_2_is, is_2_ns
from tsugu_api._typing import _ServerId, _Update

from ...utils import text_response, UserLocal
from ...command_matcher import MC

from ..db import db_manager, get_user_data


def handler(user: UserLocal, res: MC, platform: str, channel_id: str):
    # 无参数
    if not res.args:
        # 默认情况1: 优先当前服务器
        for i in user.game_ids:
            if i.get("server") == user.server_mode:
                player_id = str(i.get("game_id"))
                server = int(i.get("server"))
                text = f'已查找默认服务器 {config._server_index_to_name[str(server)]} 的记录'
                msg = [text_response(text), tsugu_api.search_player(int(player_id), server)]
                return msg
        else:
            # 默认情况2: 优先第一个记录
            if len(user.game_ids) > 0:
                player_id = str(user.game_ids[0].get("game_id"))
                server = int(user.game_ids[0].get("server"))
                text = f'已查找第一个记录 {player_id}'
                msg = [text_response(text), tsugu_api.search_player(int(player_id), server)]
                return msg
            else:
                return text_response('未绑定任何记录')

    # 查询指定服务器的玩家状态
    server: _ServerId = n_2_i(res.args[0])
    if server_exists(server):
        for i in user.game_ids:
            if i.get("server") == server:
                player_id = str(i.get("game_id"))
                text = f'已查找指定服务器 {i_2_n(server)} 的记录'
                msg = tsugu_api.search_player(int(player_id), server) + text_response(text)
                return msg
        else:
            return text_response(
                f'未在 {len(user.game_ids)} 条记录中找到 {i_2_n(server)} 的记录')

    # 查询指定记录顺序的玩家状态
    if res.args[0].isdigit():
        if int(res.args[0]) > len(user.game_ids) or int(res.args[0]) < 1:
            return text_response(f'未找到记录 {res.args[0]}')
        player_id = str(user.game_ids[int(res.args[0]) - 1].get("game_id"))
        server = int(user.game_ids[int(res.args[0]) - 1].get("server"))
        text = f'已查找第 {res.args[0]} 条记录'
        msg = tsugu_api.search_player(int(player_id), server) + text_response(text)
        return msg

    return text_response('请确保输入是 服务器名(字母缩写) 或者 记录(数字)')



