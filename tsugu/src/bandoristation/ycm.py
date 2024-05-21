from ...utils import text_response, User, config
import tsugu_api
from arclet.alconna import Alconna, Option, Subcommand, Args, CommandMeta, Empty, Namespace, namespace, command_manager


def handler(message: str, user: User, platform: str, channel_id: str):
    res = Alconna(
        ["ycm", "车来", "有车吗"],
        meta=CommandMeta(
            compact=config.compact, description="获取车牌",
        )
    ).parse(message)

    if res.matched:
        return car_search()
    return res


def car_search():
    try:
        data = tsugu_api.query_room_number()
    except Exception as e:
        return text_response('获取房间信息失败，请稍后再试')
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

    return tsugu_api.room_list(new_data)

