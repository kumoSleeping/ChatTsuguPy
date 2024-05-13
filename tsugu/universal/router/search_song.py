from ...config import config
from ...utils import text_response, User
from ...command_matcher import MC
import tsugu_api


def handler(user: User, res: MC, platform: str, channel_id: str):
    if not res.args:
        return text_response('请输入歌曲名，乐队，歌曲ID等查询参数')
    return tsugu_api.search_song(user.default_server, res.text)

