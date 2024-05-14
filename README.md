
<h1 align="center"> Tsugu Bot Py <img src="./logo.jpg" width="30" width="30" height="30" alt="tmrn"/> </h1>


<p align="center">

<a href="https://github.com/Yamamoto-2/tsugu-bangdream-bot">
    <img src="https://img.shields.io/badge/tsugubangdream bot - v2 api-yellow" alt="license">
  </a>

<a href="https://github.com/kumoSleeping/tsugu-python-frontend?tab=MIT-1-ov-file">
    <img src="https://img.shields.io/github/license/kumoSleeping/tsugu-python-frontend" alt="license">
  </a>
<a href="https://pypi.org/project/tsugu/">
    <img src="https://img.shields.io/pypi/v/tsugu.svg" alt="license">
  </a>
</p>


***


- `tsugu`
  - [x] 自然语言输入 -> 返回结果
  - [x] 远程数据库 
  - [x] 本地数据库 


- `tsugu.async`
  - [x] 自然语言输入 -> 返回结果
  - [x] 远程数据库 
  - [ ] 本地数据库





```shell
pip install tsugu
```
> Powered by  <a href="https://github.com/WindowsSov8forUs/tsugu-api-python?tab=readme-ov-file">tsugu-api-python</a>


***


<h2 align="center"> 测试与调用 </h2>

## handler

- `handler` 是 `tsugu` 的一个同步函数，用于直接处理用户输入的自然语言并返回查询结果: 

```python
import tsugu

# tsugu.database(path="./data.db")

# 四个参数，分别意味着 消息内容 用户id 平台 频道id
for i in tsugu.handler(message='查卡 ars 1x', user_id='1528593481', platform='red', channel_id='666808414'):
    print('文本: ',i) if isinstance(i, str) else None
    print(f"[图片]") if isinstance(i, bytes) else None
```

```python
import tsugu_async

# tsugu_async.config.reload_from_json('./config.json')

async def main():
    res = await tsugu_async.handler(message='查卡 ars 1x', user_id='1528593481', platform='red', channel_id='666808414')
    for i in res:
        print('文本: ',i) if isinstance(i, str) else None
        print(f"[图片]") if isinstance(i, bytes) else None
```


> 在常用的qqbot中，群号就是 `channel_id`。   
> 当你使用QQ号作为 `user_id` 时，`platform` 可以填写 `red`。   

## handler_raw
如果你方便使用 base64，`handler_raw` 方法或许会更好  
`tsugu` 后端本身返回此数据结构，如果你的bot可以直接发送 `base64` 类图片，这个方法会节省不必要的开销。

```python
import tsugu

for i in tsugu.handler_raw(message='查卡 ars 1x', user_id='1528593481', platform='red', channel_id='666808414'):
    print('文本: ',i) if i['type'] == 'text' else None
    print(f"[图片]") if i['type'] == 'base64' else None


import tsugu_async
...
```


## 使用本地数据库(不支持`tsugu_async`)
本地数据库由 `sqlite3` 提供，你可以使用 `tsugu.database` 来创建或使用本地数据库。

```py
import tsugu

tsugu.database(path="./data.db")
```

> 此操作会自动创建或使用本地数据库为 tsugu.bot 提供用户数据。  
> 远程数据库将不使用。

## 配置


> 随意更改配置项可能会导致不可预知的错误。

### tsugu_api settings

```py
from tsugu_api import settings

settings.timeout = 10
'''
请求超时时间
'''

settings.proxy = ''
'''
代理地址
'''

settings.backend_url = 'http://tsugubot.com:8080'
'''
后端地址
默认为 Tsugu 官方后端，若有自建后端服务器可进行修改。
'''

settings.backend_proxy = True
'''
是否使用后端代理
当设置代理地址后可修改此项以决定是否使用代理。
默认为 True，即使用后端代理。若使用代理时后端服务器无法访问，可将此项设置为 False。
'''

settings.userdata_backend_url = 'http://tsugubot.com:8080'
'''
用户数据后端地址
默认为 Tsugu 官方后端，若有自建后端服务器可进行修改。
'''

settings.userdata_backend_proxy = True
'''
是否使用用户数据后端代理
当设置代理地址后可修改此项以决定是否使用代理。
默认为 True，即使用后端代理。若使用代理时后端服务器无法访问，可将此项设置为 False。
'''

settings.use_easy_bg = True
'''
是否使用简易背景，使用可在降低背景质量的前提下加快响应速度。
默认为 True，即使用简易背景。若不使用简易背景，可将此项设置为 False。
'''

settings.compress = True
'''
是否压缩返回数据，压缩可减少返回数据大小。
默认为 True，即压缩返回数据。若不压缩返回数据，可将此项设置为 False。
'''

```

```py
from tsugu_api_async import settings
...
```

### tsugu_async config

```py
from tsugu import config

config.prefix = ['/', '']
'''
命令前缀
最后一个参数如果不是空字符串，则只有在命令前缀符合时才会触发命令。
'''

config.allow_gap_less = True
'''
是否允许命令与参数之间没有空格
'''

config.get_remote_user_data_max_retry = 3
'''
获取远程用户数据最大重试次数
'''

config.token_name = "Tsugu"
'''
bandori station token
'''
config.bandori_station_token = "ZtV4EX2K9Onb"
'''
bandori station token
'''

config.ban_gacha_simulate_group_data = []
'''
需要关闭模拟抽卡的群
'''

config.commands = ...

config.user_commands = ...
```

```py
from tsugu_async import config
...
```



***

 <details>
<summary><b>客服ano酱指导(这里可以点击)</b></summary>
 
**注意，如果你不知道什么是BanGDream，请不要随意加群**    
**本群还是欢迎加群的（**    
[BanGDreamBot开发聊天群](https://qm.qq.com/q/zjUPQkrdpm)   
温馨的聊天环境～   

</details>


下方已无内容。

<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>

🐱: 喵