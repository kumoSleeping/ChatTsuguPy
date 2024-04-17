import base64
from typing import List, Union

from .utils import *


def bot(message, user_id, platform, channel_id):
    '''
    不再建议直接使用此函数，请使用 handler 函数
    :param message:
    :param user_id:
    :param platform:
    :param channel_id:
    :return:
    '''
    try:
        message = message.strip()

        # help
        if config.features.get('help', True):
            if message.startswith('帮助'):
                return help_command()
            if message.startswith('help'):
                arg_text = message[4:].strip()
                return help_command(arg_text)
            if message.endswith('-h'):
                arg_text = message[:-2].strip()
                return help_command(arg_text)

        # 进行车牌匹配
        if config.features.get('car_number_forwarding'):
            status = submit_car_number_msg(message, user_id, platform)
            if status:
                return None  # 已经匹配了车牌，就不需要再匹配其他指令了

        # 进行 v2 api 命令匹配
        command_matched, api = match_command(message, load_commands_from_config(config.commands))
        if command_matched:
            return v2_api_command(message, command_matched, api, platform, user_id, channel_id)
        if config.user_database_path:
            return bot_extra_local_database(message, user_id, platform)
        return bot_extra_remote_server(message, user_id, platform)
    except Exception as e:
        logger.error(f'Error: {e}')
        raise e


def handler(message: str, user_id: str, platform: str, channel_id: str) -> List[Union[bytes, str]]:
    '''
    :param message: 用户消息
    :param user_id: 用户ID
    :param platform: 平台名称 默认 red
    :param channel_id: 频道ID / 群号
    :return: List[Union[bytes, str]] bytes 为图片 str 为文字
    '''
    data = bot(message, user_id, platform, channel_id)
    response = []
    if not data:
        return response
    for item in data:
        if item['type'] == 'string':
            response.append(item['string'])
        elif item['type'] == 'base64':
            bytes_data = base64.b64decode(item['string'].encode('utf-8'))
            response.append(bytes_data)
    return response


def bot_extra_local_database(message, user_id, platform):
    # 玩家状态
    if config.features.get('player_status', True):
        if message.endswith('服玩家状态'):
            return player_status(user_id, platform, message[:-4]) if server_exists(r_ := query_server_info(message[:-4])) else text_response('未找到被指定的服务器') if len(message) <= 7 else None

        if message.startswith('玩家状态'):
            if (arg_ := message[4:].strip()) == '':
                return player_status(user_id, platform)
            # 如果用户输入了数字
            if arg_.isdigit():
                return player_status(user_id, platform, int(arg_))
            # 如果用户输入了服务器名
            if server_exists(r_ := query_server_info(arg_)):
                return player_status(user_id, platform, arg_)
            else:
                return text_response('未找到绑定记录')
    # 绑定玩家
    if config.features.get('bind_player', True):
        if message.startswith('绑定玩家'):
            if server_exists(query_server_info(message[4:].strip())) or message[4:].strip() == '':
                return bind_player_request(platform, user_id)
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
            return bind_player_verification(platform, user_id, server, player_id, True)

        if message.startswith('解除绑定'):
            if message[4:].strip() == '':
                return unbind_player_request(platform, user_id)
            msg_list = message.split(' ')
            if len(msg_list) < 2:
                return unbind_player_request(platform, user_id)
            if not msg_list[-1].isdigit():
                return unbind_player_request(platform, user_id)
            record = int(msg_list[-1])
            if record == 0:
                return text_response('为什么会有0啊，服了')
            return unbind_player_verification(platform, user_id, record)

    # 车牌转发控制
    if config.features.get('switch_car_forwarding', True):
        if message in ['开启车牌转发', '开启个人车牌转发']:
            return set_car_forward(platform, user_id, True)

        if message in ['关闭车牌转发', '关闭个人车牌转发']:
            return set_car_forward(platform, user_id, False)

    # 切换服务器模式
    if config.features.get('change_main_server', True):
        if message.endswith('服模式'):
            return set_server_mode(platform, user_id, message[:-2])

        if message.startswith('主服务器'):
            return set_server_mode(platform, user_id, message[4:].strip())

    # 设置默认服务器列表
    if config.features.get('change_server_list', True):
        if message.startswith('设置默认服务器'):
            return set_default_server(platform, user_id, message[7:].strip())

    return None


