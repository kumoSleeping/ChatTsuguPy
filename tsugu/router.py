from .utils import *


def player_router(text, default_servers, server):
    return v2api_from_backend('player', text, default_servers, server)


def card_router(text, default_servers, server):
    return v2api_from_backend('card', text, default_servers, server)


def gacha_router(text, default_servers, server):
    return v2api_from_backend('gachaSimulate', text, default_servers, server)


def event_router(text, default_servers, server):
    return v2api_from_backend('event', text, default_servers, server)


def song_router(text, default_servers, server):
    return v2api_from_backend('song', text, default_servers, server)


def song_meta_router(text, default_servers, server):
    return v2api_from_backend('songMeta', text, default_servers, server)


def character_router(text, default_servers, server):
    return v2api_from_backend('character', text, default_servers, server)


def chart_router(text, default_servers, server):
    return v2api_from_backend('chart', text, default_servers, server)


def ycxall_router(text, default_servers, server):
    return v2api_from_backend('ycxAll', text, default_servers, server)


def ycx_router(text, default_servers, server):
    return v2api_from_backend('ycx', text, default_servers, server)


def lsycx_router(text, default_servers, server):
    return v2api_from_backend('lsycx', text, default_servers, server)


def ycm_router(text, default_servers, server):
    return v2api_from_backend('ycm', text, default_servers, server)


def card_illustration_router(text, default_servers, server):
    return v2api_from_backend('cardIllustration', text, default_servers, server)


def bind_player_request_router(platform, user_id, server, status):
    return bind_player_request(platform, user_id, server, status)


def bind_player_verification_router(platform, user_id, server, player_id, status):
    return bind_player_verification(platform, user_id, server, player_id, status)


def set_car_forward_router(platform, user_id, status):
    return set_car_forward(platform, user_id, status)


def set_default_server_router(platform, user_id, text):
    return set_default_server(platform, user_id, text)


def set_server_mode_router(platform, user_id, text):
    return set_server_mode(platform, user_id, text)

