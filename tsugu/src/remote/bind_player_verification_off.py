from ...utils import get_user, text_response, User, server_id_2_server_name, server_name_2_server_id, get_user_async
import tsugu_api
import tsugu_api_async

from arclet.alconna import Alconna, Option, Subcommand, Args, CommandMeta, Empty, Namespace, namespace, command_manager


alc = Alconna(
        ["验证解绑"],
        Args["index#要解绑的绑定编号", int],
        meta=CommandMeta(
            compact=True,
            description="验证解绑",
            usage="验证解绑 记录编号(数字)",
            example="验证解绑 1 : 解绑第一个记录"
        ),
    )


def handler(message: str, user_id: str, platform: str):
    res = alc.parse(message)

    if res.matched:
        user = get_user(user_id, platform)
        if len(user.user_player_list) < int(res.index):
            return text_response('未找到记录')
        player_id = user.user_player_list[int(res.index) - 1].get("playerId")
        server_mode = user.user_player_list[int(res.index) - 1].get("server")
        try:
            r = tsugu_api.bind_player_verification(platform, user.user_id, server_mode, player_id, 'unbind')
            return text_response('解绑成功！')
        except Exception as e:
            return text_response(str(e))
    
    return res


async def handler_async(message: str, user_id: str, platform: str):
    res = alc.parse(message)

    if res.matched:
        user = await get_user_async(user_id, platform)
        if len(user.user_player_list) < int(res.index):
            return text_response('未找到记录')
        player_id = user.user_player_list[int(res.index) - 1].get("playerId")
        server_mode = user.user_player_list[int(res.index) - 1].get("server")
        try:
            r = await tsugu_api_async.bind_player_verification(platform, user.user_id, server_mode, player_id, 'unbind')
            return text_response('解绑成功！')
        except Exception as e:
            return text_response(str(e))

    return res

