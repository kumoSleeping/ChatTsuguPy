from ...config import config
from ...utils import text_response, User, server_exists
from ...command_matcher import MC
import tsugu_api


def handler(user: User, res: MC, platform: str, channel_id: str):
    if res.args:
        #     最后一个参数
        # if server_exists(name_2_index(res.args[-1])):
        #     user.server_mode = name_2_index(res.args[-1])
        event_id_pre: str = res.args[0]
        # if event_id_pre.isdigit():
        #     event_id = int(event_id_pre)
        #     return tsugu_api.event_stage(user.server_mode, event_id=event_id, meta=False)
        if res.text == '-m':
            return tsugu_api.event_stage(user.server_mode, meta=True)

    return tsugu_api.event_stage(user.server_mode, meta=False)
