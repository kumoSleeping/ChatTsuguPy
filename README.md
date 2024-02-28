


[//]: # (<h1 align="center"> TomorinBOT  <img src="./DemoProject2/register/example/eg.jpg" width="30" height="30" alt="tmrn"/> </div></h1>)
<h1 align="center"> Tsugu-Lite-Py  <img src="./logo.jpg" width="120"" width="30" height="30" alt="tmrn"/> </div></h1>


<p align="center">

<a href="https://github.com/Yamamoto-2/tsugu-bangdream-bot">
    <img src="https://img.shields.io/badge/tsugu-bangdream bot-yellow" alt="license">
  </a>

<a href="https://github.com/kumoSleeping/tsugu-bangdream-bot-lite-py?tab=MIT-1-ov-file">
    <img src="https://img.shields.io/github/license/kumoSleeping/TomorinBot" alt="license">
  </a>
<a href="https://pypi.org/project/tsugu/">
    <img src="https://img.shields.io/pypi/v/tsugu.svg
" alt="license">
  </a>

</p>
<p align="center">
<br>  Python编写的 Tsugu 前端

<br> 基于 <a href="https://github.com/Yamamoto-2/tsugu-bangdream-bot">tsugu-bangdream-bot</a> v2 api 后端



***


<h2 align="center"> 安装 </h2>

## 安装 tsugu 模块
```shell
pip install package_name --index-url https://pypi.org/simple/
```
## 后端需求

- 出图：需要支持 `v2 API` (2024.2.28日以后的后端版本)
- utils：需要支持 `v2 API` 
- 用户数据：需要一个启用了**数据库**的后端，需要支持 `v2 API`

> 三个后端可以设置为不同，默认全部设置为**公共后端**。

<h2 align="center"> 测试与接入 </h2>

***
## 调用 tsugu
`tsugu` 是一个同步函数，需要 `message` `user_id` `platform` `channel_id` 四个参数，分别意味着 **消息内容** **用户id** **平台** **频道id**。   
在常用的qqbot中，群号就是 `channel_id`。   
当你使用QQ号作为 `user_id` 时，`platform` 可以填写 `red`。   


```py
from tsugu import tsugu_config, tsugu

data = tsugu('查卡 红 ksm 5x', '114514', 'red', '666808414')
```

## 返回

```json
[{"type": "string", "string": string},
{"type": "base64", "string": string}, ... ]
```
当 type 为 string 时，string 为消息内容，可以直接发送到客户端。   
当 type 为 base64 时，string 为图片的 base64 编码，需要解码后发送到客户端。   
可能会返回多个结果。  
如果返回值为 `None` 代表bot不发送任何消息。   

## 测试例

```python
import base64
from PIL import Image
import io

from tsugu import tsugu_config, tsugu

data = tsugu('查卡 红 ksm 5x', '114514', 'red', '666808414')

if not data:
    print("[无反馈数据]")

for item in data:
    if item["type"] == "string":
        print(f"[文字信息]\n{item['string']}")
    elif item["type"] == "base64":
        image_data = base64.b64decode(item["string"])
        print(f"[图像大小: {len(image_data) / 1024:.2f}KB]")
        Image.open(io.BytesIO(image_data)).show()
    else:
        print(item)
```
上面的代码使用 `pillow` 库，将返回值处理成字符串或者图片输出。


## 更改 `tsugu_config` 配置

当你在绝大部分只能编辑器打出 `tsugu_config.` 时，编辑器静态检查会提示你可以更改的配置，以及一系列 `set_xxx` 函数。   

例如，你可以更改的后端地址。
```py
from tsugu import tsugu_config

tsugu_config.set_backend('http://127.0.0.1:3000')
```

你可以设置代理。
```py
from tsugu import tsugu_config

tsugu_config.set_use_proxies(True)
tsugu_config.set_proxies('http://127.0.0.1:1080')
```

你可以添加关闭抽卡模拟的群号。
```py
from tsugu import tsugu_config

tsugu_config.add_ban_gacha_simulate_group_data('114514')
```

等等... 文档会在后续更新中补充。

## 机器人接入例

```python
from core import on
from tsugu import tsugu_config, tsugu

# 监听每一条文字消息
@on.message_created
def tsugulp(event):
    # 设置代理
    tsugu_config.set_use_proxies(True)
    # 添加关闭抽卡模拟的群号
    tsugu_config.add_ban_gacha_simulate_group_data('114514')
    tsugu_config.add_ban_gacha_simulate_group_data('1919810')
    # 调用 tsugu
    rpl = tsugu(event.message.content, event.user.id, 'red', event.message.id)
    # 如果返回值为None，不发送任何消息
    if not rpl:
        return

    def handle_string(item):
        return item['string']

    def handle_base64(item):
        base64_data = item['string']
        return f'<img src="data:image/png;base64,{base64_data}"/>'

    handlers = {
        'string': handle_string,
        'base64': handle_base64,
    }
    # 使用列表推导式，将返回值处理成字符串
    modified_results = [handlers[item['type']](item) for item in rpl if item['type'] in handlers]
    result_string = ''.join(modified_results)
    # 发送消息
    event.message_create(result_string)
```

这是随机挑选的一个 `satori` 协议机器人框架的 `tsugu` 接入实现，对于绝大部分 `Python` 机器人框架，接入方法大同小异。唯一可能需要处理的可能就是异步函数的调用问题。   



<h2 align="center"> 为什么不再提供登录端？ </h2>

## 黑暗时代...

因为这不是一个好的时代，当下一个好的时代到来时，我们会再次提供登录端。   
但部署方式仍然是有不少的，如果有部署期望，可以翻到页面底部 `客服ano酱指导` 聊聊天，我们会尽力帮助你。

另外， `C#` + `Lagrange` 组合的登录端正由 [棱镜](https://github.com/DreamPrism) 开发中，敬请期待。   
基于本项目的 `NoneBot2` 插件也由 [zhaomoaniu](https://github.com/zhaomaoniupi) 开发中，敬请期待。   



 <details>
<summary><b>客服ano酱指导</b></summary>
 
**注意，如果你不知道什么是BanGDream，请不要随意加群**    
**本群还是欢迎加群的（**    
[BanGDreamBot开发聊天群](https://qm.qq.com/q/zjUPQkrdpm)   
温馨的聊天环境～   

</details>

**未来还会继续完善以及同步更新的，感谢大家的支持！**   
**也感谢山本和大家的付出**

***






