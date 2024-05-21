from ...utils import get_user, text_response, User, server_id_2_server_name, server_name_2_server_id
from arclet.alconna import Alconna, Option, Subcommand, Args, CommandMeta, Empty, Namespace, namespace, command_manager, MultiVar, AllParam


alc = Alconna(
        ["help"],
        Args["cmd;?#命令", str],
        meta=CommandMeta(
            compact=True,
            description="Chat Tsugu Py 帮助",)
    )


def handler(message: str, user_id: str, platform: str, channel_id: str):
    res = alc.parse(message)

    if res.matched:
        if not res.cmd:
            return text_response(command_manager.all_command_help())

        try:
            cmd = command_manager.command_help(res.cmd)
            return text_response(cmd)

        except KeyError:
            # return text_response('未找到该命令')
            return None

        except Exception as e:
            # return text_response('未知错误')
            return None

    return None


async def handler_async(message: str, user_id: str, platform: str, channel_id: str):
    res = alc.parse(message)

    if res.matched:
        if not res.cmd:
            return text_response(command_manager.all_command_help())

        try:
            cmd = command_manager.command_help(res.cmd)
            return text_response(cmd)

        except KeyError:
            # return text_response('未找到该命令')
            return None

        except Exception as e:
            # return text_response('未知错误')
            return None

    return None
