from ...config import config
from ...utils import text_response, User
from ...command_matcher import MC
import tsugu_api_async


async def handler(user: User, res: MC, platform: str, channel_id: str):
    data = await tsugu_api_async.station_query_all_room()
    if not data.get('status'):
        return text_response('获取房间列表失败')
    return await tsugu_api_async.room_list(data.get('data'))

