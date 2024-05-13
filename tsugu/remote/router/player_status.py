from ...config import config
from ...utils import text_response, User
from ...command_matcher import MC
import tsugu_api
from ...utils import server_exists, n_2_i, i_2_n, ns_2_is, is_2_ns
from tsugu_api._typing import _ServerId, _Update


def handler(user: User, res: MC, platform: str, channel_id: str):
    # 获取用户数据
    if not res.args:
        # 查询默认服务器的玩家状态
        return tsugu_api.search_player(server=user.server_mode,
                                       player_id=user.server_list[user.server_mode]['playerId'])
    else:
        # 查询指定服务器的玩家状态
        server: _ServerId = n_2_i(res.args[0])
        # 服务器不存在
        if not server_exists(server):
            return text_response('未找到服务器，请输入正确的服务器名')
        player_id = user.server_list[server]['playerId']
        # 未绑定玩家
        if not player_id:
            return text_response('未绑定玩家，请先绑定玩家')
        # 查询玩家状态
        return tsugu_api.search_player(server=server, player_id=user.server_list[server]['playerId'])
    return None




