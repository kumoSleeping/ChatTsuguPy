from ...utils import text_response, User, get_user, get_user_async
from arclet.alconna import Alconna, Option, Subcommand, Args, CommandMeta, Empty, Namespace, namespace, command_manager
import re
import tsugu_api
import tsugu_api_async


# 虚空注册
alc = Alconna(
    ["上传车牌"],
    meta=CommandMeta(
        description="上传车牌",
       ),
    )


def handler(message: str, user_id: str, platform: str, channel_id: str):
    if message.startswith("上传车牌"):
        message = message[4:].strip()

    # 检查car_config['car']中的关键字
    for keyword in _car_config["car"]:
        if str(keyword) in message:
            break
    else:
        return None

    # 检查car_config['fake']中的关键字
    for keyword in _car_config["fake"]:
        if str(keyword) in message:
            return None

    pattern = r"^\d{5}(\D|$)|^\d{6}(\D|$)"
    if not re.match(pattern, message):
        return None

    user = get_user(user_id, platform)

    # 获取用户数据
    try:
        if platform:
            if not user.car:
                return None
    except Exception as e:
        # 默认不开启关闭车牌，继续提交
        pass

    try:
        car_id = message[:6]
        if not car_id.isdigit() and car_id[:5].isdigit():
            car_id = car_id[:5]
        if user.user_id.isdigit():
            car_user_id = user.user_id
        else:
            car_user_id = '3889000770'
        tsugu_api.submit_room_number(number=int(car_id), user_id=car_user_id, raw_message=message, source="Tsugu", token="ZtV4EX2K9Onb")
        return None

    except Exception as e:
        return None


async def handler_async(message: str, user_id: str, platform: str, channel_id: str):
    if message.startswith("上传车牌"):
        message = message[4:].strip()

    # 检查car_config['car']中的关键字
    for keyword in _car_config["car"]:
        if str(keyword) in message:
            break
    else:
        return None

    # 检查car_config['fake']中的关键字
    for keyword in _car_config["fake"]:
        if str(keyword) in message:
            return None

    pattern = r"^\d{5}(\D|$)|^\d{6}(\D|$)"
    if not re.match(pattern, message):
        return None

    user = await get_user_async(user_id, platform)

    # 获取用户数据
    try:
        if platform:
            if not user.car:
                return None
    except Exception as e:
        # 默认不开启关闭车牌，继续提交
        pass

    try:
        car_id = message[:6]
        if not car_id.isdigit() and car_id[:5].isdigit():
            car_id = car_id[:5]
        if user.user_id.isdigit():
            car_user_id = user.user_id
        else:
            car_user_id = '3889000770'
        await tsugu_api_async.submit_room_number(number=int(car_id), user_id=car_user_id, raw_message=message, source="Tsugu", token="ZtV4EX2K9Onb")
        return None

    except Exception as e:
        return None


_car_config = {
    "car": [
        "q1",
        "q2",
        "q3",
        "q4",
        "Q1",
        "Q2",
        "Q3",
        "Q4",
        "缺1",
        "缺2",
        "缺3",
        "缺4",
        "差1",
        "差2",
        "差3",
        "差4",
        "3火",
        "三火",
        "3把",
        "三把",
        "打满",
        "清火",
        "奇迹",
        "中途",
        "大e",
        "大分e",
        "exi",
        "大分跳",
        "大跳",
        "大a",
        "大s",
        "大分a",
        "大分s",
        "长途",
        "生日车",
        "军训",
        "禁fc",
    ],
    "fake": [
        "114514",
        "野兽",
        "恶臭",
        "1919",
        "下北泽",
        "粪",
        "糞",
        "臭",
        "11451",
        "xiabeize",
        "雀魂",
        "麻将",
        "打牌",
        "maj",
        "麻",
        "[",
        "]",
        "断幺",
        "qq.com",
        "腾讯会议",
        "master",
        "疯狂星期四",
        "离开了我们",
        "日元",
        "av",
        "bv",
    ],
}


