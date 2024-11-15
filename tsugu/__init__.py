import re
from typing import Callable, List, Literal, TypeAlias, Union, Dict, Optional
import asyncio
from dataclasses import dataclass
import traceback

from loguru import logger

from arclet.alconna import (
    Alconna,
    Option,
    Subcommand,
    Args,
    CommandMeta,
    Empty,
    Namespace,
    namespace,
    command_manager,
    AllParam,
    MultiVar,
    Arparma,
    output_manager,
    command_manager,
)

import tsugu_api_async
from tsugu_api_core._typing import _ServerName, _ServerId, _UserPlayerInList
from tsugu_api_core import settings

from .alc_cmd import *
from .config import _s_i, _i_s, _difficulty_text_2_difficulty_id, _car_config
from typing import Callable, List, Literal, TypeAlias, Union, Dict, Optional


settings.timeout = int(os.getenv('TSUGU_TIMEOUT', '120'))
settings.proxy = os.getenv('TSUGU_PROXY', '')
settings.backend_url = os.getenv('TSUGU_BACKEND_URL', 'http://tsugubot.com:8080')
settings.backend_proxy = os.getenv('TSUGU_BACKEND_PROXY', 'true').lower() == 'true'
settings.userdata_backend_url = os.getenv('TSUGU_USERDATA_BACKEND_URL', 'http://tsugubot.com:8080')
settings.serdata_backend_proxy = os.getenv('TSUGU_USERDATA_BACKEND_PROXY', 'true').lower() == 'true'
settings.use_easy_bg = os.getenv('TSUGU_USE_EASY_BG', 'true').lower() == 'true'
settings.compress = os.getenv('TSUGU_COMPRESS', 'true').lower() == 'true'

if settings.backend_url != "http://tsugubot.com:8080":
    logger.info(f"Backend: {settings.backend_url}")
if settings.userdata_backend_url != "http://tsugubot.com:8080":
    logger.info(f"Userdata Backend: {settings.userdata_backend_url}")    
if settings.proxy != "":
    logger.warning(f"Proxy: {settings.backend_proxy}")

    
def text_response(string):
    return [{"type": "string", "string": str(string)}]


def server_names_2_server_ids(server_name: List[str]) -> List[_ServerId]:
    return [_s_i[code] for code in server_name]


def server_name_2_server_id(server_name: str) -> _ServerId:
    return _s_i[server_name] if server_name in _s_i else None


def server_ids_2_server_names(index: List[_ServerId]) -> List[str]:
    return [_i_s[code] for code in index]


def server_id_2_server_name(index: _ServerId) -> str:
    return _i_s[index] if index in _i_s else None


def server_exists(server):
    if server or server == 0:
        return True
    if not server:
        return False
    return False


@dataclass
class User:
    user_id: str
    platform: str
    main_server: _ServerId
    displayed_server_list: List[_ServerId]
    share_room_number: bool
    user_player_index: int
    user_player_list: List[_UserPlayerInList]


