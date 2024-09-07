
<h1 align="center"> Chat Tsugu Py <img src="./logo.jpg" width="30" width="30" height="30" alt="tmrn"/> </h1>


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


- 以 `satori-python` + `chronocat` 为例

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


## ❌ 同步多线程支持
- 4.0.0 后不再支持同步多线程，因为本人用不到。实现起来很简单，本包在导入时完成了 `Alconna` 的初始化，避免了多线程 `context` 错误，因此可以在多线程中使用 `tsugu`，欢迎有志人士一同完善。





## ⚙️ api settings

> 安装 `tsugu` 后可以直接导入 `tsugu_api_core` 的 `settings` 修改配置项。


```py 
from tsugu_api_core import settings

...
```

[tsugu_api settings 详细内容](https://github.com/WindowsSov8forUs/tsugu-api-python/blob/main/tsugu_api_core/settings.py)


---