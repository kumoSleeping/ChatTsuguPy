import base64
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageOps
import os
from io import BytesIO
import requests
import re


current_dir = os.path.dirname(__file__)
# 切换到当前文件所在的目录
os.chdir(current_dir)

# 定义一个全局的配置字典，用于存储插件配置信息
plugin_configurations = []

# 用于设置red实例基础信息
class Msg:
    IP = 'localhost'
    PORT = '16530'
    TOKEN = "ef9596b968925eafc5d8822438c70ab4242c9ba13f9a2e29be2feee4417008d8"

    def __init__(self):
        self.IP = self.IP
        self.PORT = self.PORT
        self.TOKEN = self.TOKEN


IP = Msg.IP
PORT = Msg.PORT
TOKEN = Msg.TOKEN


# 插件装饰器，用于装饰插件函数，被装饰的函数将被记录到plugin_configurations字典中，按顺序执行
def plugin(func):
    plugin_configurations.append(func)


# 解析cat_json
def c_j(cat_json):
    mm = str(cat_json['mm'])
    user_id = str(cat_json['user_id'])
    group_id = str(cat_json['group_id'])
    chat_type = str(cat_json['chat_type'])
    message_data = cat_json['message_data']
    return mm, user_id, group_id, chat_type, message_data


'''
方法：
- @plugin  装饰器用于装饰插件函数，被装饰的函数将被顺序执行
- send(message, group_id)  用于发送消息，接受两个参数，第一个参数是消息内容，第二个参数是群号
- c_j(send_json) 用于解析消息，接受一个参数，即send_json，返回五个值，分别是消息 内容，发送者QQ，群号，消息类型，原消息数据

at元素：
- API: at(user_id)  用于at某人，接受一个参数，即被at的人的QQ，str类型
- 文字码: ^AT=12345^ 用于at某人，12345即被at的人的QQ，str类型

image元素：
- API: p2b(image)  用于将pillow的Image对象转换为base64编码的字符串，接受一个参数，即Image对象
- 文字码: ^image={base64}^  用于发送图片，接受base64编码的字符串，str类型

=========================================================================PLUGIN_START

'''

from tsuguLP import tsugu_main


@plugin
def tsugulp(send_json):
    mm, user_id, group_id, chat_type, message_data = c_j(send_json)
    rpl = tsugu_main(mm, user_id, group_id)
    if not rpl:
        pass
    else:
        modified_results = []
        for item in rpl:
            if item['type'] == 'string':
                # 处理字符串类型的结果，可能是文本消息
                text_message = item['string']
                modified_results.append(text_message)
            elif item['type'] == 'base64':
                # 处理Base64编码的图像数据
                base64_data = item['string']
                # 将Base64数据包裹在^IMG=xxx^中并添加到文本中
                image_tag = f'^IMG={base64_data}^'
                modified_results.append(image_tag)
        result_string = ''.join(modified_results)
        send(result_string, group_id)
    if mm == 'tsuguLP':
        rpl = '''[tsuguLP] tsugu的python前端口实现
    Tsugu_Lite_Python 是一个基于 Tsugu-BanGDream-Bot 的 Python 轻量化前端脚本。

    部署教程：http://ks.ksm.ink/#/tsugu'''
        send(rpl, group_id)

@plugin
def tsugu_kawa(send_json):
    mm, user_id, group_id, chat_type, message_data = c_j(send_json)
    if mm == 'tsugu可爱':
        # 函数转换，发送消息
        send(f'^AT={user_id}^ ...\n没事，就@你一下\n {p2b(Image.open("../logo.jpg"))}', group_id)



'''
=========================================================================PLUGIN_END
'''

# 处理
def process_message(message_content):
    # 利用process_message_2_c_j函数，将message_content里面第一个text元素打包，合成send_json
    send_json = process_message_2_c_j(message_content)
    if not send_json:
        return
    rcv = send_json['mm'][0:15] + '...' if len(send_json['mm']) > 15 else send_json['mm']
    print(f"\033[92m[receive] [M] {rcv} [G] {send_json['group_id']} [S] {send_json['user_id']}\033[0m")

    '''启用的插件函数⬇️'''
    for plugin in plugin_configurations:
        plugin(send_json)


