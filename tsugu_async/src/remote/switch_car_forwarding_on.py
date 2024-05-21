from ...utils import text_response, User, server_id_2_server_name, server_name_2_server_id, server_exists, config
import tsugu_api_async
from arclet.alconna import Alconna, Option, Subcommand, Args, CommandMeta, Empty, Namespace, namespace, command_manager


async def handler(message: str, user: User, platform: str, channel_id: str):
    res = Alconna(
        ["开启车牌转发", "开启个人车牌转发"],
        meta=CommandMeta(
            compact=config.compact, description="开启车牌转发",)
    ).parse(message)

    if res.matched:
        update = {'car': True, }
        r = await tsugu_api_async.change_user_data(platform, user.user_id, update)
        if r.get('status') != 'success':
            return text_response(r.get('data'))
        return text_response('开启车牌转发成功！')
    return res

