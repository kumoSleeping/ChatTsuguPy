from ...config import config
from ...utils import text_response, UserLocal
from ...command_matcher import MC
import tsugu_api
from ...utils import server_exists, n_2_i
from tsugu_api._typing import _ServerId

from ..db import db_manager, get_user_data


def handler(user: UserLocal, res: MC, platform: str, channel_id: str):
    if not res.args:
        return text_response('请输入正确的记录(数字)\n例如: 解除绑定 1')
    if not res.args[0].isdigit():
        return text_response('请输入正确的记录(数字)')
    now_game_ids = user.game_ids
    # 检测是否存在该记录
    if int(res.args[0]) > len(now_game_ids):
        return text_response(f'未找到记录 {res.args[0]}')
    exe_game_id = user.game_ids.pop(int(res.args[0]) - 1)

    cursor = db_manager.conn.cursor()
    cursor.execute("UPDATE users SET game_ids = ? WHERE user_id = ? AND platform = ?",
                   (str(now_game_ids), user.user_id, platform))
    db_manager.conn.commit()

    return text_response(f'已解除绑定 {exe_game_id.get("game_id")}')

