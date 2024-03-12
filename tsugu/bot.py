from .utils import *


def bot(message, user_id, platform, channel_id):
    message = message.strip()

    # 进行车牌匹配
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


def bot_extra_local_database(message, user_id, platform):
    if message.endswith('服玩家状态'):
        return player_status(user_id, platform, message[:-4]) if server_exists(r_ := query_server_info(message[:-4])) else text_response('服务器没找到喵') if len(message) <= 7 else None

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
            return text_response('没找到您要求的服务器或记录喵')


    if message.startswith('绑定玩家') and len(message.replace('绑定玩家', '').strip()) < 4:
        # 如果匹配 绑定玩家 则绑定默认服务器的玩家 如果用户输入了服务器名 则绑定对应服务器的玩家，如果服务器名无效则 赋值为 None
        return bind_player_request(platform, user_id)

    if message.startswith('验证'):
        arg_list = message.replace('验证', '').strip().split(' ')
        if len(arg_list) < 1:  # 如果长度小于2
            return text_response('请输入正确')
        if not arg_list[0].isdigit():  # 如果第一个不是数字
            return text_response('请确保您输入正确(例如: 验证 123456 cn)')
        server = query_server_info(arg_list[-1])
        player_id = arg_list[0]
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
            return text_response('为什么会有0啊（')
        return unbind_player_verification(platform, user_id, record)

    if message in ['开启车牌转发', '开启个人车牌转发']:
        return set_car_forward(platform, user_id, True)

    if message in ['关闭车牌转发', '关闭个人车牌转发']:
        return set_car_forward(platform, user_id, False)

    if message.endswith('服模式'):
        return set_server_mode(platform, user_id, message[:-2])

    if message.startswith('主服务器'):
        return set_server_mode(platform, user_id, message[4:].strip())

    if message.startswith('设置默认服务器'):
        return set_default_server(platform, user_id, message[6:].strip())


    return None


def bot_extra_remote_server(message, user_id, platform):
    if message.endswith('服玩家状态'):
        # 如果匹配 *服玩家状态 则查询对应服务器的玩家状态 前提是用户输入的 * 是一个有效的服务器名 否则返回None
        return Remote.player_status(user_id, platform, r_) if server_exists(r_ := query_server_info(message[:-4])) else text_response('服务器没找到喵') if len(message) <= 7 else None

    if message.startswith('玩家状态'):
        # 如果匹配 玩家状态 则查询默认服务器的玩家状态 如果用户输入了服务器名 则查询对应服务器的玩家状态，如果服务器名无效则返回None
        return Remote.player_status(user_id, platform) if (arg_ := message[4:].strip()) == '' else (Remote.player_status(user_id, platform, r_) if server_exists(r_ := query_server_info(arg_)) else None)

    if message.startswith('绑定玩家'):
        # 如果匹配 绑定玩家 则绑定默认服务器的玩家 如果用户输入了服务器名 则绑定对应服务器的玩家，如果服务器名无效则 赋值为 None
        server = Remote.get_user_data(platform, user_id)['data']['server_mode'] if message[4:].strip() == '' else (r_ if server_exists(r_ := query_server_info(message[4:])) else None)
        if not server:
            return text_response(f'未找到名为 {message[4:]} 的服务器信息，请确保您输入的是服务器名而不是玩家ID，通常情况您只需要发送"绑定玩家"或"绑定玩家 服务器"即可')

        res = Remote.bind_player_request(platform, user_id, server, True)
        if res.get('status') != 'success':
            print(res)
            # {'status': 'success', 'data': {'verifyCode': 12492}}
            return text_response(res.get('data') + ' 喵')
        # if not res.get('status') == 'failed':
        #     return text_response('未知错误喵')
        return text_response(f'''正在绑定账号，请将您的 评论(个性签名) 或者 当前使用的 乐队编队名称改为\n{res.get('data')['verifyCode']}\n稍等片刻等待同步后，发送\n验证 + 空格 + 您的玩家ID 来完成本次身份验证\n例如：验证 114514''')

    if message.startswith('解除绑定'):
        server = Remote.get_user_data(platform, user_id)['data']['server_mode'] if message[4:].strip() == '' else (r_ if (config.server_list(r_ := query_server_info(message[4:]))) else None)
        if not server:
            return text_response(f'未找到名为 {message[4:].strip()} 的服务器信息，请确保您输入的是服务器名而不是玩家ID，通常情况您只需要发送"解除绑定"即可')
        response = Remote.bind_player_request(platform, user_id, server, False)  # 获取响应
        if response.get('status') == 'failed':  # 检查状态
            return text_response(response.get('data') + ' 喵')
        # 如果是200
        return text_response(f'''正在解除，请将您的 评论(个性签名) 或者 当前使用的 乐队编队名称改为\n{response.get('data')['verifyCode']}\n稍等片刻等待同步后，发送\n验证解绑 {server}\n来完成本次身份验证(没错只需要加上 {server} 来确定您需要解绑的服务器)''')

    if message.startswith('验证解绑'):
        if not message[4:].strip().isdigit():
            return text_response('请输入解绑时提供的serverID(数字)')
        r = Remote.bind_player_verification(platform, user_id, int(message[4:].strip()), Remote.get_user_data(platform, user_id)['data']['server_list'][int(message[4:].strip())]['playerId'], False)
        if r.get('status') == 'failed':
            return text_response(r.get('data') + ' 喵')
        return text_response('解绑成功喵！')

    if message.startswith('验证'):
        if not message[2:].strip().isdigit():
            return text_response('请输入正确的玩家ID(数字)')
        if r := Remote.bind_player_verification(platform, user_id, Remote.get_user_data(platform, user_id)['data']['server_mode'], message[2:].strip(), True).get('status') == 'failed':
            return text_response(r.get('data') + ' 喵') if r.get('data') != '错误: 未请求绑定或解除绑定玩家' else None
        return text_response('绑定成功！现在可以使用"玩家状态"来查询玩家信息了～')

    if message in ['开启车牌转发', '开启个人车牌转发']:
        r = Remote.set_car_forward(platform, user_id, True)
        return text_response('已开启车牌转发') if r.get('status') == 'success' else None

    if message in ['关闭车牌转发', '关闭个人车牌转发']:
        r = Remote.set_car_forward(platform, user_id, False)
        return text_response('已关闭车牌转发') if r.get('status') == 'success' else None

    if message.endswith('服模式'):
        if r := Remote.set_server_mode(platform, user_id, message[:-2]).get('status') == 'success':
            return text_response('已切换为' + message[:-2] + '模式')
        return text_response(r.get('data')) if len(message) <= 5 else None

    if message.startswith('主服务器'):
        if r := Remote.set_server_mode(platform, user_id, message[4:].strip()).get('status') == 'success':
            return text_response('主服务器已切换为' + message[4:].strip())
        return text_response(r.get('data')) if ' ' in message else None

    if message.startswith('设置默认服务器'):
        if r := Remote.set_default_server(platform, user_id, message[6:].strip()).get('status') == 'success':
            return text_response('默认服务器已设置为' + message[6:].strip())
        return text_response(r.get('data')) if ' ' in message else None



