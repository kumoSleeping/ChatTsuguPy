from . import db
from . import remote_db


def _get_user(user_id: str, platform: str, local=False):
    if local:
        user = db.get_user(user_id, platform)
    else:
        user = remote_db.get_user(user_id, platform)
    return user