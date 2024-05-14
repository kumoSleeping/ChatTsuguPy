from ...utils import text_response, User
from ...command_matcher import MC
import tsugu_api
from ...utils import server_exists, server_name_2_server_id, server_id_2_server_name
from tsugu_api._typing import _ServerId, _Update


def handler(user: User, res: MC, platform: str, channel_id: str):
    if res.args:
        server_mode = server_name_2_server_id(res.args[0])
        if not server_exists(server_mode):
            return text_response('未找到服务器，请输入正确的服务器名')
        update: _Update = {'server_mode': server_mode, }
        if r := tsugu_api.change_user_data(platform, user.user_id, update):
            if r.get('status') == 'success':
                return text_response('主服务器已设置为 ' + server_id_2_server_name(server_mode))
            return text_response(r.get('data'))

