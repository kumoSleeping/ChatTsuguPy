import re
from typing import Callable, List, Literal, TypeAlias, Union, Dict, Optional
import asyncio
from dataclasses import dataclass

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

settings.timeout = 30

_i_s = {0: "jp", 1: "en", 2: "tw", 3: "cn", 4: "kr"}
_s_i = {
    "jp": 0,
    "en": 1,
    "tw": 2,
    "cn": 3,
    "kr": 4,
    "日服": 0,
    "国际服": 1,
    "台服": 2,
    "国服": 3,
    "韩服": 4,
}
_ServerNameFull: TypeAlias = Literal[
    "jp", "en", "tw", "cn", "kr", "日服", "国际服", "台服", "国服", "韩服"
]


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
                return text_response(
                    (
                        str(result.error_info)
                        + "\n"
                        + command_manager.command_help(result.source.name)
                    )
                )

    # 已生成结果
    if isinstance(result, list):
        return result

    return None


alc_0 = Alconna(
    ["help"],
    Args["cmd;?", str],
    meta=CommandMeta(
        compact=True,
        description="",
    ),
)


alc_1 = Alconna(
    ["查试炼", "查stage", "查舞台", "查festival", "查5v5"],
    Args["eventId;?", [int]]["meta;?", ["-m"]],
    meta=CommandMeta(
        compact=True,
        description="查询活动的试炼信息",
        example="""查试炼 157 -m :返回157号活动的试炼信息，包含歌曲meta
查试炼 -m :返回当前活动的试炼信息，包含歌曲meta
查试炼 :返回当前活动的试炼信息""",
    ),
)


alc_2 = Alconna(
    ["抽卡模拟", "卡池模拟"],
    Args["times", int, 10]["gacha_id;?", int],
    meta=CommandMeta(
        compact=True,
        description="就像真的抽卡一样",
        example="抽卡模拟 300 922 :模拟抽卡300次，卡池为922号卡池",
    ),
)

alc_3 = Alconna(
    ["查卡面", "查插画"],
    Args["cardId", int],
    meta=CommandMeta(
        compact=True,
        description="根据卡面ID查询卡面插画",
        example="查卡面 1399 :返回1399号卡牌的插画",
    ),
)

alc_4 = Alconna(
    ["lsycx", "历史预测线"],
    Args["tier", int]["eventId;?", int][
        "serverName;?",
        _ServerNameFull,
    ],
    meta=CommandMeta(
        compact=True,
        description="查询指定档位的预测线与最近的4期活动类型相同的活动的档线数据",
        example="lsycx 1000\nlsycx 1000 177 jp",
    ),
)

alc_5 = Alconna(
    ["查卡池"],
    Args["gachaId", str],
    meta=CommandMeta(
        compact=True,
        description="根据卡池ID查询卡池信息",
        example="查卡池 947 :返回947号卡池的信息",
    ),
)

alc_6 = Alconna(
    ["查角色"],
    Args["word", AllParam],
    meta=CommandMeta(
        compact=True,
        description="根据角色名、乐队、昵称等查询角色信息",
        example="查角色 10 :返回10号角色的信息\n查角色 吉他 :返回所有角色模糊搜索标签中包含吉他的角色列表",
    ),
)

alc_7 = Alconna(
    ["查活动"],
    Args["word", AllParam],
    meta=CommandMeta(
        compact=True,
        description="根据活动名、乐队、活动ID等查询活动信息",
        example="查活动 绿 tsugu :返回所有属性加成为pure，且活动加成角色中包括羽泽鸫的活动列表\n查活动 177 :返回177号活动的信息",
    ),
)

alc_8 = Alconna(
    ["查卡"],
    Args["word", AllParam],
    meta=CommandMeta(
        compact=True,
        description="根据卡面ID、角色名、乐队、昵称等查询卡面信息",
        example="查卡 1399 :返回1399号卡牌的信息\n查卡 红 ars 5x :返回角色 ars 的 5x 卡片的信息",
    ),
)

alc_9 = Alconna(
    ["查玩家", "查询玩家"],
    Args["playerId", int][
        "serverName;?",
        _ServerNameFull,
    ],
    meta=CommandMeta(
        compact=True,
        description="根据玩家ID、服务器查询玩家信息",
        example="""查玩家 1003282233 : 查询默认服务器中玩家ID为1003282233的玩家信息
查玩家 40474621 jp : 查询日服玩家ID为40474621的玩家信息
""",
    ),
)

