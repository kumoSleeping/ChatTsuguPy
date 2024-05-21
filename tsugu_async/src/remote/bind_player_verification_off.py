from ...utils import text_response, User, server_id_2_server_name, server_name_2_server_id, server_exists, config
import tsugu_api_async
from arclet.alconna import Alconna, Option, Subcommand, Args, CommandMeta, Empty, Namespace, namespace, command_manager


async def handler(message: str, user: User, platform: str, channel_id: str):
    res = Alconna(
        ["验证解绑"],
        Args["index#要解绑的绑定编号", int],
        meta=CommandMeta(
            compact=config.compact, description="验证解绑",
            usage="验证解绑 记录编号(数字)",
            example="验证解绑 1 : 解绑第一个记录"
        ),
    ).parse(message)

    if res.matched:
        if len(user.game_ids) < int(res.index):
            return text_response('未找到记录')
        player_id = user.game_ids[int(res.index) - 1].get("game_id")
        server_mode = user.game_ids[int(res.index) - 1].get("server")
        r = await tsugu_api_async.bind_player_verification(platform, user.user_id, server_mode, player_id, False)
        if r.get('status') != 'success':
            return text_response(r.get('data'))
        return text_response('解绑成功！')
    
    return res


