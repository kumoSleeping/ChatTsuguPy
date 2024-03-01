from typing import List
from .utils import *


class Router:
    def __init__(self):
        pass

    @staticmethod
    def player(text: str, default_servers: List[int], server: int):
        return v2api_from_backend('player', text, default_servers, server)

    @staticmethod
    def card(text: str, default_servers: List[int], server: int):
        return v2api_from_backend('card', text, default_servers, server)

    @staticmethod
    def gacha(text: str, default_servers: List[int], server: int):
        return v2api_from_backend('gachaSimulate', text, default_servers, server)

    @staticmethod
    def event(text: str, default_servers: List[int], server: int):
        return v2api_from_backend('event', text, default_servers, server)

    @staticmethod
    def song(text: str, default_servers: List[int], server: int):
        return v2api_from_backend('song', text, default_servers, server)

    @staticmethod
    def song_meta(text: str, default_servers: List[int], server: int):
        return v2api_from_backend('songMeta', text, default_servers, server)

    @staticmethod
    def character(text: str, default_servers: List[int], server: int):
        return v2api_from_backend('character', text, default_servers, server)

    @staticmethod
    def chart(text: str, default_servers: List[int], server: int):
        return v2api_from_backend('chart', text, default_servers, server)

    @staticmethod
    def ycxall(text: str, default_servers: List[int], server: int):
        return v2api_from_backend('ycxAll', text, default_servers, server)

    @staticmethod
    def ycx(text: str, default_servers: List[int], server: int):
        return v2api_from_backend('ycx', text, default_servers, server)

    @staticmethod
    def lsycx(text: str, default_servers: List[int], server: int):
        return v2api_from_backend('lsycx', text, default_servers, server)

    @staticmethod
    def ycm(text: str, default_servers: List[int], server: int):
        return v2api_from_backend('ycm', text, default_servers, server)

    @staticmethod
    def card_illustration(text: str, default_servers: List[int], server: int):
        return v2api_from_backend('cardIllustration', text, default_servers, server)

    @staticmethod
    def bind_player_request(platform: str, user_id: str, server: int, status: bool):
        return bind_player_request(platform, user_id, server, status)

    @staticmethod
    def bind_player_verification(platform: str, user_id: str, server: int, player_id: str, status: bool):
        return bind_player_verification(platform, user_id, server, player_id, status)

    @staticmethod
    def set_car_forward(platform: str, user_id: str, status: str):
        return set_car_forward(platform, user_id, status)

    @staticmethod
    def set_default_server(platform: str, user_id: str, text: str):
        return set_default_server(platform, user_id, text)

    @staticmethod
    def set_server_mode(platform: str, user_id: str, text: str):
        return set_server_mode(platform, user_id, text)

    @staticmethod
    def get_user_data(platform: str, user_id: str):
        return get_user_data(platform, user_id)


router = Router()

