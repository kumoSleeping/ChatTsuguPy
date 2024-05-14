from ...config import config
from ...utils import text_response, User, server_name_2_server_id, server_exists
from ...command_matcher import MC
import tsugu_api_async


async def handler(user: User, res: MC, platform: str, channel_id: str):
    if res.args:
        if server_exists(server_name_2_server_id(res.text)):
            user.server_mode = server_name_2_server_id(res.args[0])
    return await tsugu_api_async.song_meta(user.default_server, user.server_mode)

