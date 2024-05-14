from ...config import config
from ...utils import text_response, User
from ...command_matcher import MC
import tsugu_api_async
from tsugu_api_async._typing import _Update


async def handler(user: User, res: MC, platform: str, channel_id: str):
    update: _Update = {'car': True, }
    r = await tsugu_api_async.change_user_data(platform, user.user_id, update)
    return text_response('已开启车牌转发') if r.get('status') == 'success' else None


