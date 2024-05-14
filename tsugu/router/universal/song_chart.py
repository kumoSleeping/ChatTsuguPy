from ...config import config
from ...utils import text_response, User
from ...command_matcher import MC
import tsugu_api

from tsugu_api._typing import _DifficultyText


def handler(user: User, res: MC, platform: str, channel_id: str):
    if not res.args:
        return text_response('请输入查询参数: 歌曲ID')
    if not res.args[0].isdigit():
        return text_response('请输入正确的歌曲ID(数字)')
    if len(res.args) > 1:
        # 难度符合 _DifficultyText
        if not res.args[1] in ['easy', 'normal', 'hard', 'expert', 'special']:
            return text_response(f'请输入正确的难度(easy, normal, hard, expert, special)')
        return tsugu_api.song_chart(user.default_server, int(res.args[0]), res.args[1])
    elif len(res.args) == 1:
        difficulty: _DifficultyText = 'expert'
        return tsugu_api.song_chart(user.default_server, int(res.args[0]), difficulty)
    return text_response('参数错误')

