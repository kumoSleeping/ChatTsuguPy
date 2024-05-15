from ...config import config
from ...utils import text_response, User
from ...command_matcher import MC
import tsugu_api_async


async def handler(user: User, res: MC, platform: str, channel_id: str):
    data = await tsugu_api_async.query_room_number()
    if not data:
        return text_response('myc')
    new_data = []
    for i in data:
        if isinstance(i['number'], str):
            i['number'] = int(i['number'])
        i['source'] = i['source_info']['name']
        i['userId'] = i['user_info']['user_id']
        i['time'] = i['time']
        i['avanter'] = i['user_info']['avatar']
        i['userName'] = i['user_info']['username']
        i['rawMessage'] = i['raw_message']
        new_data.append(i)
    # 过滤掉 number 相同的
    new_data = list({v['number']: v for v in new_data}.values())
    return await tsugu_api_async.room_list(new_data)

