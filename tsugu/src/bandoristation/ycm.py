from tsugu_api_core._typing import _Room

from ...utils import text_response, User, server_id_2_server_name, server_name_2_server_id
import tsugu_api
import tsugu_api_async
from arclet.alconna import Alconna, Option, Subcommand, Args, CommandMeta, Empty, Namespace, namespace, command_manager
from tsugu.utils import get_user, get_user_async
from typing import Optional

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

        user = get_user(user_id, platform)
        new_data_list = []

        for i in data:
            new_data_list.append({})

            # 检查是否有足够的玩家信息
            if len(user.user_player_list) > user.user_player_index:
                # 添加玩家信息
                new_data_list[-1].update({
                    'playerId': user.user_player_list[user.user_player_index]['playerId'],
                    'server': user.user_player_list[user.user_player_index]['server']
                })

            # 更新其他数据
            new_data_list[-1].update({'number': int(i['number'])})
            new_data_list[-1].update({'source': i['source_info']['name']})
            new_data_list[-1].update({'userId': i['user_info']['user_id']})
            new_data_list[-1].update({'time': i['time']})

            if i['user_info']['avatar']:
                new_data_list[-1].update({'avatarUrl': 'https://asset.bandoristation.com/images/user-avatar/' + i['user_info']['avatar']})
            elif i['user_info']['type'] == 'qq':
                new_data_list[-1].update({'avatarUrl': f'https://q2.qlogo.cn/headimg_dl?dst_uin={i["user_info"]["user_id"]}&spec=100'})
            new_data_list[-1].update({'userName': i['user_info']['username']})
            new_data_list[-1].update({'rawMessage': i['raw_message']})

        try:
            # 逆序
            new_data_list.reverse()
            # 过滤掉 new_data_list 中 number 相同的元素中较早的元素
            new_data_list_processed = []
            seen_numbers = set()

            for data in new_data_list:
                if data['number'] not in seen_numbers:
                    new_data_list_processed.append(data)
                    seen_numbers.add(data['number'])

            new_data_list = new_data_list_processed

            return tsugu_api.room_list(new_data_list)  # type: ignore
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

        user = await get_user_async(user_id, platform)
        new_data_list = []

        for i in data:
            new_data_list.append({})

            # 检查是否有足够的玩家信息
            if len(user.user_player_list) > user.user_player_index:
                # 添加玩家信息
                new_data_list[-1].update({
                    'playerId': user.user_player_list[user.user_player_index]['playerId'],
                    'server': user.user_player_list[user.user_player_index]['server']
                })

            # 更新其他数据
            new_data_list[-1].update({'number': int(i['number'])})
            new_data_list[-1].update({'source': i['source_info']['name']})
            new_data_list[-1].update({'userId': i['user_info']['user_id']})
            new_data_list[-1].update({'time': i['time']})

            if i['user_info']['avatar']:
                new_data_list[-1].update({'avatarUrl': 'https://asset.bandoristation.com/images/user-avatar/' + i['user_info']['avatar']})
            elif i['user_info']['type'] == 'qq':
                new_data_list[-1].update({'avatarUrl': f'https://q2.qlogo.cn/headimg_dl?dst_uin={i["user_info"]["user_id"]}&spec=100'})
            new_data_list[-1].update({'userName': i['user_info']['username']})
            new_data_list[-1].update({'rawMessage': i['raw_message']})

        try:
            # 逆序
            new_data_list.reverse()

            # 过滤掉 new_data_list 中 number 相同的元素中较早的元素
            new_data_list_processed = []
            seen_numbers = set()

            for data in new_data_list:
                if data['number'] not in seen_numbers:
                    new_data_list_processed.append(data)
                    seen_numbers.add(data['number'])

            new_data_list = new_data_list_processed

            return await tsugu_api_async.room_list(new_data_list)  # type: ignore
        except Exception as e:
            return text_response(e)

    return res