def bot_extra_remote_server(message, user_id, platform):
    # 玩家状态
    if config.features.get('player_status', True):
        if message.endswith('服玩家状态'):
            # 如果匹配 *服玩家状态 则查询对应服务器的玩家状态 前提是用户输入的 * 是一个有效的服务器名 否则返回None
            return Remote.player_status(user_id, platform, r_) if server_exists(r_ := query_server_info(message[:-4])) else text_response('未找到服务器') if len(message) <= 7 else None

        if message.startswith('玩家状态'):
            # 如果匹配 玩家状态 则查询默认服务器的玩家状态 如果用户输入了服务器名 则查询对应服务器的玩家状态，如果服务器名无效则返回None
            return Remote.player_status(user_id, platform) if (arg_ := message[4:].strip()) == '' else (Remote.player_status(user_id, platform, r_) if server_exists(r_ := query_server_info(arg_)) else None)

    # 绑定玩家
    if config.features.get('bind_player', True):
        if message.startswith('绑定玩家'):
            # 如果匹配 绑定玩家 则绑定默认服务器的玩家 如果用户输入了服务器名 则绑定对应服务器的玩家，如果服务器名无效则 赋值为 None
            server = Remote.get_user_data(platform, user_id)['data']['server_mode'] if message[4:].strip() == '' else (r_ if server_exists(r_ := query_server_info(message[4:])) else None)
            if not server_exists(server):
                return text_response(f'未找到名为 {(message[4:]).strip()} 的服务器信息，请确保输入的是服务器名而不是玩家ID，通常情况发送"绑定玩家"即可')

            res = Remote.bind_player_request(platform, user_id, server, True)

            if res.get('status') != 'success':
                # {'status': 'success', 'data': {'verifyCode': 12492}}
                return text_response(res.get('data'))
            # if not res.get('status') == 'failed':
            #     return text_response('未知错误喵')
            return text_response(f'''正在绑定账号，请将 评论(个性签名) 或者 当前使用的 乐队编队名称改为\n{res.get('data')['verifyCode']}\n稍等片刻等待同步后，发送\n验证 + 空格 + 玩家ID 来完成本次身份验证\n验证 10000xxxx 国服''')

        if message.startswith('解除绑定'):
            server = Remote.get_user_data(platform, user_id)['data']['server_mode'] if message[4:].strip() == '' else (r_ if (config.server_list(r_ := query_server_info(message[4:]))) else None)
            if server_exists(server) is False:
                return text_response(f'未找到名为 {(message[4:]).strip()} 的服务器信息，请确保输入的是服务器名而不是玩家ID，通常情况发送"绑定玩家"即可')
            response = Remote.bind_player_request(platform, user_id, server, False)  # 获取响应
            if response.get('status') == 'failed':  # 检查状态
                return text_response(response.get('data'))
            # 如果是200
            return text_response(f'''正在解除，请将 评论(个性签名) 或者 当前使用的 乐队编队名称改为\n{response.get('data')['verifyCode']}\n稍等片刻等待同步后，发送\n验证解绑 {server}\n来完成本次身份验证(没错只需要加上 {server} 来确定需要解绑的服务器)''')

        if message.startswith('验证解绑'):
            if not message[4:].strip().isdigit():
                return text_response('请输入解绑时提供的serverID(数字)')
            r = Remote.bind_player_verification(platform, user_id, int(message[4:].strip()), Remote.get_user_data(platform, user_id)['data']['server_list'][int(message[4:].strip())]['playerId'], False)
            if r.get('status') == 'failed':
                return text_response(r.get('data'))
            return text_response('解绑成功')

        if message.startswith('验证'):
            if not message[2:].strip().isdigit():
                return text_response('请输入正确的玩家ID(数字)')
            if r := Remote.bind_player_verification(platform, user_id, Remote.get_user_data(platform, user_id)['data']['server_mode'], message[2:].strip(), True).get('status') == 'failed':
                return text_response(r.get('data')) if r.get('data') != '错误: 未请求绑定或解除绑定玩家' else None
            return text_response('绑定成功！现在可以使用"玩家状态"来查询玩家信息')

    # 车牌转发控制
    if config.features.get('switch_car_forwarding', True):
        if message in ['开启车牌转发', '开启个人车牌转发']:
            r = Remote.set_car_forward(platform, user_id, True)
            return text_response('已开启车牌转发') if r.get('status') == 'success' else None

        if message in ['关闭车牌转发', '关闭个人车牌转发']:
            r = Remote.set_car_forward(platform, user_id, False)
            return text_response('已关闭车牌转发') if r.get('status') == 'success' else None

    # 切换服务器模式
    if config.features.get('change_main_server', True):
        if message.endswith('服模式'):
            if server_exists(r_ := query_server_info(message[:-2])) is False:
                return text_response('未找到服务器') if len(message) <= 5 else None
            if r := Remote.set_server_mode(platform, user_id, message[:-2]).get('status') == 'success':
                return text_response('已切换为' + message[:-2] + '模式')
            return text_response(r.get('data')) if len(message) <= 5 else None

        if message.startswith('主服务器'):
            if server_exists(r_ := query_server_info(message[4:].strip())) is False:
                return text_response('未找到服务器') if len(message) <= 7 else None
            if r := Remote.set_server_mode(platform, user_id, message[4:].strip()).get('status') == 'success':
                return text_response('主服务器已切换为' + message[4:].strip())
            return text_response(r.get('data')) if ' ' in message else None

    # 设置默认服务器列表
    if config.features.get('change_server_list', True):
        if message.startswith('设置默认服务器'):
            for i in message[7:].strip().split(' '):
                if server_exists(r_ := query_server_info(i)) is False:
                    return text_response(f'未找到服务器 {i}')
            if r := Remote.set_default_server(platform, user_id, message[6:].strip()).get('status') == 'success':
                return text_response('默认服务器已设置为' + message[6:].strip())
            return text_response(r.get('data')) if ' ' in message else None

    return None


