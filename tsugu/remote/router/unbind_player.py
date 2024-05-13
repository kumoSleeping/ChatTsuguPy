from ...config import config
from ...utils import text_response, User
from ...command_matcher import MC
import tsugu_api
from ...utils import server_exists, n_2_i
from tsugu_api._typing import _ServerId


def handler(user: User, res: MC, platform: str, channel_id: str):
    if res.args:
        server_pre = n_2_i(res.args[0])
        if not server_exists(server_pre):
            return text_response('未找到服务器，请输入正确的服务器名')
        user.server_mode: _ServerId = server_pre
        if not user.server_list[user.server_mode]['playerId']:
            return text_response('未绑定玩家，请先绑定玩家')
    r = tsugu_api.bind_player_verification(platform, user.user_id, user.server_mode,
                                           user.server_list[user.server_mode]['playerId'], False)
    if r.get('status') != 'success':
        return text_response(r.get('data'))
    # 如果是200
    return text_response(
        f'''正在解除，请将 评论(个性签名) 或者 当前使用的 乐队编队名称改为\n{r.get('data')['verifyCode']}\n稍等片刻等待同步后，发送\n验证解绑 {user.server_mode}\n来完成本次身份验证(用 {user.server_mode} 来确定需要解绑的服务器)''')


