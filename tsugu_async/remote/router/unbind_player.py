from ...utils import text_response, User
from ...command_matcher import MC
import tsugu_api_async
from ...utils import server_exists, server_name_2_server_id, server_id_2_server_name


async def handler(user: User, res: MC, platform: str, channel_id: str):
    if res.args:
        server_pre = server_name_2_server_id(res.args[0])
        if not server_exists(server_pre):
            return text_response('未找到服务器，请输入正确的服务器名')
        user.server_mode = server_pre
        if not user.server_list[user.server_mode]['playerId']:
            return text_response('未绑定玩家，请先绑定玩家')
    r = await tsugu_api_async.bind_player_request(platform, user.user_id, user.server_mode, False)
    if r.get('status') != 'success':
        return text_response(r.get('data'))
    # 如果是200
    return text_response(
        f'''正在解除，请将 评论(个性签名) 或者 当前使用的 乐队编队名称改为\n{r.get('data')['verifyCode']}\n稍等片刻等待同步后，发送\n验证解绑 {server_id_2_server_name(user.server_mode)}\n来完成本次身份验证''')


