from ...config import config
from ...utils import text_response, UserLocal
from ...command_matcher import MC
# import tsugu_api
from ...utils import server_exists, n_2_i, i_2_n
from ..db import db_manager
import json
import random
from .. import utils as local_utils
from ..db import get_user_data, get_user_data


def bind_player_request(platform: str, user: UserLocal):

    cursor = db_manager.conn.cursor()

    bind_count = len(user.game_ids)

    def generate_verify_code():
        while True:
            verify_code = random.randint(10000, 99999)
            if '64' not in str(verify_code) and '89' not in str(verify_code):
                return verify_code
    # 不包含64和89的随机数

    verify_code = generate_verify_code()
    # verify_code = "000000"
    rpl_true = f'正在绑定第{bind_count + 1}个记录，请将 评论(个性签名) 或者 当前使用的 乐队编队名称改为\n{verify_code}\n稍等片刻等待同步后，发送\n验证 玩家ID 来完成本次身份验证\n例如：验证 10000xxxx 国服'
    # 存入verify_code
    cursor.execute("UPDATE users SET verify_code = ? WHERE user_id = ? AND platform = ?", (verify_code, user.user_id, platform))
    db_manager.conn.commit()
    return {'status': 'success', 'data': {'count': bind_count + 1, 'verifyCode': verify_code, 'response': rpl_true}}


def handler(user: UserLocal, res: MC, platform: str, channel_id: str):
    # 获取绑定请求
    r = bind_player_request(platform, user)
    if r.get('status') != 'success':
        return text_response(r.get('data'))
    return text_response(
        f'''正在绑定第{r.get('data').get('count')}个记录，请将 评论(个性签名) 或者 当前使用的 乐队编队名称改为\n{r.get('data')['verifyCode']}\n稍等片刻等待同步后，发送\n验证 你的玩家ID(数字) {i_2_n(user.server_mode)}\n''')

