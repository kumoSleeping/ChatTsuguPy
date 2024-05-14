from ...config import config
from ...utils import text_response, User
from ...command_matcher import MC
import tsugu_api_async


async def handler(user: User, res: MC, platform: str, channel_id: str):
    if not res.args:
        return text_response('请输入卡面ID')
    if res.args[0].isdigit():
        card_id = int(res.args[0])
        return await tsugu_api_async.get_card_illustration(card_id)
    return text_response('请输入正确的卡面ID')
