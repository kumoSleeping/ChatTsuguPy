from ..command_matcher import MC
from ..config import config
from ..utils import text_response


async def help_command(res: MC):
    if not res.args:
        # 读取 config.help_doc_dict 中的所有键
        command_list = list(config._help_doc_dict.keys())
        command_list.sort()
        return text_response(f'当前支持的命令有：\n{" ".join(command_list)}\n请使用"help 命令名"来查看命令的详细帮助')
    else:
        help_text = config.help_doc_dict.get(res.args[0], None)
        if help_text:
            return text_response(help_text)
        return None

