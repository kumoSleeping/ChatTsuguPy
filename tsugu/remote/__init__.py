from ..utils import server_exists, load_commands_from_config, text_response, config
from ..utils import n_2_i, i_2_n, ns_2_is, is_2_ns
from ..command_matcher import match_command

from .. import utils
import typing
from typing import List
from loguru import logger
import tsugu_api
from tsugu_api._typing import _Update
from tsugu_api._typing import _ServerId
from ..universal import universal_api_handler
from ..utils import User

from . import router


def remote_api_handler(user: User, message: str,  platform: str, channel_id: str):
    for i in config.user_commands:
        if res := match_command(message, commands=i['command_name']):
            api = i['api']
            logger.info(f'调用 {api} 的 handler')
            return router.api_handler(user, res, api, platform, channel_id)

    return None


def handler(message, user_id, platform, channel_id):
    if config.features.get('car_number_forwarding'):
        # status = utils.submit_car_number_msg(message, user_id, platform)
        # if status:
        #     return None
        pass

    user_data_res = tsugu_api.get_user_data(platform, user_id)
    # 获取用户数据失败
    if user_data_res.get('status') == 'failed':
        return text_response(user_data_res.get('data'))
    # 构建用户对象
    user_data = user_data_res.get('data')
    user = utils.User(user_id, platform, user_data['server_mode'], user_data['default_server'], user_data['car'], user_data['server_list'])

    # 进行 api 命令匹配
    result = universal_api_handler(user, message, platform, channel_id)
    if result:
        return result

    # 远程命令
    result = remote_api_handler(user, message, platform, channel_id)
    if result:
        return result

