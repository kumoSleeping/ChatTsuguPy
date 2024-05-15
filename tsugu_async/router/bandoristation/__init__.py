from . import rooms_forward
from . import ycm


async def api_handler(user, res, api, platform, channel_id):
    handler = getattr(globals()[api], 'handler')
    return await handler(user, res, platform, channel_id)

