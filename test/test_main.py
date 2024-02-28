from tsugu import tsugu_config, tsugu
import unittest


class TestTsugu(unittest.TestCase):

    def test_tsugu(self):
        def text_response(string):
            return [{"type": "string", "string": string}]

        def show_back_msg(data):
            import base64
            from PIL import Image
            import io

            if not data:
                return "[无反馈数据]"

            for item in data:
                if item["type"] == "string":
                    print(f"[文字信息]\n{item['string']}")
                elif item["type"] == "base64":
                    image_data = base64.b64decode(item["string"])
                    print(f"[图像大小: {len(image_data) / 1024:.2f}KB]")
                    Image.open(io.BytesIO(image_data)).show()
                else:
                    print(item)

        self.subTest(
            tsugu_config.set_use_proxies(True)
        )
        self.subTest(
            tsugu_config.set_proxies({
                "http": "http://127.0.0.1:7890",
                "https": "http://127.0.0.1:7890"
            })
        )
        self.subTest(
            show_back_msg(
                tsugu('查卡 ', '114514', 'red', '666808414'),
            )
        )


if __name__ == '__main__':
    unittest.main()


