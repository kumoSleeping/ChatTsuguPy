import httpx

from ...config import config
from ...utils import text_response, UserLocal
from ...command_matcher import MC
# import tsugu_api
from ...utils import server_exists, server_name_2_server_id, server_id_2_server_name
import json
import urllib3
from ...storage.db import db_manager, get_user
from tsugu_api._typing import _ServerId


def get_bestdori_player(player_id: str, server: _ServerId):
    # 获取服务器名
    server_s_name = server_id_2_server_name(server)
    # 构建 URL
    url = f'https://bestdori.com/api/player/{server_s_name}/{player_id}?mode=2'
    if config.verify_player_bind_use_proxy:
        http = httpx.Client(proxies=config.proxy)
    else:
        http = httpx.Client()
    # 发送请求
    response = http.get(url)
    # 检查响应的状态码是否为 200
    if response.status_code == 200:
        # 解析 JSON 响应数据
        data = json.loads(response.text)
    else:
        return None
    return data


def bind_player_verification(platform: str, user: UserLocal, server: int | None, player_id: str, bind_type: bool):

    cursor = db_manager.conn.cursor()
    # 先检查verify_code是否正确
    # 使用 get
    verify_code = user.verify_code

    if server is None:
        server = user.server_mode
    if verify_code == "" or not verify_code:
        return {'status': 'error', 'data': '请先发送绑定请求'}
    # 检测重复性
    game_ids = user.game_ids
    for i in game_ids:
        if i.get("game_id") == player_id and i.get("server") == server:
            return {'status': 'error', 'data': '该记录已绑定'}

    # 获取玩家信息
    data = get_bestdori_player(player_id, server)

    if data.get("data").get("profile") is None or data.get("profile") == {}:
        return {'status': 'error', 'data': '未找到玩家，请检查玩家ID是否正确'}
    introduction = data.get("data", {}).get("profile", {}).get("introduction")
    deck_name = data.get("data", {}).get("profile", {}).get("mainUserDeck", {}).get("deckName")
    if verify_code != introduction and verify_code != deck_name:
        return {'status': 'error', 'data': '验证失败，请检查验证代码是否正确'}
    # 验证成功
    game_ids = user.game_ids
    game_ids.append({"game_id": player_id, "server": server})
    cursor.execute("UPDATE users SET game_ids = ? WHERE user_id = ? AND platform = ?",
                   (json.dumps(game_ids), user.user_id, platform))  # 存入game_ids
    cursor.execute("UPDATE users SET verify_code = ? WHERE user_id = ? AND platform = ?",
                   ("", user.user_id, platform))  # 清空verify_code
    db_manager.conn.commit()
    return {'status': 'success', 'data': '绑定成功! 现在可以使用"玩家状态"来查询玩家信息了'}


def handler(user: UserLocal, res: MC, platform: str, channel_id: str):
    if not res.args:
        return text_response('请输入正确的玩家ID和服务器名参数(可选)')
    if not res.args[0].isdigit():
        return text_response('请输入正确的玩家ID')
    player_id = int(res.args[0])
    if len(res.args) > 1:
        server_pre = server_name_2_server_id(res.args[1])
        if not server_exists(server_pre):
            return text_response('未找到服务器，请输入正确的服务器名')
        user.server_mode = server_pre

    r = bind_player_verification(platform, user, user.server_mode, player_id, True)
    if r.get('status') != 'success':
        return text_response(r.get('data'))
    return text_response('绑定成功')



