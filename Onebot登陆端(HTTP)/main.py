from flask import Flask, request
import requests
import menu

FLASK_PORT = 5701
HTTP_PORT = 5700

app = Flask(__name__)


class API:
    @staticmethod
    def send(message):
        data = request.get_json()
        message_type = data['message_type']
        if 'group' == message_type:
            group_id = data['group_id']
            params = {
                "message_type": message_type,
                "group_id": str(group_id),
                "message": message
            }
        else:
            user_id = data['user_id']
            params = {
                "message_type": message_type,
                "user_id": user_id,
                "message": message
            }
        url = f"http://127.0.0.1:{HTTP_PORT}/send_msg"

        requests.post(url, json=params)  # Changed to POST and used json=params


@app.route('/', methods=["POST"])
def post_data():
    data = request.get_json()
    print(data)
    if data['post_type'] == 'message':
        message = data['message']
        if "[CQ:" in message:
            # 防止车牌误匹配
            return "这条消息，不需要了"
        print(message)
        menu.menu()
    else:
        print("暂不处理")

    return "OK"


if __name__ == '__main__':
    # 此处的 host和 port对应上面 yml文件的设置
    app.run(host='0.0.0.0', port=FLASK_PORT)  # 保证和我们在配置里填的一致
