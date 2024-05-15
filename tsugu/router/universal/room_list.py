from ...config import config
from ...utils import text_response, User
from ...command_matcher import MC
import tsugu_api

import httpx


def handler(user: User, res: MC, platform: str, channel_id: str):
    data = tsugu_api.station_query_all_room()
    if not data.get('status'):
        return text_response('获取房间列表失败')
    print(data.get('data'))
    return tsugu_api.room_list(data.get('data'))

