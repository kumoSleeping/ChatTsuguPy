from ..utils import User, UserLocal
from ..command_matcher import match_command
from ..config import config
from . import router
from .help import help_command
from ..user_data import db
from ..user_data import remote_db
from .rooms_forward import submit_rooms


def _get_user(user_id: str, platform: str, loacl=False):
    if loacl:
        user = db.get_user(user_id, platform)
    else:
        user = remote_db.get_user(user_id, platform)
    return user


def universal_api_handler(user_id: str, message: str,  platform: str, channel_id: str, loacl=False):
    for i in config.commands:
        if res := match_command(message, commands=i['command_name']):
            api = i['api']
            user = _get_user(user_id, platform, loacl)
            return router.api_handler(user, res, api, platform, channel_id)
    # 开始匹配 help
    if res := match_command(message, commands=['help']):
        return help_command(res)
        # 开始上传车牌
    if res := match_command(message, commands=['上传车牌', '']):
        user = _get_user(user_id, platform, loacl)
        submit_rooms(res, user, platform)
    return None


