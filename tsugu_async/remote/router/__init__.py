from . import bind_player
from . import unbind_player
from . import player_status
from . import bind_player_verification_off
from . import bind_player_verification_on
from . import switch_car_forwarding_off
from . import switch_car_forwarding_on
from . import change_server_mode
from . import change_default_server


async def api_handler(user, res, api, platform, channel_id):
    handler = getattr(globals()[api], 'handler')
    return await handler(user, res, platform, channel_id)


