from ...config import config
from ...utils import text_response, UserLocal
from ...command_matcher import MC
from ...utils import server_names_2_server_ids, server_ids_2_server_names
import json
from ...storage.db import db_manager


def handler(user: UserLocal, res: MC, platform: str, channel_id: str):
    default_server = server_names_2_server_ids(res.args)
    if not default_server:
        return text_response('未找到服务器，请输入正确的服务器名')
    cursor = db_manager.conn.cursor()
    cursor.execute("UPDATE users SET default_server = ? WHERE user_id = ? AND platform = ?",
                   (json.dumps(default_server), user.user_id, platform))
    db_manager.conn.commit()
    return text_response(f'默认服务器设置为 {server_ids_2_server_names(default_server)}')