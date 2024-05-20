from ...utils import text_response, User, server_id_2_server_name, server_name_2_server_id, server_exists
import tsugu_api_async
from ...config import config
from arclet.alconna import Alconna, Option, Subcommand, Args, CommandMeta, Empty, Namespace, namespace, command_manager
from tsugu_api_core._typing import _ServerName


alc = Alconna(
        ["解除绑定"],
    Args["index#要解绑的绑定编号", int, None],
        meta=CommandMeta(
            compact=config.compact, description="解除绑定",
            usage="验证解绑 记录编号(数字)",
            example="验证解绑 1 : 解绑第一个记录"
        ),
    )


async def handler(message: str, user: User, platform: str, channel_id: str):
    res = alc.parse(message)

    if res.matched:
        if not res.index:
            bind_record = '\n'.join([f'{i + 1}. {mask_data(x.get("game_id"))} {server_id_2_server_name(x.get("server"))}' for i, x in enumerate(user.game_ids)])
            return text_response('请输入正确的记录(数字)\n例如: 解除绑定 1\n当前的绑定记录如下:\n' + bind_record)

        if len(user.game_ids) < int(res.index):
            return text_response('未找到记录')

        server_mode = user.game_ids[int(res.index) - 1].get("server")

        r = await tsugu_api_async.bind_player_request(platform, user.user_id, server_mode, False)
        if r.get('status') != 'success':
            return text_response(r.get('data'))
        return text_response(f'''正在解除，请将 评论(个性签名) 或者 当前使用的 乐队编队名称改为\n{r.get('data')['verifyCode']}\n稍等片刻等待同步后，发送\n验证解绑 {res.index}\n来完成本次身份验证''')
    elif res.head_matched:
        return text_response(res.error_info)
    return None


def mask_data(game_id: str):
    game_id = str(game_id)
    if len(game_id) < 6:
        return game_id[:3] + '*' * (len(game_id) - 3)
    elif len(game_id) < 3:
        return '*' * len(game_id)
    else:
        game_id = game_id[:3] + '*' * (len(game_id) - 6) + game_id[-3:]
    return game_id

