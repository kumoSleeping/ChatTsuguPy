from ...config import config
from ...utils import text_response, User
from ...command_matcher import MC
import tsugu_api_async
from ...utils import server_exists, server_name_2_server_id


async def handler(user: User, res: MC, platform: str, channel_id: str):
    if not res.args:
        return text_response('请输入正确的玩家ID和服务器名参数(可选)')
    if not res.args[0].isdigit():
        return text_response('请输入正确的玩家ID')
    player_id = int(res.args[0])
    if len(res.args) > 1:
        server_pre = server_name_2_server_id(res.args[1])
        if not server_exists(server_pre):
            return text_response('未找到服务器，请输入正确的服务器名')
        user.server_mode = server_pre

    r = await tsugu_api_async.bind_player_verification(platform, user.user_id, user.server_mode, player_id, True)
    if r.get('status') != 'success':
        return text_response(r.get('data'))
    return text_response('绑定成功')

    # 车牌转发控制


