from ...config import config
from ...utils import text_response, User, server_exists, n_2_i
from ...command_matcher import MC
import tsugu_api


def handler(user: User, res: MC, platform: str, channel_id: str):
    if not res.args:
        return text_response('请输入玩家ID')

    if len(res.args) == 1:
        if not res.args[0].isdigit():
            return text_response('请输入正确的玩家ID(数字)')
        player_id = int(res.args[0])

        return tsugu_api.search_player(player_id, user.server_mode)

    if len(res.args) == 2:
        if not res.args[0].isdigit():
            return text_response('请输入正确的玩家ID(数字)')
        player_id = int(res.args[0])
        if not server_exists(n_2_i(res.args[1])):
            return text_response('请输入正确的服务器ID(数字)')
        server_id = n_2_i(res.args[1])

        return tsugu_api.search_player(player_id, server_id)# type: ignore
    return text_response('功能暂未开放')

