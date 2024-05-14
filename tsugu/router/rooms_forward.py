import tsugu_api

from ..utils import config, get_user
from loguru import logger
import httpx
import re

from ..utils import User, text_response
from ..command_matcher import MC


def submit_rooms(res: MC, user_id, platform=None):
    message = res.text
    # 检查car_config['car']中的关键字
    for keyword in config._car_config["car"]:
        if str(keyword) in message:
            break
    else:
        return []

    # 检查car_config['fake']中的关键字
    for keyword in config._car_config["fake"]:
        if str(keyword) in message:
            return []

    pattern = r"^\d{5}(\D|$)|^\d{6}(\D|$)"
    if not re.match(pattern, message):
        return []

    user = get_user(user_id, platform)

    # 获取用户数据
    try:
        if platform:
            if not user.car:
                return []
    except Exception as e:
        # 默认不开启关闭车牌，继续提交
        pass

    try:
        car_id = message[:6]
        if not car_id.isdigit() and car_id[:5].isdigit():
            car_id = car_id[:5]

        tsugu_api.submit_room_number(int(car_id), user.user_id, message, config.token_name, config.bandori_station_token)
        return []
    except Exception as e:
        logger.error(f"[Tsugu] 发生异常: {e}")
        return []  # 虽然提交失败，但是确定了是车牌消息