alc_10 = Alconna(
    ["随机曲"],
    Args["word;?", AllParam],
    meta=CommandMeta(
        compact=True,
        description="根据关键词或曲目ID随机曲目信息",
        example="""随机曲 lv27 :在所有包含27等级难度的曲中, 随机返回其中一个
随机曲 ag :返回随机的 Afterglow 曲目""",
    ),
)

alc_11 = Alconna(
    ["查曲"],
    Args["word", AllParam],
    meta=CommandMeta(
        compact=True,
        description="根据关键词或曲目ID查询曲目信息",
        example="""查曲 1 :返回1号曲的信息
查曲 ag lv27 :返回所有难度为27的ag曲列表""",
    ),
)

alc_12 = Alconna(
    ["查谱面", "查铺面"],
    Args["songId", int][
        "difficultyText",
        ("easy", "ez", "normal", "nm", "hard", "hd", "expert", "ex", "special", "sp"),
        "ex",
    ],
    meta=CommandMeta(
        compact=True,
        description="根据曲目ID与难度查询铺面信息",
        example="查谱面 1 :返回1号曲的ex难度谱面\n查谱面 128 special :返回128号曲的special难度谱面",
    ),
)

alc_13 = Alconna(
    ["查询分数表", "查分数表", "查询分数榜", "查分数榜"],
    Args["serverName;?", _ServerNameFull],
    meta=CommandMeta(
        compact=True,
        description="",
        example="查询分数表 cn :返回国服的歌曲分数表",
    ),
)

alc_14 = Alconna(
    ["ycxall", "ycx all"],
    Args["eventId;?", int]["serverName;?", _ServerNameFull],
    meta=CommandMeta(
        compact=True,
        description="输出全部档位的预测线",
        example="ycx 1000\nycx 1000 177 jp",
    ),
)

alc_15 = Alconna(
    ["ycx", "预测线"],
    Args["tier", int]["eventId;?", int]["serverName;?", _ServerNameFull],
    meta=CommandMeta(
        compact=True,
        description="指定档位的预测线",
        example="""ycx 1000
ycx 1000 177 jp""",
    ),
)

alc_16 = Alconna(
    ["绑定玩家"],
    Args["playerId", int]["serverName;?", _ServerNameFull],
    meta=CommandMeta(
        compact=True,
        description="绑定游戏账号",
        example="""绑定玩家 114514 : 绑定默认服务器中玩家ID为114514的玩家
绑定玩家 1919810 jp : 绑定日服玩家ID为1919810的玩家
绑定玩家 0 : 刷新你的验证码""",
    ),
)


alc_18 = Alconna(
    ["设置默认服务器", "默认服务器"],
    Args["serverList", MultiVar(_ServerNameFull)],
    meta=CommandMeta(
        compact=True,
        description="设定信息显示中的默认服务器排序",
        example="""设置默认服务器 cn jp : 将国服设置为第一服务器，日服设置为第二服务器""",
    ),
)

alc_19 = Alconna(
    ["主服务器", "设置主服务器"],
    Args["serverName", _ServerNameFull],
    meta=CommandMeta(
        compact=True,
        description="将指定的服务器设置为你的主服务器",
        example="""主服务器 cn : 将国服设置为主服务器""",
    ),
)

alc_20 = Alconna(
    ["关闭车牌转发", "关闭个人车牌转发"],
    meta=CommandMeta(
        compact=True,
        description="",
    ),
)

alc_21 = Alconna(
    ["开启车牌转发", "开启个人车牌转发"],
    meta=CommandMeta(
        compact=True,
        description="",
    ),
)

alc_22 = Alconna(
    ["玩家状态"],
    Args["accountIndex;?", int],
    meta=CommandMeta(
        compact=True,
        description="查询自己的玩家状态",
        example="""
玩家状态 :返回指定默认账号的玩家状态
玩家状态 1 :返回账号1的玩家状态
主账号 :返回默认查询账号
主账号 2 :设置账号2为默认查询账号
玩家状态 2 :返回账号2的玩家状态
""",
    ),
)

