from . import rooms_forward
from . import ycm


def api_handler(user, res, api, platform, channel_id):
    return getattr(globals()[api], 'handler')(user, res, platform, channel_id)

