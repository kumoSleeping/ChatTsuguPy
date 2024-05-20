from ...utils import text_response, User, server_name_2_server_id
import tsugu_api_async
from ...config import config
from arclet.alconna import Alconna, Option, Subcommand, Args, CommandMeta, Empty, Namespace, namespace, command_manager
from tsugu_api_core._typing import _ServerName


alc = Alconna(
        ["查试炼", '查stage', '查舞台', '查festival', '查5v5'],
        Args["eventId;?#省略活动ID时查询当前活动。", [int]]["meta;?#歌曲meta。", ['-m']],

        meta=CommandMeta(
            compact=config.compact, description="查试炼",
            usage='查询当前服务器当前活动试炼信息。',
            example='''查试炼 157 -m :返回157号活动的试炼信息，包含歌曲meta。
查试炼 -m :返回当前活动的试炼信息，包含歌曲meta。
查试炼 :返回当前活动的试炼信息。'''
        )
    )

async def handler(message: str, user: User, platform: str, channel_id: str):
    res = alc.parse(message)

    if res.matched:
        if res.meta:
            meta = True
        else:
            meta = False
        print(meta)
        return await tsugu_api_async.event_stage(user.server_mode, res.eventId, meta)
    elif res.head_matched:
        return text_response(res.error_info)
    return None
