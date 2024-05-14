from ...utils import text_response, User
from ...command_matcher import MC
import tsugu_api_async
from ...utils import server_exists, server_name_2_server_id
from loguru import logger


async def handler(user: User, res: MC, platform: str, channel_id: str):
    if not res.args or len(res.args) > 1:
        return text_response('请输入正确的格式：验证解绑 记录编号(数字)')
    if not res.args[0].isdigit():
        return text_response('请输入正确的格式：验证解绑 记录编号(数字)')
    if int(res.text) <= 0:
        return text_response('请输入正确的格式：验证解绑 记录编号(数字)，编号从1开始')
    if len(user.game_ids) < int(res.text):
        return text_response('未找到记录')
    player_id = user.game_ids[int(res.args[0]) - 1].get("game_id")
    server_mode = user.game_ids[int(res.args[0]) - 1].get("server")
    r = await tsugu_api_async.bind_player_verification(platform, user.user_id, server_mode, player_id, False)
    if r.get('status') != 'success':
        return text_response(r.get('data'))
    return text_response('解绑成功！')


