from flask import Flask, request
from main import API
from tsuguLP import tsugu_main


def menu():
    data = request.get_json()
    message = None
    if type(data['message']) == str:
        message = data['message']
    elif type(data['message']) == list:
        for d in data['message']:
            if d['type'] == 'text':
                message = d['data']['text']
    if message is None:
        return "不OK"
    user_id = data['user_id']
    group_id = data['group_id']
    rpl = tsugu_main(message, user_id, group_id)
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
                image_tag = f'[CQ:image,file=base64://{base64_data}]'
                modified_results.append(image_tag)
        result_string = ''.join(modified_results)
        API.send(result_string)
    if "tsugu可爱" == message:
        a = "你也可爱～"
        API.send(a)
    return "OK"
