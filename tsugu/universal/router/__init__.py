from . import get_card_illustration
from . import search_player
from . import gacha_simulate
from . import search_gacha
from . import search_event
from . import search_song
from . import song_meta
from . import search_character
from . import song_chart
from . import ycx_all
from . import ycx
from . import lsycx
from . import room_list
from . import search_card
from . import event_stage


def api_handler(user, res, api, platform, channel_id):
    return getattr(globals()[api], 'handler')(user, res, platform, channel_id)



