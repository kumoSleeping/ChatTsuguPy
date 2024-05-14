from ...config import config
from ...utils import text_response, User
from ...command_matcher import MC
import tsugu_api
from tsugu_api._typing import _Update


def handler(user: User, res: MC, platform: str, channel_id: str):
    update: _Update = {'car': False, }
    r = tsugu_api.change_user_data(platform, user.user_id, update)
    return text_response('已关闭车牌转发') if r.get('status') == 'success' else None

    # 切换服务器模式


