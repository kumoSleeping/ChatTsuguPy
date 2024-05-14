from ...config import config
from ...utils import text_response, User
from ...command_matcher import MC
import tsugu_api


def handler(user: User, res: MC, platform: str, channel_id: str):
    if not res.args:
        return text_response('请输入活动名，乐队，活动ID等查询参数，可以使用>225查询大于225的活动')
    return tsugu_api.search_event(user.default_server, res.text)

