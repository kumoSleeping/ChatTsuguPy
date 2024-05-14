from ...config import config
from ...utils import text_response, UserLocal
from ...command_matcher import MC
# import tsugu_api
from ...user_data.db import db_manager
import json
import random


def generate_verify_code():
    # 不包含64和89的随机数
    while True:
        verify_code = random.randint(10000, 99999)
        if '64' not in str(verify_code) and '89' not in str(verify_code):
            return verify_code


def handler(user: UserLocal, res: MC, platform: str, channel_id: str):
    # 获取绑定请求
    cursor = db_manager.conn.cursor()
    verify_code = generate_verify_code()
    cursor.execute("UPDATE users SET verify_code = ? WHERE user_id = ? AND platform = ?", (verify_code, user.user_id, platform))
    db_manager.conn.commit()
    f'''正在绑定第{len(user.game_ids) + 1}个记录，请将 评论(个性签名) 或者 当前使用的 乐队编队名称改为\n{verify_code}\n稍等片刻等待同步后，发送\n验证 玩家ID 来完成本次身份验证\n例如：验证 10000xxxx 国服'''