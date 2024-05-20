from ...utils import text_response, User
import tsugu_api
from ...config import config
from arclet.alconna import Alconna, Option, Subcommand, Args, CommandMeta, Empty, Namespace, namespace, command_manager


difficulty_text_tuple = ('easy', 'ez', 'normal', 'nm', 'hard', 'hd', 'expert', 'ex', 'special', 'sp')

alc = Alconna(
        ["查谱面", "查铺面"],
        Args["songId", int]['difficultyText', difficulty_text_tuple, 'ex'],
        meta=CommandMeta(
            compact=config.compact, description="查谱面",
            usage='根据曲目ID与难度查询铺面信息。',
            example='''查谱面 1 :返回1号曲的ex难度谱面
查谱面 128 special :返回128号曲的special难度谱面'''
        )
    )


def handler(message: str, user: User, platform: str, channel_id: str):
    res = alc.parse(message)

    if res.matched:
        return tsugu_api.song_chart(user.default_server, res.songId, res.difficultyText)
    elif res.head_matched:
        return text_response(res.error_info)
    return None



