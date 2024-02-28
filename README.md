


[//]: # (<h1 align="center"> TomorinBOT  <img src="./DemoProject2/register/example/eg.jpg" width="30" height="30" alt="tmrn"/> </div></h1>)
<h1 align="center"> Tsugu-Lite-Py  <img src="./logo.jpg" width="120"" width="30" height="30" alt="tmrn"/> </div></h1>


<p align="center">

<a href="https://github.com/Yamamoto-2/tsugu-bangdream-bot">
    <img src="https://img.shields.io/badge/tsugu-bangdream bot-yellow" alt="license">
  </a>

<a href="https://github.com/kumoSleeping/tsugu-bangdream-bot-lite-py?tab=MIT-1-ov-file">
    <img src="https://img.shields.io/github/license/kumoSleeping/TomorinBot" alt="license">
  </a>
<a href="https://www.python.org/">
    <img src="https://img.shields.io/badge/python-3.10+-blue?logo=python&logoColor=edb641" alt="license">
  </a>

</p>
<p align="center">
<br>  Python编写的 Tsugu 前端

<br> 基于 <a href="https://github.com/Yamamoto-2/tsugu-bangdream-bot">tsugu-bangdream-bot</a> v2 api 后端



***

<h2 align="center"> 为什么不再提供登录端？ </h2>

## 黑暗时代...

因为这不是一个好的时代，当下一个好的时代到来时，我们会再次提供登录端。   
但部署方式仍然是有不少的，如果有部署期望，可以翻到页面底部 `客服ano酱指导` 聊聊天，我们会尽力帮助你。

另外， `C#` + `Lagrange` 组合的登录端正由 [棱镜](https://github.com/DreamPrism) 开发中，敬请期待。   
基于本项目的 `NoneBot2` 插件也由 [zhaomoaniu](https://github.com/zhaomaoniupi) 开发中，敬请期待。   
<h2 align="center"> 环境需求 </h2>

## Python 第三方库
```shell
pip install requests PyYAML
```
如果您要使用 `test` 函数测试，您还需要安装 `Pillow` 来显示图片
```shell
pip install requests pillow
```
## 后端功能

- 出图：需要支持 `v2 API` (2024.2.28日以后的后端版本)
- utils：需要支持 `v2 API` 
- 用户数据：需要一个启用了**数据库**的后端，需要支持 `v2 API`

> 三个后端可以设置为不同，默认全部设置为**公共后端**。

<h2 align="center"> 使用 test 函数测试 </h2>

你可以发现 `main.py` 底部有这样一行

```python
test(main('查卡 红 ksm 5x', '114514', 'red', '666808414'))
```

直接运行 `main.py` 即可测试。修改传入参数可以测试不同的功能。


<h2 align="center"> 接入 Python 程序 / BOT </h2>

## 前提

- 你会简单的使用你即将接入的 Python 程序 / BOT。
- 一些非常简单的py知识。
- 注释掉 `main.py` 底部的 `test` 函数。
- 可能需要修改 `from utils import *` 为 `from .utils import *`。(相对导入)

***
## 调用 
`main.py` 提供了一个 `main` 同步函数，他需要 `message` `user_id` `platform` `channel_id` 四个参数，分别意味着 **消息内容** **用户id** **平台** **频道id**。   
在常用的qqbot中，群号就是 `channel_id`。   
当你使用QQ号作为 `user_id` 时，`platform` 可以填写 `red`。   

## 返回

```json
[{"type": "string", "string": string},
{"type": "base64", "string": string}, ... ]
```
当 type 为 string 时，string 为消息内容，可以直接发送到客户端。   
当 type 为 base64 时，string 为图片的 base64 编码，需要解码后发送到客户端。   
可能会返回多个结果。  
如果返回值为 `None` 代表bot不发送任何消息。   

## 举例
```python
# 监听每一条文字消息
@on.message_created
def tsugulp(event):
    # 调用main函数
    rpl = main(event.message.content, event.user.id, 'red', event.message.id)
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






