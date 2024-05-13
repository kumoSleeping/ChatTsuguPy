from typing import Optional, Union, List
from ..utils import config


def remove_first_prefix(text):
    '''
    移除第一个前缀 (前缀在配置文件规定)


    Remove the first prefix (the prefix is specified in the configuration file)
    '''
    for prefix in config.prefix:
        if text.startswith(prefix):
            text = text.replace(prefix, '', 1)
            break
    return text.strip()


def plaintext_if_prefix(text):
    '''
    如果有前缀，移除第一个前缀 (前缀在配置文件规定)，如果没有前缀，返回空字符串


    If there is a prefix, remove the first prefix (the prefix is specified in the configuration file), if there is no prefix, return an empty string
    '''
    for prefix in config.prefix:
        if text.startswith(prefix):
            text = text.replace(prefix, '', 1)
            return text.strip()
    else:
        text = ''
        return text


class MC:
    def __init__(self, args: list, text: str):
        '''
        匹配命令的对象
        entity of matching command

        :param args: list 参数列表
        :param text: str 文本
        '''
        self.args: Optional[list[str]] = args
        self.text: str = text


def match_command(text: str,
                  commands: Optional[Union[List[str], str]] = '',
                  limit_arg_less: bool = False,
                  ) -> Optional[MC]:
    '''
    必须参数:
    commandss  指令头。

    可选参数:
    limit_arg_less  限制指令头后面不能有参数。
    allow_gap_less  容许指令头后不加空格。

    返回:
    Optional[MC] / None  如果匹配到了，返回一个"MC 对象"，否则返回None。

    MC对象属性：
    args: list  指令的参数列表 (不包括指令头)。
    text: str  指令的参数的文本 (去除了指令头的文本)。

    注意：
    必须要命令前缀匹配，才会触发。但如果你的命令前缀有''空字符串，任何消息都会触发。
    命令前缀在配置文件里设置。
    '''

    pure_msg = plaintext_if_prefix(text).strip()

    # 统一处理为列表
    if isinstance(commands, str):
        command_list: list = [commands]
    elif isinstance(commands, list):
        command_list = commands
    else:
        return None

    for item in command_list:
        # log.debug('item: ' + item)
        # 如果命令为空，就会理解为任何消息都会触发
        if item == '':
            # log.debug('command is empty')
            return MC( [], pure_msg)

        # 从此处开始，下方四个分支只会有一个会被触发
        # 先匹配带空格的，剩下的再匹配不带空格的
        if pure_msg.startswith(item + ' ') and not limit_arg_less:
            args = pure_msg.replace(item + ' ', '', 1).split()
            text = pure_msg.replace(item + ' ', '', 1)
            return MC( args, text)

        # gap_less：容许不加空格
        elif config.allow_gap_less and pure_msg.startswith(item) and not limit_arg_less:
            args = pure_msg.replace(item, '', 1).split()
            # print(args)
            text = pure_msg.replace(item, '', 1)
            return MC(args, text)

        # 完全匹配
        elif pure_msg == item:
            args = []
            text = ''
            return MC( args, text)

    else:
        return None










