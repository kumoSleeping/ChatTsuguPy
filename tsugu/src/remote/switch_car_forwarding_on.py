from ...utils import get_user, text_response, User, server_id_2_server_name, server_name_2_server_id, get_user_async
import tsugu_api
import tsugu_api_async

from arclet.alconna import Alconna, Option, Subcommand, Args, CommandMeta, Empty, Namespace, namespace, command_manager


alc = Alconna(
        ["开启车牌转发", "开启个人车牌转发"],
        meta=CommandMeta(
            compact=True,
            description="开启车牌转发",)
    )


def handler(message: str, user_id: str, platform: str):
    res = alc.parse(message)

    if res.matched:
        user = get_user(user_id, platform)
        update = {'shareRoomNumber': True, }
        try:
            r = tsugu_api.change_user_data(platform, user.user_id, update)
            return text_response('开启车牌转发成功！')
        except Exception as e:
            return text_response(e)

    return res


async def handler_async(message: str, user_id: str, platform: str):
    res = alc.parse(message)

    if res.matched:
        user = await get_user_async(user_id, platform)
        update = {'shareRoomNumber': True, }
        try:
            r = await tsugu_api_async.change_user_data(platform, user.user_id, update)
            return text_response('开启车牌转发成功！')
        except Exception as e:
            return text_response(e)

    return res


