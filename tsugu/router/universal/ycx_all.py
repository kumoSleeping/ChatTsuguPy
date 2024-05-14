from ...config import config
from ...utils import text_response, User, server_exists, server_name_2_server_id
from ...command_matcher import MC
import tsugu_api


def handler(user: User, res: MC, platform: str, channel_id: str):
    # 无参数
    if not res.args:
        return tsugu_api.ycx_all(user.server_mode)

    # 一个参数
    if len(res.args) == 1:
        # 两个参数都是数字
        if res.args[0].isdigit():
            if res.args[0].isdigit():
                event_id: int = int(res.args[0])
            else:
                return text_response('请输入正确的活动ID')
            return tsugu_api.ycx_all(user.server_mode, event_id)
        elif server_exists(server_pre := server_name_2_server_id(res.args[0])):
            user.server_mode = server_pre
            return tsugu_api.ycx_all(user.server_mode)
        else:
            return text_response('请输入正确的活动ID或服务器名称字母简写')

    if len(res.args) == 2:
        # 两个参数是 event_id server_mode
        if res.args[0].isdigit():
            event_id: int = int(res.args[0])
        else:
            return text_response('第一个参数请输入正确的活动ID')
        if server_exists(server_pre := server_name_2_server_id(res.args[1])):
            user.server_mode = server_pre
            return tsugu_api.ycx_all(user.server_mode, event_id)
        else:
            return text_response('第二个参数请输入正确的服务器名称字母简写')

    return text_response('参数过多(<=2)')
