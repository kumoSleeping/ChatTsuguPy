from ...config import config
from ...utils import text_response, User
from ...command_matcher import MC
import tsugu_api
from ...utils import server_exists, server_name_2_server_id, server_id_2_server_name
from tsugu_api._typing import _ServerId


def mask_data(game_id: str):
    game_id = str(game_id)
    if len(game_id) < 6:
        return game_id[:3] + '*' * (len(game_id) - 3)
    elif len(game_id) < 3:
        return '*' * len(game_id)
    else:
        game_id = game_id[:3] + '*' * (len(game_id) - 6) + game_id[-3:]
    return game_id


def handler(user: User, res: MC, platform: str, channel_id: str):
    bind_record = '\n'.join(
        [f'{i + 1}. {mask_data(x.get("game_id"))} {server_id_2_server_name(x.get("server"))}' for i, x in
         enumerate(user.game_ids)])
    if not res.args:
        return text_response(f'请输入正确的记录(数字)\n例如: 解除绑定 1\n当前的绑定记录如下:\n{bind_record}')

    if not res.args[0].isdigit():
        return text_response(f'请输入正确的记录(数字)\n例如: 解除绑定 1\n当前的绑定记录如下:\n{bind_record}')

    if int(res.args[0]) > len(user.game_ids):
        return text_response(f'未找到记录 {res.args[0]}，当前的绑定记录如下:\n{bind_record}')

    server_mode = user.game_ids[int(res.args[0]) - 1].get("server")
    r = tsugu_api.bind_player_request(platform, user.user_id, server_mode, False)
    if r.get('status') != 'success':
        return text_response(r.get('data'))
    # 如果是200
    return text_response(
        f'''正在解除，请将 评论(个性签名) 或者 当前使用的 乐队编队名称改为\n{r.get('data')['verifyCode']}\n稍等片刻等待同步后，发送\n验证解绑 {res.args[0]}\n来完成本次身份验证''')
