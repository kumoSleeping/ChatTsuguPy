from ..utils import User, UserLocal
from ..command_matcher import match_command
from ..config import config
from . import router
from .help import help_command
from ..storage import remote_db
from .rooms_forward import submit_rooms


async def _get_user(user_id: str, platform: str):
    user = await remote_db.get_user(user_id, platform)
    return user


async def universal_api_handler(user_id: str, message: str,  platform: str, channel_id: str):
    for i in config.commands:
        if res := match_command(message, commands=i['command_name']):
            api = i['api']
            user = await _get_user(user_id, platform)
            return await router.api_handler(user, res, api, platform, channel_id)

    # 开始匹配 help
    if res := match_command(message, commands=['help']):
        return await help_command(res)

    # 开始上传车牌
    if res := match_command(message, commands=['上传车牌', '']):
        await submit_rooms(res, user_id, platform)
    return None


