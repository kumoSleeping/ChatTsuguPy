from ...config import config
from ...utils import text_response, User, n_2_i, server_exists
from ...command_matcher import MC
import tsugu_api


def handler(user: User, res: MC, platform: str, channel_id: str):
    if res.args:
        if server_exists(n_2_i(res.text)):
            user.server_mode = n_2_i(res.args[0])
    return tsugu_api.song_meta(user.default_server, user.server_mode)# type: ignore

