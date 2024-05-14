from ...config import config
from ...utils import text_response, User
from ...command_matcher import MC
import tsugu_api_async
from ...utils import server_exists, server_names_2_server_ids
from tsugu_api._typing import _Update


async def handler(user: User, res: MC, platform: str, channel_id: str):
    default_server = server_names_2_server_ids(res.args)
    if not default_server:
        return text_response('未找到服务器，请输入正确的服务器名')
    change_data: _Update = {'default_server': default_server}
    r = await tsugu_api_async.change_user_data(platform, user.user_id, change_data)
    if r.get('status') == 'success':
        return text_response(f'默认服务器已设置为 {", ".join(res.args)}')
    return text_response(r.get('data'))
