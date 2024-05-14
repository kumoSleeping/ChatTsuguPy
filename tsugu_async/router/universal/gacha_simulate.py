from ...config import config
from ...utils import text_response, User
from ...command_matcher import MC
import tsugu_api_async


async def handler(user: User, res: MC, platform: str, channel_id: str):
    if res.args:
        if len(res.args) == 1:
            if res.args[0].isdigit():
                times = int(res.args[0])
                return await tsugu_api_async.gacha_simulate(user.server_mode, times=times)
            else:
                return text_response('请输入正确的次数')
        elif len(res.args) == 2:
            if res.args[0].isdigit() and res.args[1].isdigit():
                times = int(res.args[0])
                gacha_id = int(res.args[1])
                return await tsugu_api_async.gacha_simulate(user.server_mode, times=times, gacha_id=gacha_id)
            else:
                return text_response('请输入正确的次数和卡池ID')
    return await tsugu_api_async.gacha_simulate(user.server_mode)

