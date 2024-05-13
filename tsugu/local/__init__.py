from ..utils import server_exists, load_commands_from_config, text_response, config, UserLocal

from . import utils as local_utils
from ..universal import universal_api_handler
from ..utils import text_response, server_exists, ns_2_is, n_2_i, i_2_n, is_2_ns
from ..command_matcher import match_command
from . import router
from tsugu_api._typing import _ServerId
import json


def local_api_handler(user: UserLocal, message: str,  platform: str, channel_id: str):
    for i in config.user_commands:
        if res := match_command(message, commands=i['command_name']):
            api = i['api']
            return router.api_handler(user, res, api, platform, channel_id)

    return None


def handler(message, user_id, platform, channel_id):
    print('local handler')
    if config.features.get('car_number_forwarding'):
        # status = utils.submit_car_number_msg(message, user_id, platform)
        # if status:
        #     return None
        pass

    user_data_res = local_utils.get_user_data(platform, user_id)
    # 获取用户数据失败
    if user_data_res.get('status') == 'failed':
        return text_response(user_data_res.get('data'))
    # 构建用户对象
    user_data = user_data_res.get('data')
    game_ids = json.loads(user_data['game_ids'])
    user = UserLocal(user_id, platform, user_data['server_mode'], user_data['default_server'], user_data['car'], [], game_ids, user_data['verify_code'])

    # 进行 api 命令匹配

    # 进行 api 命令匹配
    result = universal_api_handler(user, message, platform, channel_id)
    if result:
        return result

    # 远程命令
    result = local_api_handler(user, message, platform, channel_id)
    if result:
        return result

    return None


    # # 玩家状态
    # if res := match_command(message, ['玩家状态']):
    #     # 获取用户数据
    #     if not res.args:
    #         # 查询默认服务器的玩家状态
    #         return tsugu_api.search_player(server=user.server_mode, player_id=user.server_list[user.server_mode]['playerId'])
    #     else:
    #         # 查询指定服务器的玩家状态
    #         server: _ServerId = n_2_i(res.args[0])
    #         # 服务器不存在
    #         if not server_exists(server):
    #             return text_response('未找到服务器，请输入正确的服务器名')
    #         player_id = user.server_list[server]['playerId']
    #         # 未绑定玩家
    #         if not player_id:
    #             return text_response('未绑定玩家，请先绑定玩家')
    #         # 查询玩家状态
    #         return tsugu_api.search_player(server=server, player_id=user.server_list[server]['playerId'])
    #
    #     if res := match_command(message, ['玩家状态']):
    #         if res.args is not None:
    #             return local_utils.player_status(user_id, platform)
    #         # 如果用户输入了数字
    #         if res.args[0].isdigit():
    #             return local_utils.player_status(user_id, platform, int(arg_))
    #         # 如果用户输入了服务器名
    #         if server_exists(r_ := n_2_i(arg_)):
    #             return local_utils.player_status(user_id, platform, arg_)
    #         else:
    #             return text_response('未找到绑定记录')
    # # 绑定玩家
    # if config.features.get('bind_player', True):
    #     if message.startswith('绑定玩家'):
    #         if server_exists(n_2_i(message[4:].strip())) or message[4:].strip() == '':
    #             return local_utils.bind_player_request(platform, user_id)
    #         else:
    #             return text_response(f'未找到名为 {(message[4:]).strip()} 的服务器信息，请确保输入的是服务器名而不是玩家ID，通常情况发送"绑定玩家"即可')
    #
    #     if message.startswith('验证'):
    #         arg = message.replace('验证', '').strip()
    #         # 正则出数字
    #         player_ids = re.findall(r'\d+', arg)
    #         if not player_ids or len(player_ids) > 1:
    #             return text_response('请确保输入正确(例如: 验证 10000xxxxx cn)')
    #         player_id = player_ids[0]
    #         server = n_2_i(arg.replace(player_id, ''))  # 后续自动处理 None
    #         return local_utils.bind_player_verification(platform, user_id, server, player_id, True)
    #
    #     # if message.startswith('解除绑定'):
    #     #     if message[4:].strip() == '':
    #     #         return local_utils.unbind_player_request(platform, user_id)
    #     #     msg_list = message.split(' ')
    #     #     if len(msg_list) < 2:
    #     #         return local_utils.unbind_player_request(platform, user_id)
    #     #     if not msg_list[-1].isdigit():
    #     #         return local_utils.unbind_player_request(platform, user_id)
    #     #     record = int(msg_list[-1])
    #     #     if record == 0:
    #     #         return text_response('为什么会有0啊，服了')
    #     #     return local_utils.unbind_player_verification(platform, user_id, record)
    #
    # # 车牌转发控制
    # if config.features.get('switch_car_forwarding', True):
    #     if message in ['开启车牌转发', '开启个人车牌转发']:
    #         return local_utils.set_car_forward(platform, user_id, True)
    #
    #     if message in ['关闭车牌转发', '关闭个人车牌转发']:
    #         return local_utils.set_car_forward(platform, user_id, False)
    #
    # # 切换服务器模式
    # if config.features.get('change_main_server', True):
    #     if message.endswith('服模式'):
    #         return local_utils.set_server_mode(platform, user_id, message[:-2])
    #
    #     if message.startswith('主服务器'):
    #         return local_utils.set_server_mode(platform, user_id, message[4:].strip())
    #
    # # 设置默认服务器列表
    # if config.features.get('change_server_list', True):
    #     if message.startswith('设置默认服务器'):
    #         return local_utils.set_default_server(platform, user_id, message[7:].strip())
    #
    # return None