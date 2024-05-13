from ...config import config
from ...utils import text_response, UserLocal
from ...command_matcher import MC
import tsugu_api
from ...utils import server_exists, ns_2_is, is_2_ns
from tsugu_api._typing import _Update
import json
from ..db import db_manager
from ...utils import i_2_n


def handler(user: UserLocal, res: MC, platform: str, channel_id: str):
    default_server = ns_2_is(res.args)
    if not default_server:
        return text_response('未找到服务器，请输入正确的服务器名')
    cursor = db_manager.conn.cursor()
    cursor.execute("UPDATE users SET default_server = ? WHERE user_id = ? AND platform = ?",
                   (json.dumps(default_server), user.user_id, platform))
    db_manager.conn.commit()
    return text_response(f'默认服务器设置为 {is_2_ns(default_server)}')