from ...utils import get_user, text_response, User, server_id_2_server_name, server_name_2_server_id
import tsugu_api
from arclet.alconna import Alconna, Option, Subcommand, Args, CommandMeta, Empty, Namespace, namespace, command_manager
import tsugu_api_async


alc = Alconna(
        ["关闭车牌转发", "关闭个人车牌转发"],
        meta=CommandMeta(
            compact=True,
            description="关闭车牌转发",)
    )


def handler(message: str, user_id: str, platform: str, channel_id: str):
    res = alc.parse(message)

    if res.matched:
        user = get_user(user_id, platform)
        update = {'car': False, }
        r = tsugu_api.change_user_data(platform, user.user_id, update)
        if r.get('status') != 'success':
            return text_response(r.get('data'))
        return text_response('关闭车牌转发成功！')
    return res


async def handler_async(message: str, user_id: str, platform: str, channel_id: str):
    res = alc.parse(message)

    if res.matched:
        user = get_user(user_id, platform)
        update = {'car': False, }
        r = await tsugu_api_async.change_user_data(platform, user.user_id, update)
        if r.get('status') != 'success':
            return text_response(r.get('data'))
        return text_response('关闭车牌转发成功！')
    return res



