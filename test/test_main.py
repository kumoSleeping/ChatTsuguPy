import tsugu
import unittest


class TestTsugu(unittest.TestCase):

    def test_tsugu(self):
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

        # self.subTest(
        #     tsugu.config.show_docs()
        # )

        # tsugu.config.utils_backend = 'http://127.0.0.1:3000'
        # tsugu.config.ban_gacha_simulate_group_data = ['666808414']

        self.subTest(
            show_back_msg(
                tsugu.bot('解除绑定', '1528593481', 'red', '666808414'),
            )
        )

        # self.subTest(
        #     show_back_msg(
        #         tsugu.router.ycx('100', [3, 0], 0),
        #     )
        # )


if __name__ == '__main__':
    unittest.main()


