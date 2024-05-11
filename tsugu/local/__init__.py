from ..universal_utils import server_exists, query_server_info, load_commands_from_config, match_command, text_response, config

from . import utils
import re


def handler(message, user_id, platform, channel_id):
    if config.features.get('car_number_forwarding'):
        status = utils.submit_car_number_msg(message, user_id, platform)
        if status:
            return None  # 已经匹配了车牌，就不需要再匹配其他指令了
    # 进行 v2 api 命令匹配
    command_matched, api = match_command(message, load_commands_from_config(config.commands))
    if command_matched:
        return utils.v2_api_command(message, command_matched, api, platform, user_id, channel_id)

    # 玩家状态
    if config.features.get('player_status', True):
        if message.endswith('服玩家状态'):
            return utils.player_status(user_id, platform, message[:-4]) if server_exists(r_ := query_server_info(message[:-4])) else text_response('未找到被指定的服务器') if len(message) <= 7 else None

        if message.startswith('玩家状态'):
            if (arg_ := message[4:].strip()) == '':
                return utils.player_status(user_id, platform)
            # 如果用户输入了数字
            if arg_.isdigit():
                return utils.player_status(user_id, platform, int(arg_))
            # 如果用户输入了服务器名
            if server_exists(r_ := query_server_info(arg_)):
                return utils.player_status(user_id, platform, arg_)
            else:
                return text_response('未找到绑定记录')
    # 绑定玩家
    if config.features.get('bind_player', True):
        if message.startswith('绑定玩家'):
            if server_exists(query_server_info(message[4:].strip())) or message[4:].strip() == '':
                return utils.bind_player_request(platform, user_id)
            else:
                return text_response(f'未找到名为 {(message[4:]).strip()} 的服务器信息，请确保输入的是服务器名而不是玩家ID，通常情况发送"绑定玩家"即可')

        if message.startswith('验证'):
            arg = message.replace('验证', '').strip()
            # 正则出数字
            player_ids = re.findall(r'\d+', arg)
            if not player_ids or len(player_ids) > 1:
                return text_response('请确保输入正确(例如: 验证 10000xxxxx cn)')
            player_id = player_ids[0]
            server = query_server_info(arg.replace(player_id, ''))  # 后续自动处理 None
            return utils.bind_player_verification(platform, user_id, server, player_id, True)

        if message.startswith('解除绑定'):
            if message[4:].strip() == '':
                return utils.unbind_player_request(platform, user_id)
            msg_list = message.split(' ')
            if len(msg_list) < 2:
                return utils.unbind_player_request(platform, user_id)
            if not msg_list[-1].isdigit():
                return utils.unbind_player_request(platform, user_id)
            record = int(msg_list[-1])
            if record == 0:
                return text_response('为什么会有0啊，服了')
            return utils.unbind_player_verification(platform, user_id, record)

    # 车牌转发控制
    if config.features.get('switch_car_forwarding', True):
        if message in ['开启车牌转发', '开启个人车牌转发']:
            return utils.set_car_forward(platform, user_id, True)

        if message in ['关闭车牌转发', '关闭个人车牌转发']:
            return utils.set_car_forward(platform, user_id, False)

    # 切换服务器模式
    if config.features.get('change_main_server', True):
        if message.endswith('服模式'):
            return utils.set_server_mode(platform, user_id, message[:-2])

        if message.startswith('主服务器'):
            return utils.set_server_mode(platform, user_id, message[4:].strip())

    # 设置默认服务器列表
    if config.features.get('change_server_list', True):
        if message.startswith('设置默认服务器'):
            return utils.set_default_server(platform, user_id, message[7:].strip())

    return None