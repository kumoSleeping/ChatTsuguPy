from ...config import config
from ...utils import text_response, User
from ...utils import server_exists , ns_2_is, n_2_i
from ...command_matcher import MC
import tsugu_api


def handler(user: User, res: MC, platform: str, channel_id: str):
    # 无参数
    if not res.args:
        return text_response('请输入档位线')

    # 一个参数
    if res.args[0].isdigit():
        tier: int = int(res.args[0])
    else:
        return text_response('请输入正确的档位线')

    if len(res.args) == 1:
        return tsugu_api.lsycx(user.server_mode, tier)

    # 两个参数
    if len(res.args) == 2:
        # 两个参数都是数字
        if res.args[1].isdigit():
            if res.args[1].isdigit():
                event_id: int = int(res.args[1])
            else:
                return text_response('请输入正确的活动ID')
            return tsugu_api.lsycx(user.server_mode, tier, event_id)
        elif server_exists(server_pre := n_2_i(res.args[1])):
            user.server_mode = server_pre
            return tsugu_api.lsycx(user.server_mode, tier)
        else:
            return text_response('请输入正确的活动ID或服务器名称字母简写')

    if len(res.args) == 3:
        # 三个参数是 tier event_id server_mode
        if res.args[1].isdigit():
            if res.args[1].isdigit():
                event_id: int = int(res.args[1])
            else:
                return text_response('第二个参数请输入正确的活动ID')
            if server_exists(server_pre := n_2_i(res.args[2])):
                user.server_mode = server_pre
                return tsugu_api.ycx(user.server_mode, tier, event_id)
            else:
                return text_response('第三个参数请输入正确的服务器名称字母简写')

    return text_response('参数过多(<=3)')