alc_23 = Alconna(
    ["主账号"],
    Args["accountIndex", int],
    meta=CommandMeta(
        compact=True,
        description="设定默认玩家状态、车牌展示中的主账号使用第几个账号",
        example="""主账号 : 返回所有账号列表
主账号 2 : 将第二个账号设置为主账号""",
    ),
)

alc_24 = Alconna(
    ["解除绑定"],
    Args["index;?", int],
    meta=CommandMeta(
        compact=True,
        description="解除绑定游戏账号",
        example="解除绑定 1 : 解绑第一个记录",
    ),
)

alc_25 = Alconna(
    ["ycm", "车来", "有车吗"],
    meta=CommandMeta(
        compact=True,
        description="获取车站信息",
    ),
)

alc_26 = Alconna(
    ["上传车牌"],
    Args["roomNumber", str],
    meta=CommandMeta(
        description="自动检测车牌并上传",
    ),
)


async def _handler(
    message: str,
    user_id: str,
    platform: str,
    message_id: str,
    active_send_func: callable,
):
    if (res := alc_0.parse(message)).matched:
        if not res.cmd:
            return text_response(command_manager.all_command_help())

        message = f"{res.cmd} -h"

    elif res.head_matched:
        return res

    if (res := alc_1.parse(message)).matched:
        user = await get_user(user_id, platform)
        if res.meta:
            meta = True
        else:
            meta = False
        try:
            return await tsugu_api_async.event_stage(
                user.main_server, res.eventId, meta
            )
        except Exception as e:
            return text_response("API Error: /event_stage" + str(e))
    elif res.head_matched:
        return res

    if (res := alc_2.parse(message)).matched:
        user = await get_user(user_id, platform)
        if res.gacha_id:
            gacha_id = res.gacha_id
        else:
            gacha_id = None
        try:
            return await tsugu_api_async.gacha_simulate(
                user.main_server, res.times, gacha_id
            )
        except Exception as e:
            return text_response("API Error: /gacha_simulate" + str(e))

    elif res.head_matched:
        return res

    if (res := alc_3.parse(message)).matched:
        try:
            return await tsugu_api_async.get_card_illustration(res.cardId)
        except Exception as e:
            return text_response("API Error: /get_card_illustration" + str(e))

    elif res.head_matched:
        return res

    if (res := alc_4.parse(message)).matched:
        user = await get_user(user_id, platform)
        server = (
            server_name_2_server_id(res.serverName)
            if res.serverName
            else user.main_server
        )
        try:
            return await tsugu_api_async.cutoff_list_of_recent_event(
                server, res.tier, res.eventId
            )
        except Exception as e:
            return text_response("API Error: /cutoff_list_of_recent_event" + str(e))

    elif res.head_matched:
        return res

    if (res := alc_5.parse(message)).matched:
        user = await get_user(user_id, platform)
        try:
            return await tsugu_api_async.search_gacha(
                user.displayed_server_list, res.gachaId
            )
        except Exception as e:
            return text_response("API Error: /search_gacha" + str(e))

    elif res.head_matched:
        return res

    if (res := alc_6.parse(message)).matched:
        user = await get_user(user_id, platform)
        try:
            return await tsugu_api_async.search_character(
                user.displayed_server_list, text=" ".join(res.word)
            )
        except Exception as e:
            return text_response("API Error: /search_character" + str(e))

    elif res.head_matched:
        return res

    if (res := alc_7.parse(message)).matched:
        user = await get_user(user_id, platform)
        try:
            return await tsugu_api_async.search_event(
                user.displayed_server_list, text=" ".join(res.word)
            )
        except Exception as e:
            return text_response("API Error: /search_event" + str(e))

    elif res.head_matched:
        return res

    if (res := alc_8.parse(message)).matched:
        user = await get_user(user_id, platform)
        try:
            return await tsugu_api_async.search_card(
                user.displayed_server_list, " ".join(res.word)
            )
        except Exception as e:
            return text_response("API Error: /search_card" + str(e))

    elif res.head_matched:
        return res

    if (res := alc_9.parse(message)).matched:
        user = await get_user(user_id, platform)
        if res.serverName:
            server = server_name_2_server_id(res.serverName)
        else:
            server = user.main_server
        if str(res.playerId).startswith("4") and server == 3:
            return text_response("Bestdori 暂不支持渠道服相关功能")
        try:
            return await tsugu_api_async.search_player(res.playerId, server)
        except Exception as e:
            return text_response("API Error: /search_player" + str(e))

    elif res.head_matched:
        return res

    if (res := alc_10.parse(message)).matched:
        user = await get_user(user_id, platform)
        try:
            text = " ".join(res.word) if res.word else None
            return await tsugu_api_async.song_random(user.main_server, text=text)
        except Exception as e:
            return text_response("API Error: /song_random" + str(e))

    elif res.head_matched:
        return res
    if (res := alc_11.parse(message)).matched:
        user = await get_user(user_id, platform)
        try:
            return await tsugu_api_async.search_song(
                user.displayed_server_list, text=" ".join(res.word)
            )
        except Exception as e:
            return text_response("API Error: /search_song" + str(e))

    elif res.head_matched:
        return res

    difficulty_text_tuple = (
        "easy",
        "ez",
        "normal",
        "nm",
        "hard",
        "hd",
        "expert",
        "ex",
        "special",
        "sp",
    )
    difficulty_text_2_difficulty_id = {
        "easy": 0,
        "ez": 0,
        "normal": 1,
        "nm": 1,
        "hard": 2,
        "hd": 2,
        "expert": 3,
        "ex": 3,
        "special": 4,
        "sp": 4,
    }

    if (res := alc_12.parse(message)).matched:
        user = await get_user(user_id, platform)
        try:
            return await tsugu_api_async.song_chart(
                user.displayed_server_list,
                res.songId,
                difficulty_text_2_difficulty_id[res.difficultyText],
            )
        except Exception as e:
            return text_response("API Error: /song_chart" + str(e))

    elif res.head_matched:
        return res

    if (res := alc_13.parse(message)).matched:
        user = await get_user(user_id, platform)
        if res.serverName:
            server = server_name_2_server_id(res.serverName)
        else:
            server = user.main_server
        try:
            return await tsugu_api_async.song_meta(user.displayed_server_list, server)
        except Exception as e:
            return text_response("API Error: /song_meta" + str(e))

    elif res.head_matched:
        return res

    if (res := alc_14.parse(message)).matched:
        user = await get_user(user_id, platform)
        server = (
            server_name_2_server_id(res.serverName)
            if res.serverName
            else user.main_server
        )
        try:
            return await tsugu_api_async.cutoff_all(server, res.eventId)
        except Exception as e:
            return text_response("API Error: /cutoff_all" + str(e))

    elif res.head_matched:
        return res

    if (res := alc_15.parse(message)).matched:
        user = await get_user(user_id, platform)
        server = (
            server_name_2_server_id(res.serverName)
            if res.serverName
            else user.main_server
        )
        try:
            return await tsugu_api_async.cutoff_detail(server, res.tier, res.eventId)
        except Exception as e:
            return text_response("API Error: /cutoff_detail" + str(e))

    elif res.head_matched:
        return res

    if (res := alc_16.parse(message)).matched:

        if res.playerId == 0:
            try:
                r = await tsugu_api_async.bind_player_request(
                    user_id=user_id, platform=platform
                )
                return text_response(
                    f"""绑定玩家 0 用于刷新验证码
刷新成功，验证码为 {r.get('data')['verifyCode']} """
                )
            except Exception as e:
                return text_response(str(e) + "请求失败，请稍后再试")

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
            r = await tsugu_api_async.bind_player_request(
                user_id=user_id, platform=platform
            )
        except Exception as e:
            return text_response(str(e) + "请求绑定失败，请稍后再试")

        await active_send_func(
            {
                "user_id": user_id,
                "platform": platform,
                "message": f"""已进入绑定流程，请将在2min内将游戏账号的 评论(个性签名) 或者 当前使用的 乐队编队名称改为\n{r.get('data')['verifyCode']}\nbot将自动验证，绑定成功后会发送消息通知\n若验证码不可用，使用「绑定玩家 0」刷新验证码""",
                "message_id": message_id,
            }
        )

        for i in range(7):
            await asyncio.sleep(20)
            try:
                await tsugu_api_async.bind_player_verification(
                    user_id=user_id,
                    platform=platform,
                    server=server,
                    player_id=res.playerId,
                    binding_action="bind",
                )
                return text_response(
                    f"绑定成功，现在可以使用 玩家状态 命令查看绑定的玩家状态"
                )
            except Exception as e:
                # 如果最后一次
                if i == 6:
                    return text_response(f"绑定超时，请重试")

                if "都与验证码不匹配" in str(e):
                    continue
                # 其他错误
                return text_response(f"绑定失败，请稍后再试")

    elif res.head_matched:
        return res

    if (res := alc_18.parse(message)).matched:
        user = await get_user(user_id, platform)
        try:
            await tsugu_api_async.change_user_data(
                platform,
                user.user_id,
                {"displayedServerList": server_names_2_server_ids(res.serverList)},
            )
        except Exception as e:
            return text_response(str(e))

        return text_response("默认服务器已设置为 " + " ".join(res.serverList))

    elif res.head_matched:
        return res

    if (res := alc_19.parse(message)).matched:
        user = await get_user(user_id, platform)
        try:
            r = await tsugu_api_async.change_user_data(
                platform,
                user.user_id,
                {"mainServer": server_name_2_server_id(res.serverName)},
            )
        except Exception as e:
            return text_response("API Error: /change_user_data" + str(e))
        return text_response("主服务器已设置为 " + res.serverName)

    elif res.head_matched:
        return res

    elif res.head_matched:
        return res
    if (res := alc_20.parse(message)).matched:
        user = await get_user(user_id, platform)
        update = {
            "shareRoomNumber": False,
        }
        try:
            r = await tsugu_api_async.change_user_data(platform, user.user_id, update)
            return text_response("关闭车牌转发成功")
        except Exception as e:
            return text_response("API Error: /change_user_data" + str(e))

    elif res.head_matched:
        return res

    if (res := alc_21.parse(message)).matched:
        user = await get_user(user_id, platform)
        update = {
            "shareRoomNumber": True,
        }
        try:
            r = await tsugu_api_async.change_user_data(platform, user.user_id, update)
            return text_response("开启车牌转发成功")
        except Exception as e:
            return text_response("API Error: /change_user_data" + str(e))

    elif res.head_matched:
        return res

    if (res := alc_22.parse(message)).matched:

        async def _player_status_case_default():
            user_player_index = user.user_player_index
            try:
                if len(user.user_player_list) == 0:
                    return text_response(f"未找到记录，请先绑定")

                if user.user_player_index + 1 > len(user.user_player_list):
                    update = {"userPlayerIndex": 0}
                    try:
                        await tsugu_api_async.change_user_data(
                            platform, user.user_id, update
                        )
                        await active_send_func(
                            {
                                "user_id": user_id,
                                "platform": platform,
                                "message": f"""主账号异常，自动修正成功，将生成玩家状态（1）""",
                                "message_id": message_id,
                            }
                        )
                    except Exception as e:
                        return text_response(
                            "主账号异常，自动修正失败，请手动发送“主账号 1”修正，或联系 bot 管理员"
                        )
                game_id_msg = user.user_player_list[user_player_index]
                return await tsugu_api_async.search_player(
                    int(game_id_msg.get("playerId")), game_id_msg.get("server")
                ) + text_response(
                    f"\n已查找默认玩家状态（{user_player_index + 1}），“help 玩家状态” 了解更多"
                )
            except Exception as e:
                return text_response("API Error: /search_player" + str(e))

        async def _player_status_case_index():
            if res.accountIndex > len(user.user_player_list) or res.accountIndex < 1:
                return text_response(f"未找到记录 {res.accountIndex}，请先绑定")
            try:
                game_id_msg = user.user_player_list[res.accountIndex - 1]
                return await tsugu_api_async.search_player(
                    int(game_id_msg.get("playerId")), game_id_msg.get("server")
                ) + text_response(f"\n已查找账号 {res.accountIndex} 玩家状态，“help 玩家状态” 了解更多")
            except Exception as e:
                return text_response("API Error: /search_player" + str(e))

        user = await get_user(user_id, platform)
        if res.accountIndex:
            return await _player_status_case_index()
        else:
            return await _player_status_case_default()

    elif res.head_matched:
        return res

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
        return bind_record

    if (res := alc_23.parse(message)).matched:
        user = await get_user(user_id, platform)
        if (
            not res.accountIndex
            or len(user.user_player_list) < res.accountIndex
            or res.accountIndex < 1
        ):
            bind_record = _get_user_account_list_msg(user=user)
            if bind_record == "":
                return text_response("未找到记录，请先绑定账号")
            return text_response(
                "请选择你要设置为主账号的账号数字：\n"
                + bind_record
                + "\n例如：主账号 1"
            )

        update = {"userPlayerIndex": res.accountIndex - 1}
        try:
            await tsugu_api_async.change_user_data(platform, user.user_id, update)
            return text_response("主账号已设置为账号 " + str(res.accountIndex))
        except Exception as e:
            return text_response("API Error: /change_user_data" + str(e))

    elif res.head_matched:
        return res
    
    
    if (res := alc_24.parse(message)).matched:
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
        server = (
            server_name_2_server_id(res.serverName)
            if res.serverName
            else user.main_server
        )

        if (not res.index) or len(user.user_player_list) < res.index or res.index < 1:

            try:
                bind_record = _get_user_account_list_msg(user=user)
                if bind_record == "":
                    return text_response("未找到记录，请先绑定账号")
                return text_response(
                    f"""选择你要解除的账号数字：\n{bind_record}\n例如：解除绑定 1"""
                )
            except Exception as e:
                return text_response(str(e) + "请求绑定失败，请稍后再试")

        try:
            r = await tsugu_api_async.bind_player_request(
                user_id=user_id, platform=platform
            )
        except Exception as e:
            return text_response(str(e) + "请求绑定失败，请稍后再试")
        await active_send_func(
            {
                "user_id": user_id,
                "platform": platform,
                "message": f"""已进入解除绑定流程，请将在2min内将游戏账号的 评论(个性签名) 或者 当前使用的 乐队编队名称改为\n{r.get('data')['verifyCode']}\nbot将自动验证，解除成功后会发送消息通知\n若验证码不可用，使用「解除绑定 0」刷新验证码""",
                "message_id": message_id,
            }
        )
        player_id = user.user_player_list[res.index - 1].get("playerId")
        for i in range(7):
            await asyncio.sleep(20)
            try:
                # logger.debug(
                #     f"解除绑定：{user_id} {platform} {server} {player_id}，第{i + 1}次尝试"
                # )
                await tsugu_api_async.bind_player_verification(
                    user_id=user_id,
                    platform=platform,
                    server=server,
                    player_id=player_id,
                    binding_action="unbind",
                )
                return text_response(f"解除绑定成功")
            except Exception as e:
                # 如果最后一次
                if i == 6:
                    return text_response(f"解除绑定超时，请重试")

                if "都与验证码不匹配" in str(e):
                    # print(f'验证码错误，{i + 1}次尝试')
                    # 进入下一次循环
                    continue
                # 其他错误
                return text_response(f"解除绑定失败，请稍后再试")

    elif res.head_matched:
        return res

    if (res := alc_25.parse(message)).matched:
        try:
            data = await tsugu_api_async.query_room_number()
        except Exception as e:
            return text_response("获取房间信息失败，请稍后再试")

        if not data:
            return text_response("myc")

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
                new_data.update(
                    {
                        "playerId": user.user_player_list[user.user_player_index][
                            "playerId"
                        ],
                        "server": user.user_player_list[user.user_player_index][
                            "server"
                        ],
                    }
                )

            # 更新其他数据
            new_data.update(
                {
                    "number": number,
                    "source": i["source_info"]["name"],
                    "userId": i["user_info"]["user_id"],
                    "time": i["time"],
                    "userName": i["user_info"]["username"],
                    "rawMessage": i["raw_message"],
                }
            )

            if i["user_info"]["avatar"]:
                new_data.update(
                    {
                        "avatarUrl": "https://asset.bandoristation.com/images/user-avatar/"
                        + i["user_info"]["avatar"]
                    }
                )
            elif i["user_info"]["type"] == "qq":
                new_data.update(
                    {
                        "avatarUrl": f'https://q2.qlogo.cn/headimg_dl?dst_uin={i["user_info"]["user_id"]}&spec=100'
                    }
                )

            new_data_list.append(new_data)

        try:
            return await tsugu_api_async.room_list(new_data_list)
        except Exception as e:
            return text_response("获取房间信息失败，请稍后再试")

    elif res.head_matched:
        return res

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
            "11451",
            "1919",
            "810",
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
        ],
    }

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
