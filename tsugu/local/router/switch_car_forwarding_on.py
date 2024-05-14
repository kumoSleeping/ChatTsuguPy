from ...utils import text_response, User
from ...command_matcher import MC

from ...storage.db import db_manager


def handler(user: User, res: MC, platform: str, channel_id: str):
    cursor = db_manager.conn.cursor()
    cursor.execute("UPDATE users SET car = ? WHERE user_id = ? AND platform = ?", (False, user.user_id, platform))
    db_manager.conn.commit()
    return text_response('车牌转发已关闭')



