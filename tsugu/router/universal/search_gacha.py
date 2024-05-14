from ...config import config
from ...utils import text_response, User
from ...command_matcher import MC
import tsugu_api


def handler(user: User, res: MC, platform: str, channel_id: str):
    if not res.args:
        return text_response('请输入卡池ID(数字)')
    if not res.args[0].isdigit():
        return text_response('请输入正确的卡池ID(数字)')
    gacha_id: int = int(res.args[0])

    return tsugu_api.search_gacha(user.default_server, gacha_id)

