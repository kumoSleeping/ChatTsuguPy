import importlib
from arclet.alconna import Alconna, Option, Subcommand, Args, CommandMeta, Empty, Namespace, namespace, output_manager, command_manager
from ..utils import text_response, get_user
import threading


def require(module_path, cmd):
    globals()[cmd] = importlib.import_module(module_path.format(cmd=cmd), __package__)


universal_list = [
    "get_card_illustration",
    "search_player",
    "gacha_simulate",
    "search_gacha",
    "search_event",
    "search_song",
    "song_meta",
    "search_character",
    "song_chart",
    "ycx_all",
    "ycx",
    "lsycx",
    "search_card",
    "event_stage",
]

remote_commands = [
    "player_status",
    "switch_car_forwarding_off",
    "switch_car_forwarding_on",
    "bind_player",
    "unbind_player",
    "change_server_mode",
    "change_default_server",
    "bind_player_verification_off",
    "bind_player_verification_on",
]


bandoristation_commands = [
    "ycm",
    "rooms_forward",
]

# 导入模块
[require(f'.universal.{cmd}', cmd) for cmd in universal_list]
[require(f'.remote.{cmd}', cmd) for cmd in remote_commands]
[require(f'.bandoristation.{cmd}', cmd) for cmd in bandoristation_commands]


class ThisValue:
    def __init__(self):
        self.local_data = threading.local()

    def set_h(self, value):
        self.local_data.h = value

    def get_h(self):
        return getattr(self.local_data, 'h', None)


this_value = ThisValue()


def handler(message, user_id, platform, channel_id):
    user = get_user(user_id, platform)

    def set_output_str(arg):
        # 为每个线程设置独立的 h 值
        this_value.set_h(arg)

    output_manager.set_action(set_output_str)

    def handler_feats(cmd_list):
        for i in cmd_list:
            result = getattr(globals()[i], 'handler')(message, user, platform, channel_id)
            if not result:
                continue
            if result[0].get('type') == 'string' and result[0].get('string') == 'help':
                return text_response(this_value.get_h())
            return result
        return None

    res = handler_feats(universal_list)
    if res:
        return res

    res = handler_feats(remote_commands)
    if res:
        return res

    res = handler_feats(bandoristation_commands)
    if res:
        return res

    if message in ["help", "帮助"]:
        return text_response(command_manager.all_command_help(show_index=True))

    return None

