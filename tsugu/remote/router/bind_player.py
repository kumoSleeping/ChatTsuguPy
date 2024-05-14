from ...config import config
from ...utils import text_response, User
from ...command_matcher import MC
import tsugu_api
from ...utils import server_exists, server_name_2_server_id, server_id_2_server_name


def handler(user: User, res: MC, platform: str, channel_id: str):
    if res.args:
        server_pre = server_name_2_server_id(res.args[0])
        if not server_exists(server_pre):
            return text_response('未找到服务器，请输入正确的服务器名')
        user.server_mode = server_pre
    # 获取绑定请求
    r = tsugu_api.bind_player_request(platform, user.user_id, user.server_mode, True)
    if r.get('status') != 'success':
        return text_response(r.get('data'))
    return text_response(
        f'''正在绑定账号，请将 评论(个性签名) 或者 当前使用的 乐队编队名称改为\n{r.get('data')['verifyCode']}\n稍等片刻等待同步后，发送\n验证 你的玩家ID(数字) {server_id_2_server_name(user.server_mode)}\n''')

