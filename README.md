
<h1 align="center"> Chat Tsugu Py <img src="./logo.jpg" width="30" width="30" height="30" alt="tsugu"/> </h1>


<div align="center">

_✨ Python 编写的 [TsuguBanGDreamBot](https://github.com/Yamamoto-2/tsugu-bangdream-bot?tab=readme-ov-file) 自然语言交互库  ✨_

</div>

<p align="center">
<a href="https://github.com/Yamamoto-2/tsugu-bangdream-bot">
    <img src="https://img.shields.io/badge/tsugubangdream bot - api-yellow" alt="license">
  </a>

<a href="https://github.com/kumoSleeping/tsugu-python-frontend?tab=MIT-1-ov-file">
    <img src="https://img.shields.io/github/license/kumoSleeping/tsugu-python-frontend" alt="license">
  </a>
<a href="https://pypi.org/project/tsugu/">
    <img src="https://img.shields.io/pypi/v/tsugu.svg" alt="license">
  </a>
</p>

---

## 📦 安装

```shell
pip install tsugu --upgrade
```

> API powered by  <a href="https://github.com/WindowsSov8forUs/tsugu-api-python?tab=readme-ov-file">tsugu-api-python</a>

> Command matching provided by <a href="https://github.com/ArcletProject/Alconna">Alconna</a>

***

## 📚 异步支持
- 4.0.0 后需要异步环境处理。



## 📖 使用
`cmd_generator` 是一个异步方法，用于直接处理用户输入的自然语言并返回查询结果:   


- 测试可用

```python
import tsugu
import asyncio
print(asyncio.run(tsugu.cmd_generator('查活动', '114514')))
# 输出：[{'type': 'string', 'string': '参数 word 丢失\n查活动 <...word> \n根据活动名、乐队、活动ID等查询活动信息\n使用示例:\n查活动 绿 tsugu :返回所有属性加成为pure，且活动加成角色中包括羽泽鸫的活动列表\n查活动 177 :返回177号活动的信息'}]
```

- 生产实操：以 `satori-python` + `chronocat` 为例

```python
from tsugu import cmd_generator

@app.register_on(EventType.MESSAGE_CREATED)
async def on_message_(account: Account, event: Event):
    
    async def send_active_message(messages: dict):
        message = messages.get('message', None)
        if message:
            await account.send(event, E.quote(event.message.id).dumps() + message)
                
    if msg := cmd_select(event, prefix=['.']):
        rpl = await cmd_generator(message=msg, user_id=event.user.id,platform='red', message_id=event.message.id, active_send_func=send_active_message)
        if not rpl:
            pass
        else:
            modified_results = []
            for item in rpl:
                if item['type'] == 'string':
                    # 处理字符串类型的结果，可能是文本消息
                    text_message = item['string'].replace("<", "&lt;").replace(">", "&gt;")
                    modified_results.append(text_message)
                elif item['type'] == 'base64':
                    # 处理Base64编码的图像数据
                    base64_data = item['string']
                    # 将Base64数据包裹在^IMG=xxx^中并添加到文本中
                    image_tag = f'<img src="data:image/png;base64,{base64_data}"/>'

                    modified_results.append(image_tag)
            result_string = ''.join(modified_results)
            await account.send(event, E.quote(event.message.id).dumps() + result_string)

```
> 在常用的qqbot中，群号就是 `channel_id`。   
> 当你使用QQ号作为 `user_id` 时，`platform` 默认 `red`。   


## ✏️ 环境变量

> Chat Tsugu Py 使用读取环境变量的方式改变一些配置

```zsh
# 命令头后是否必须更上完整的空格才能匹配，例如 `查卡947` 与 `查卡 947` 。（默认值：false）
export TSUGU_COMPACT='false' 

# 设置请求超时时间（默认值：120秒）
export TSUGU_TIMEOUT=120

# 设置代理地址（默认值：空字符串）
export TSUGU_PROXY=''

# 设置后端地址（默认值：http://tsugubot.com:8080）
export TSUGU_BACKEND_URL='http://tsugubot.com:8080'

# 设置是否使用后端代理（默认值：true）
export TSUGU_BACKEND_PROXY='true'

# 设置用户数据后端地址（默认值：http://tsugubot.com:8080）
export TSUGU_USERDATA_BACKEND_URL='http://tsugubot.com:8080'

# 设置是否使用用户数据后端代理（默认值：true）
export TSUGU_USERDATA_BACKEND_PROXY='true'

# 设置是否使用简易背景（默认值：true）
export TSUGU_USE_EASY_BG='true'

# 设置是否压缩返回数据（默认值：true）
export TSUGU_COMPRESS='true'
```

# 🤖 特性

- 为改善用户体验，本包与 `koishi 插件` 在部分行为上略有不同。
  - BOT 玩家状态绑定/解绑策略自验证策略
  - 基于 `Alconna` 的真 “可选参数” 。

- 为了适应官方 BOT 的特性，本包提供了隐式一些非通用方法。
  - 当解除绑定用户数据库返回特定值时会被认定为安全模式，触发直接解除绑定操作。

---