class ApiError(Exception):
    def __init__(self, message, status_code=None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code

    def __str__(self):
        if self.status_code:
            return f"[{self.status_code}] {self.message}"
        return self.message
    
def _get_user_account_list_msg(user) -> str:
    def mask_data(game_id: str):
        game_id = str(game_id)
        if len(game_id) < 6:
            return game_id[:3] + "*" * (len(game_id) - 3)
        elif len(game_id) < 3:
            return "*" * len(game_id)
        else:
            game_id = game_id[:3] + "*" * (len(game_id) - 6) + game_id[-3:]
        return game_id

    bind_record = "\n".join(
        [
            f'{i + 1}. {mask_data(str(x.get("playerId")))} {server_id_2_server_name(x.get("server"))}'
            for i, x in enumerate(user.user_player_list)
        ]
    )
    
    if bind_record.strip() == "":
        return "error: 暂无记录，请先绑定"

    return bind_record
    
async def _api_call(api_call, *args, **kwargs):
    try:
        return await api_call(*args, **kwargs)
    except Exception as e:
        # raise e
        logger.error(e)
        return text_response(f"API Error: {api_call.__name__}")
    
    
async def get_user(user_id: str, platform: str) -> User:
    """
    多次尝试获取用户数据

    :param user_id:
    :param platform:
    :return:
    """
    for i in range(3):
        try:
            user_data_res = await tsugu_api_async.get_user_data(platform, user_id)
            user_data = user_data_res.get("data")
            user = User(
                user_id=user_id,
                platform=platform,
                main_server=user_data.get("mainServer"),
                displayed_server_list=user_data.get("displayedServerList"),
                share_room_number=user_data.get("shareRoomNumber"),
                user_player_index=user_data.get("userPlayerIndex"),
                user_player_list=user_data.get("userPlayerList"),
            )
            return user
        except TimeoutError:
            await asyncio.sleep(0.2)
            continue
        except Exception as e:
            logger.error(f"Error: {e}")
            raise e
            # return '用户数据库连接失败，请联系管理员'


output_manager.set_action(lambda *_: None)


async def async_print(*args, **kwargs):
    print(*args, **kwargs)


async def cmd_generator(
    message: str,
    user_id: str,
    platform: str = "red",
    message_id: str = "",
    active_send_func: Optional[Callable] = async_print,
) -> Optional[List[Dict[str, str]]]:
    """## 命令生成器
    生成命令并返回结果
    _summary_

    Args:
        message (str): _description_ 用户信息
        user_id (str): _description_ 用户ID
        platform (str, optional): _description_. Defaults to "red". 平台，当用户ID为真实QQ号时，平台可以为red
        message_id (str, optional): _description_. Defaults to "". 消息ID，可用于主动消息的回复
        send_func (Optional[Callable], optional): _description_. Defaults to None. 主动发送消息的函数

    Returns:
        Optional[List[Dict[str, str]]]: _description_
    """

    result = await _handler(
        message=message,
        user_id=user_id,
        platform=platform,
        message_id=message_id,
        active_send_func=active_send_func,
    )

    # 未生成结果
    if isinstance(result, Arparma):
        # 匹配了命令头
        if result.head_matched:

            # 帮助信息
            if result.error_data == ["-h"]:
                return text_response(command_manager.command_help(result.source.name))
            # 错误信息
            else:
                return text_response(f'{str(result.error_info)}\n{command_manager.command_help(result.source.name)}')
                

    # 已生成结果
    if isinstance(result, list):
        return result
    
    # 字符串
    if isinstance(result, str):
        return text_response(result)
    
    if isinstance(result, ApiError):
        return text_response(f"API Error: {result}\nTraceback.")

    return None


async def _handler(
    message: str,
    user_id: str,
    platform: str,
    message_id: str,
    active_send_func: callable,
):
    
    async def _send(message: str):
        await active_send_func(
            {
                "user_id": user_id,
                "platform": platform,
                "message": message,
                "message_id": message_id,
            }
        )
        
    if (res := alc_help.parse(message)).head_matched:
        if res.matched:
            if not res.cmd:
                return command_manager.all_command_help()
            message = f"{res.cmd} -h"
        return res
    
    if (res := alc_event_stage.parse(message)).head_matched:
        if res.matched:
            user = await get_user(user_id, platform)
            meta = True if res.meta else False
            return await _api_call(tsugu_api_async.event_stage, user.main_server, res.eventId, meta)
        return res

    if (res := alc_gacha_simulate.parse(message)).head_matched:
        if res.matched:
            user = await get_user(user_id, platform)
            gacha_id = res.gacha_id if res.gacha_id else None
            return await _api_call(tsugu_api_async.gacha_simulate, user.main_server, res.times, gacha_id)
        return res

    if (res := alc_get_card_illustration.parse(message)).head_matched:
        if res.matched:
            return await _api_call(tsugu_api_async.get_card_illustration, res.cardId)
        return res

    if (res := alc_cutoff_list_of_recent_event.parse(message)).head_matched:
        if res.matched:
            user = await get_user(user_id, platform)
            server = server_name_2_server_id(res.serverName) if res.serverName else user.main_server
            return await _api_call(tsugu_api_async.cutoff_list_of_recent_event, main_server=server, tier=res.tier, event_id=res.eventId)
        return res

    if (res := alc_search_gacha.parse(message)).head_matched:
        if res.matched:
            user = await get_user(user_id, platform)
            return await _api_call(tsugu_api_async.search_gacha, displayed_server_list=user.displayed_server_list, gacha_id=res.gachaId)
        return res

    if (res := alc_search_character.parse(message)).head_matched:
        if res.matched:
            user = await get_user(user_id, platform)
            return await _api_call(tsugu_api_async.search_character, displayed_server_list=user.displayed_server_list, text=" ".join(res.word))
        return res

    if (res := alc_search_event.parse(message)).head_matched:
        if res.matched:
            user = await get_user(user_id, platform)
            return await _api_call(tsugu_api_async.search_event, displayed_server_list=user.displayed_server_list, text=" ".join(res.word))
        return res

    if (res := alc_search_card.parse(message)).head_matched:
        if res.matched:
            user = await get_user(user_id, platform)
            return await _api_call(tsugu_api_async.search_card, displayed_server_list=user.displayed_server_list, text=" ".join(res.word))
        return res
    
    if (res := alc_search_player.parse(message)).head_matched:
        if res.matched:
            user = await get_user(user_id, platform)
            server = server_name_2_server_id(res.serverName) if res.serverName else user.main_server
            if str(res.playerId).startswith("4") and server == 3:
                return "Bestdori 暂不支持渠道服相关功能"
            return await _api_call(tsugu_api_async.search_player, player_id=res.playerId, main_server=server)
        return res

    if (res := alc_song_random.parse(message)).head_matched:
        if res.matched:
            user = await get_user(user_id, platform)
            text = " ".join(res.word) if res.word else None
            return await _api_call(tsugu_api_async.song_random, main_server=user.main_server, text=text)
        return res

    if (res := alc_search_song.parse(message)).head_matched:
        if res.matched:
            user = await get_user(user_id, platform)
            return await _api_call(tsugu_api_async.search_song, displayed_server_list=user.displayed_server_list, text=" ".join(res.word))
        return res

    if (res := alc_song_chart.parse(message)).head_matched:
        if res.matched:
            user = await get_user(user_id, platform)
            return await _api_call(tsugu_api_async.song_chart, displayed_server_list=user.displayed_server_list, song_id=res.songId, difficulty_id=_difficulty_text_2_difficulty_id[res.difficultyText])
        return res

    if (res := alc_song_meta.parse(message)).head_matched:
        if res.matched:
            user = await get_user(user_id, platform)
            server = server_name_2_server_id(res.serverName) if res.serverName else user.main_server
            return await _api_call(tsugu_api_async.song_meta, displayed_server_list=user.displayed_server_list, main_server=server)
        return res

    if (res := alc_cutoff_all.parse(message)).head_matched:
        if res.matched:
            user = await get_user(user_id, platform)
            server = server_name_2_server_id(res.serverName) if res.serverName else user.main_server
            return await _api_call(tsugu_api_async.cutoff_all, main_server=server, event_id=res.eventId)
        return res

    if (res := alc_cutoff_detail.parse(message)).head_matched:
        if res.matched:
            user = await get_user(user_id, platform)
            server = server_name_2_server_id(res.serverName) if res.serverName else user.main_server
            return await _api_call(tsugu_api_async.cutoff_detail, main_server=server, tier=res.tier, event_id=res.eventId)
        return res

    if (res := alc_bind_player.parse(message)).head_matched:
        if res.playerId == 0:
            try:
                r = await tsugu_api_async.bind_player_request( user_id=user_id, platform=platform )
                return f"绑定玩家 0 用于刷新验证码\n刷新成功，验证码为 {r.get('data')['verifyCode']} "
            except Exception as e:
                return "请求失败，请稍后再试"
                

        user = await get_user(user_id, platform)
        server = (
            server_name_2_server_id(res.serverName)
            if res.serverName
            else user.main_server
        )

        if str(res.playerId).startswith("4") and server == 3:
            return text_response("Bestdori 暂不支持渠道服相关功能")

        if res.playerId in [player["playerId"] for player in user.user_player_list]:
            return text_response("你已经绑定过这个玩家了")
        try:
            r = await tsugu_api_async.bind_player_request(user_id=user_id, platform=platform)
        except Exception as e:
            return text_response(str(e) + "请求绑定失败，请稍后再试")

        await _send(f"""已进入绑定流程，请将在2min内将游戏账号的 评论(个性签名) 或者 当前使用的 乐队编队名称改为\n{r.get('data')['verifyCode']}\nbot将自动验证，绑定成功后会发送消息通知\n若验证码不可用，使用「绑定玩家 0」刷新验证码""")

        for i in range(7):
            await asyncio.sleep(20)
            try:
                await tsugu_api_async.bind_player_verification(  user_id=user_id, platform=platform, server=server, player_id=res.playerId, binding_action="bind", )
                return f"绑定成功，现在可以使用 玩家状态 命令查看绑定的玩家状态"
            except Exception as e:
                # 如果最后一次
                if i == 6 and "都与验证码不匹配" in str(e):
                    return f"解除绑定超时，{e}\n用户未及时修改游戏信息或Bestdori服务器暂时失效"
                if i == 6:
                    return f"解除绑定超时，{e}"
                if "都与验证码不匹配" in str(e):
                    continue
                # 其他错误
                return f"绑定失败，{e}"

        return res

    if (res := alc_change_displayed_server_list.parse(message)).head_matched:
        if res.matched:
            user = await get_user(user_id, platform)
            try:
                server_list = server_names_2_server_ids(res.serverList)
                update = {"displayedServerList": server_list}
                await tsugu_api_async.change_user_data(platform=platform, user_id=user.user_id, update=update)
                return f"默认服务器已设置为 {', '.join(res.serverList)}"
            except Exception as e:
                return ApiError
        return res

    if (res := alc_change_main_server.parse(message)).head_matched:
        if res.matched:
            user = await get_user(user_id, platform)
            server = server_name_2_server_id(res.serverName)
            try:
                r = await tsugu_api_async.change_user_data(platform=platform, user_id=user.user_id, update={"mainServer": server})
                return f"主服务器已设置为 {res.serverName}"
            except Exception as e:
                return ApiError
        return res

    if (res := alc_toggle_share_room_number_off.parse(message)).head_matched:
        if res.matched:
            user = await get_user(user_id, platform)
            update = {"shareRoomNumber": False}
            try:
                await tsugu_api_async.change_user_data(platform=platform, user_id=user.user_id, update=update)
                return "关闭车牌转发成功"
            except Exception as e:
                return ApiError
        return res

    if (res := alc_toggle_share_room_number_on.parse(message)).head_matched:
        if res.matched:
            user = await get_user(user_id, platform)
            update = {"shareRoomNumber": True}
            try:
                await tsugu_api_async.change_user_data(platform=platform, user_id=user.user_id, update=update)
                return "开启车牌转发成功"
            except Exception as e:
                return ApiError
        return res
    
    if (res := alc_player_status.parse(message)).head_matched:
        if res.matched:
            async def _player_status_case_default():
                user_player_index = user.user_player_index
                if len(user.user_player_list) == 0:
                    return "未找到记录，请先绑定"

                if user.user_player_index + 1 > len(user.user_player_list):
                    update = {"userPlayerIndex": 0}
                    try:
                        await tsugu_api_async.change_user_data(platform=platform, user_id=user.user_id, update=update)
                        await _send(f"""主账号异常，自动修正成功，将生成玩家状态（1）""")
                    except Exception as e:
                        return "主账号异常，自动修正失败，请手动发送“主账号 1”修正，或联系 bot 管理员"
                game_id_msg = user.user_player_list[user_player_index]
                return await _api_call(tsugu_api_async.search_player, player_id=int(game_id_msg.get("playerId")), main_server=game_id_msg.get("server"))

            async def _player_status_case_server():
                server_id = server_name_2_server_id(res.serverName)
                if not server_exists(server_id):
                    return "未找到服务器 " + res.serverName

                for i, x in enumerate(user.user_player_list):
                    if x.get("server") == server_id:
                        game_id_msg = user.user_player_list[i]
                        return await _api_call(tsugu_api_async.search_player, player_id=int(game_id_msg.get("playerId")), main_server=game_id_msg.get("server"))
                return f"未找到服务器 {res.serverName} 的记录"

            async def _player_status_case_index():
                if res.accountIndex > len(user.user_player_list) or res.accountIndex < 1:
                    return f"未找到记录 {res.accountIndex}，请先绑定"

                game_id_msg = user.user_player_list[res.accountIndex - 1]
                return await _api_call(tsugu_api_async.search_player, int(game_id_msg.get("playerId")), game_id_msg.get("server"))

            user = await get_user(user_id, platform)
            if res.accountIndex and not res.serverName:
                return await _player_status_case_index()
            elif res.serverName and not res.accountIndex:
                return await _player_status_case_server()
            elif res.serverName and res.accountIndex:
                return "只能同时指定一个账号或服务器"
            else:
                return await _player_status_case_default()
        return res

    if (res := alc_set_main_account.parse(message)).head_matched:
        if res.matched:
            user = await get_user(user_id, platform)
            if (
                not res.accountIndex
                or len(user.user_player_list) < res.accountIndex
                or res.accountIndex < 1
            ):
                bind_record = _get_user_account_list_msg(user=user)
                if bind_record == "":
                    return "未找到记录，请先绑定账号"
                return f'请选择你要设置为主账号的账号数字：\n{bind_record}\n例如：主账号 1'
            update = {"userPlayerIndex": res.accountIndex - 1}
            try:
                await tsugu_api_async.change_user_data(platform, user.user_id, update)
                return f"主账号已设置为账号 {res.accountIndex}"
            except Exception as e:
                return ApiError
        return res

    if (res := alc_unbind_player.parse(message)).head_matched:
        if res.matched:
            if res.index == 0:
                try:
                    r = await tsugu_api_async.bind_player_request(
                        user_id=user_id, platform=platform
                    )
                    return text_response(
                        f"""解除绑定 0 用于刷新验证码
    刷新成功，验证码为 {r.get('data')['verifyCode']} """
                    )
                except Exception as e:
                    return text_response(str(e) + "请求失败，请稍后再试")
            
            user = await get_user(user_id, platform)

            if (not res.index) or len(user.user_player_list) < res.index or res.index < 1:
                bind_record = _get_user_account_list_msg(user=user)
                if bind_record == "":
                    return "未找到记录，请先绑定账号"
                return f"选择你要解除的账号数字：\n{bind_record}\n例如：解除绑定 1"

            r = await _api_call(tsugu_api_async.bind_player_request, user_id=user_id, platform=platform)
            
            # 私有数据库API的解绑流程
            if r.get("extra") == "safe_mode":
                try:
                    await tsugu_api_async.bind_player_verification( user_id=user_id, platform=platform,
                                                                   server=user.user_player_list[res.index - 1].get("server"),
                                                                   player_id=user.user_player_list[res.index - 1].get("playerId"), binding_action="unbind")
                    return f"解除绑定成功"
                except Exception as e:
                    return f"解除绑定失败，请联系管理员"
            
            # 常规解绑流程
            await _send(f"""已进入解除绑定流程，请将在2min内将游戏账号的 评论(个性签名) 或者 当前使用的 乐队编队名称改为\n{r.get('data')['verifyCode']}\nbot将自动验证，解除成功后会发送消息通知\n若验证码不可用，使用「解除绑定 0」刷新验证码""")
            for i in range(7):
                await asyncio.sleep(20)
                try:
                    await tsugu_api_async.bind_player_verification(user_id=user_id, platform=platform,
                                                                   server=user.user_player_list[res.index - 1].get("server"),
                                                                   player_id=user.user_player_list[res.index - 1].get("playerId"),
                                                                   binding_action="unbind")
                    return f"解除绑定成功"
                except Exception as e:
                    if i == 6 and "都与验证码不匹配" in str(e):
                        return f"解除绑定超时，{e}\n用户未及时修改游戏信息或Bestdori服务器暂时失效"
                    if i == 6:
                        return f"解除绑定超时，{e}"
                    if "都与验证码不匹配" in str(e):
                        continue
                    return f"解除绑定失败，{e}"
        return res

    if (res := alc_query_room_number.parse(message)).head_matched:
        if res.matched:
            data = await _api_call(tsugu_api_async.query_room_number)
            if not data:
                return "myc"

            user = await get_user(user_id, platform)
            new_data_list = []
            seen_numbers = set()

            # 一开始就逆序 data 列表
            data.reverse()

            for i in data:
                number = int(i["number"])

                # 跳过已经处理过的 number
                if number in seen_numbers:
                    continue

                new_data = {}
                # 添加 number 到 seen_numbers，以便后续检查
                seen_numbers.add(number)

                # 检查是否有足够的玩家信息
                if len(user.user_player_list) > user.user_player_index:
                    # 添加玩家信息
                    new_data.update({ "playerId": user.user_player_list[user.user_player_index]["playerId"],  "server": user.user_player_list[user.user_player_index]["server"], })
                # 更新其他数据
                new_data.update({"number": number,"source": i["source_info"]["name"],"userId": i["user_info"]["user_id"],"time": i["time"],"userName": i["user_info"]["username"],"rawMessage": i["raw_message"], } )
                if i["user_info"]["avatar"]:
                    new_data.update({"avatarUrl": "https://asset.bandoristation.com/images/user-avatar/" + i["user_info"]["avatar"] })
                elif i["user_info"]["type"] == "qq":
                    new_data.update({"avatarUrl": f'https://q2.qlogo.cn/headimg_dl?dst_uin={i["user_info"]["user_id"]}&spec=100'})

                new_data_list.append(new_data)

            return await _api_call(tsugu_api_async.room_list, new_data_list)
        return res

    # 最后检查车牌
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

    user = await get_user(user_id, platform)

    # 获取用户数据
    try:
        if platform:
            if not user.share_room_number:
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
            car_user_id = "3889000770"
        await tsugu_api_async.submit_room_number(
            number=int(car_id),
            user_id=car_user_id,
            raw_message=message,
            source="Tsugu",
            token="ZtV4EX2K9Onb",
        )
        return None

    except Exception as e:
        return None
    
    
    # 未匹配到任何命令 结束 
