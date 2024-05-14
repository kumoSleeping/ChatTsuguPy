from ...config import config
from ...utils import text_response, User
from ...command_matcher import MC
import tsugu_api_async


async def handler(user: User, res: MC, platform: str, channel_id: str):
    if not res.args:
        return text_response('请输入角色名，乐队，昵称等查询参数')
    return await tsugu_api_async.search_character(default_servers=user.default_server, text=res.text)


