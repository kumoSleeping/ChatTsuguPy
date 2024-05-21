from ...utils import text_response, User, server_id_2_server_name, server_name_2_server_id, server_exists, config
import tsugu_api
from arclet.alconna import Alconna, Option, Subcommand, Args, CommandMeta, Empty, Namespace, namespace, command_manager


def handler(message: str, user: User, platform: str, channel_id: str):
    res = Alconna(
        ["抽卡模拟", "卡池模拟"],
        Args["times", int, 10]['gacha_id;?#如果没有卡池ID的话，卡池为当前活动的卡池。', int],
        meta=CommandMeta(
            compact=config.compact, description="抽卡模拟",
            usage='根据卡片ID查询卡片插画',
            example='抽卡模拟 300 922 :模拟抽卡300次，卡池为922号卡池。'
        )
    ).parse(message)

    if res.matched:
        if channel_id in config.disable_gacha_simulate_group_ids:
            return None
        if res.gacha_id:
            gacha_id = res.gacha_id
        else:
            gacha_id = None
        return tsugu_api.gacha_simulate(user.server_mode, res.times, gacha_id)

    return res
