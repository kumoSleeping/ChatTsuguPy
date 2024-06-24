from ...utils import get_user, text_response, User, server_id_2_server_name, server_name_2_server_id, get_user_async
import tsugu_api
import tsugu_api_async

from arclet.alconna import Alconna, Option, Subcommand, Args, CommandMeta, Empty, Namespace, namespace, command_manager



alc = Alconna(
        ["查试炼", '查stage', '查舞台', '查festival', '查5v5'],
        Args["eventId;?#省略活动ID时查询当前活动。", [int]]["meta;?#歌曲meta。", ['-m']],

        meta=CommandMeta(
            compact=True,
            description="查试炼",
            usage='查询当前服务器当前活动试炼信息。',
            example='''查试炼 157 -m :返回157号活动的试炼信息，包含歌曲meta。
查试炼 -m :返回当前活动的试炼信息，包含歌曲meta。
查试炼 :返回当前活动的试炼信息。'''
        )
    )


def handler(message: str, user_id: str, platform: str, channel_id: str):
    res = alc.parse(message)

    if res.matched:
        user = get_user(user_id, platform)
        if res.meta:
            meta = True
        else:
            meta = False
        return tsugu_api.event_stage(user.server_mode, res.eventId, meta)

    return res


async def handler_async(message: str, user_id: str, platform: str, channel_id: str):
    res = alc.parse(message)

    if res.matched:
        user = await get_user_async(user_id, platform)
        if res.meta:
            meta = True
        else:
            meta = False
        return await tsugu_api_async.event_stage(user.server_mode, res.eventId, meta)

    return res

