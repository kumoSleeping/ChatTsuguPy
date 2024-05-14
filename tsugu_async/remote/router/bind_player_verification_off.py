from ...utils import text_response, User
from ...command_matcher import MC
import tsugu_api_async
from ...utils import server_exists, server_name_2_server_id
from loguru import logger


async def handler(user: User, res: MC, platform: str, channel_id: str):
    if not res.args:
        return text_response('请输入正确的服务器名参数')
    server_pre = server_name_2_server_id(res.args[0])
    if not server_exists(server_pre):
        return text_response('未找到服务器，请输入正确的服务器名')
    player_id = int(user.server_list[server_pre]['playerId'])

    r = await tsugu_api_async.bind_player_verification(platform, user.user_id, server_pre, player_id, False)
    if r.get('status') != 'success':
        logger.error(r.get('data'))
        return text_response(r.get('data'))
    return text_response('解绑成功')