def process_message_2_c_j(message_content):
    # print(message_content)

    if message_content["type"] != "message::recv" or message_content['payload'] == []:
        return None

    # 提取消息元素列表
    elements = message_content['payload'][0]['elements']

    # 初始化结果字符串
    result_string = ""

    # 遍历消息元素
    for element in elements:
        if element['elementType'] == 1:  # 文字元素
            text_content = element['textElement']['content']
            result_string += text_content
        elif element['elementType'] == 2:  # 图片元素
            # base64_data = element['extBufForUI']
            image_tag = f'^IMG^'
            result_string += image_tag


    send_json = {
        "mm": result_string,
        "group_id": message_content['payload'][0]["peerUin"],
        "user_id": message_content['payload'][0].get("senderUin", ''),  # 可能不存在
        "chat_type": message_content['payload'][0]["chatType"],
        "message_data": message_content,
    }

    if result_string != '':
        return send_json
    else:
        return None

def p2b(img) -> str:
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode()
    b64_ksm = f"^IMG={img_str}^"
    return b64_ksm


# qq at
def at(user_id) -> str:
    return f"^AT={user_id}^"


# 调用发送消息
def send(rpl, group_id):
    # asyncio.run(send_message(rpl, 2, group_id))
    send_reply(chat_type=2, message=rpl, peer_uin=group_id)


def send_reply(chat_type, peer_uin, message):
    if message is None:
        return
    parts = re.findall(r'[^^]+', message)
    at_elements = []

    for idx, part in enumerate(parts):
        # 省略部分代码...

        # 添加at信息元素
        if part is None:
            continue

        if idx < len(parts):
            if part.startswith('AT='):
                at_uin = part[3:]

                element = {
                    "elementType": 1,
                    "textElement": {
                        "content": f"@时空猫猫",
                        "atType": 2,
                        "atNtUin": at_uin
                    }
                }
                at_elements.append(element)
                continue

        # 添加图片元素
        if idx < len(parts):
            if part.startswith('IMG='):
                img_uin = part[4:]
                image_info = upload_image_base64(img_uin)

                if image_info:
                    pic_element = {
                        "elementType": 2,
                        "picElement": {
                            "md5HexStr": image_info["md5"],
                            "fileSize": image_info["fileSize"],
                            "picHeight": image_info["imageInfo"]["height"],
                            "picWidth": image_info["imageInfo"]["width"],
                            "fileName": f"{image_info['md5']}.{image_info['imageInfo']['type']}",
                            "sourcePath": image_info["ntFilePath"]
                        }
                    }
                    at_elements.append(pic_element)
                    continue

        # 添加普通文本元素
        if part:
            element = {
                "elementType": 1,
                "textElement": {
                    "content": part
                }
            }
            at_elements.append(element)

    reply_packet = {
        # "type": "message::send",
        # "payload": {
            "peer": {
                "chatType": chat_type,
                "peerUin": peer_uin
            },
            "elements": at_elements
        # }
    }

    def send_http_request(data):
        headers = {
            "Content-Type": "application/json",
            'Authorization': f'Bearer {TOKEN}'  # 使用 token 进行身份验证
        }
        # print(data)
        response_ = requests.post(f"http://{IP}:{PORT}/api/message/send", json=data, headers=headers)
        print(f"\033[93m[send] ----------------- [Success!] \033[0m")

        return

    response = send_http_request(reply_packet)


def upload_image_base64(img_file):
    try:
        img_data = base64.b64decode(img_file)
        data = {
            "file": ("image.png", img_data, "image/png")
        }
        headers = {
            'Authorization': f'Bearer {TOKEN}'
        }
        response = requests.post(f"http://{IP}:{PORT}/api/upload", files=data, headers=headers, timeout=5)
        if response.status_code == 200:
            image_info = response.json()
            return image_info
        else:
            print(f"图片上传失败：HTTP状态码 {response.status_code}")
    except requests.exceptions.Timeout:
        print("图片上传超时")
    except Exception as e:
        print(f"图片上传时出现异常：{e}")
    return None









