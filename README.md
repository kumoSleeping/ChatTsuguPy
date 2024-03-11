
<h1 align="center"> Tsugu Python Frontend <img src="./logo.jpg" width="30" width="30" height="30" alt="tmrn"/> </h1>


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


<p align="center">
<br>  Python 编写的 Tsugu 前端模块


***

<h2 align="center"> 实现 </h2>


- [x] 自然语言输入 -> 返回结果
- [ ] 独立路由输入 -> 返回结果 `目前仅基础路由`
- [x] 本地数据库 (sqlite3)
- [x] 远程数据库 (客户端)
- [x] 配置项 (基础配置、代理、命令别名 等)


<h2 align="center"> 安装与更新 </h2>

## 安装 tsugu 模块
```shell
pip install tsugu
```

## 更新
```shell
pip install tsugu --upgrade
```

## 使用官方源安装
```shell
pip install tsugu --index-url https://pypi.org/simple/
```
## 后端需求

- 出图：需要支持 `v2 API` (2024.2.28日以后的后端版本)
- utils：需要支持 `v2 API` 
- 用户数据：需要一个启用了**数据库**的后端，需要支持 `v2 API`

> 三个后端设置可以不同，默认全部设置为**公共后端**。

***


<h2 align="center"> 测试与调用 </h2>




## 调用 `tsugu.bot`

- `bot` 是 `tsugu` 的一个同步函数，用于直接处理用户输入的自然语言并返回查询结果: 

```python
import base64
from PIL import Image
import io

import tsugu

# 四个参数，分别意味着 消息内容 用户id 平台 频道id
data = tsugu.bot('查卡 红 ksm 5x', '114514', 'red', '666808414')

# 如果返回值为 None 代表bot不发送任何消息。
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

> 在常用的qqbot中，群号就是 `channel_id`。   
> 当你使用QQ号作为 `user_id` 时，`platform` 可以填写 `red`。   


## 调用 `tsugu.database`

```python
import tsugu

tsugu.database(path="./data.db")

# 此操作会自动创建或使用本地数据库为 tsugu.bot 提供用户数据。
# 远程数据库将不使用。
# 更多功能可能在未来版本中添加。
```

## 查看与更改 `tsugu.config` 配置

- 查看默认配置文档: 
```py
import tsugu

tsugu.config.show_docs()  # 输出默认配置文档到控制台
```
- 你可以更改配置:   

```py
import tsugu

# 更改的后端地址。
tsugu.config.backend = "http://127.0.0.0.1:3000"

# 设置代理。
tsugu.config.use_proxies = True
tsugu.config.proxies = {"http": "http://127.0.0.1:1145", "https": "http://127.0.0.1:1919"}

# 添加关闭抽卡模拟的群号。
tsugu.config.ban_gacha_simulate_group_data = ["114514", "1919810"]

# 使用 `add_command_name` 和 `remove_command_name` 方法添加或删除命令名以添加别名或关闭命令。
tsugu.config.add_command_name(api="gacha", command_name="抽卡")
```
> 注意，不清楚的配置项请不要更改，更改配置项可能会导致不可预知的错误。



## 使用 `tsugu.router` 路由

- 如果想自己进行自然语言处理，你可以使用单独的路由:
```py
import tsugu

# 获取用户数据
reply = tsugu.router.get_user_data("red", "1234567890")

# 查卡
reply = tsugu.router.card("红 ksm", [0, 3], 5)

# 设置玩家车牌转发
reply = tsugu.router.set_car_forward("red", "1234567890", True)
```


***

<h2 align="center"> 相对应登录端？ </h2>

这不是一个好的时代， 但部署方式仍然是有不少的，如果有部署期望，可以看下面的 ▶️`客服ano酱指导` 进群聊聊天，我们会尽力帮助你。

基于 v2 api 的 `C#` + `Lagrange` 组合的登录端正由 [棱镜](https://github.com/DreamPrism) 开发中，敬请期待。   
基于本项目的 `NoneBot2` 插件也由 [zhaomaoniu](https://github.com/zhaomaoniu) 开发中，敬请期待。   



 <details>
<summary><b>客服ano酱指导(这里可以点击)</b></summary>
 
**注意，如果你不知道什么是BanGDream，请不要随意加群**    
**本群还是欢迎加群的（**    
[BanGDreamBot开发聊天群](https://qm.qq.com/q/zjUPQkrdpm)   
温馨的聊天环境～   

</details>

***

<h2 align="center"> 开发者的话 </h2>

> kumo: 我草我要4了   

> kumo: 未来还会继续完善以及同步更新喵，感谢大家的支持～  
&emsp;&emsp;&emsp;感谢提出建议的所有人～   
&emsp;&emsp;&emsp;也感谢山本和大家的付出与帮助!  

> zhaomaoniu: 这周末不是很想写代码

***






