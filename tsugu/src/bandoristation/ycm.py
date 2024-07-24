from ...utils import text_response, User, server_id_2_server_name, server_name_2_server_id
import tsugu_api
import tsugu_api_async
from arclet.alconna import Alconna, Option, Subcommand, Args, CommandMeta, Empty, Namespace, namespace, command_manager
from tsugu.utils import get_user, get_user_async

alc = Alconna(
        ["ycm", "车来", "有车吗"],
        meta=CommandMeta(
            compact=True,
            description="获取车牌",
        )
    )


def handler(message: str, user_id: str, platform: str):
    res = alc.parse(message)

    if res.matched:
        try:
            data = tsugu_api.query_room_number()
        except Exception as e:
            return text_response('获取房间信息失败，请稍后再试')
        if not data:
            return text_response('myc')

        new_data = {}
        user = get_user(user_id, platform)
        for i in data:
            new_data.update({'player': {'playerId': user.user_player_list[user.user_player_index]['playerId'],
                              'server': user.user_player_list[user.user_player_index]['server']}})
            new_data.update({'number': int(i['number'])})
            new_data.update({'source': i['source_info']['name']})
            new_data.update({'userId': i['user_info']['user_id']})
            new_data.update({'time': i['time']})
            new_data.update({'avatarUrl': 'https://asset.bandoristation.com/images/user-avatar/' + i['user_info']['avatar']})
            new_data.update({'userName': i['user_info']['username']})
            new_data.update({'rawMessage': i['raw_message']})
        # 过滤掉 number 相同的
        try:
            return tsugu_api.room_list([new_data])
        except Exception as e:
            return text_response(e)

    return res


async def handler_async(message: str, user_id: str, platform: str):
    res = alc.parse(message)

    if res.matched:
        try:
            data = await tsugu_api_async.query_room_number()
        except Exception as e:
            return text_response('获取房间信息失败，请稍后再试')
        if not data:
            return text_response('myc')

        new_data = {}
        user = await get_user_async(user_id, platform)
        for i in data:
            new_data.update({'player': {'playerId': user.user_player_list[user.user_player_index]['playerId'],
                              'server': user.user_player_list[user.user_player_index]['server']}})
            new_data.update({'number': int(i['number'])})
            new_data.update({'source': i['source_info']['name']})
            new_data.update({'userId': i['user_info']['user_id']})
            new_data.update({'time': i['time']})
            new_data.update({'avatarUrl': 'https://asset.bandoristation.com/images/user-avatar/' + i['user_info']['avatar']})
            new_data.update({'userName': i['user_info']['username']})
            new_data.update({'rawMessage': i['raw_message']})
        # 过滤掉 number 相同的
        try:
            return await tsugu_api_async.room_list([new_data])
        except Exception as e:
            return text_response(e)

    return res