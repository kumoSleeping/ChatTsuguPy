from ...utils import text_response, User, server_id_2_server_name, server_name_2_server_id
import tsugu_api
import tsugu_api_async
from arclet.alconna import Alconna, Option, Subcommand, Args, CommandMeta, Empty, Namespace, namespace, command_manager


alc = Alconna(
        ["ycm", "车来", "有车吗"],
        meta=CommandMeta(
            compact=True,
            description="获取车牌",
        )
    )


def handler(message: str, user_id: str, platform: str, channel_id: str):
    res = alc.parse(message)

    if res.matched:
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

    return res


async def handler_async(message: str, user_id: str, platform: str, channel_id: str):
    res = alc.parse(message)

    if res.matched:
        try:
            data = await tsugu_api_async.query_room_number()
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

        return await tsugu_api_async.room_list(new_data)

    return res


