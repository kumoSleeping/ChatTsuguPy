from ...config import config
from ...utils import text_response, User
from ...command_matcher import MC
import tsugu_api_async
from ...utils import server_exists, server_name_2_server_id


async def handler(user: User, res: MC, platform: str, channel_id: str):
    if not res.args or len(res.args) < 2:
        return text_response('请输入正确的格式：验证绑定 你的玩家ID(数字) 服务器名(字母缩写)')
    player_id = int(res.args[0])
    server_pre = server_name_2_server_id(res.args[1])
    if not server_exists(server_pre):
        return text_response('未找到服务器，请输入正确的服务器名')
    user.server_mode = server_pre

    r = await tsugu_api_async.bind_player_verification(platform, user.user_id, user.server_mode, player_id, True)
    if r.get('status') != 'success':
        return text_response(r.get('data'))
    return text_response(f'绑定成功！现在可以使用 玩家状态 {len(user.game_ids) + 1} 查看绑定的玩家状态')



