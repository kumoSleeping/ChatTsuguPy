
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
- [ ] 独立路由输入 -> 返回结果 `部分支持`
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




## 调用 `tsugu.handler`

- `handler` 是 `tsugu` 的一个同步函数，用于直接处理用户输入的自然语言并返回查询结果: 

```python
import io
import tsugu

# 四个参数，分别意味着 消息内容 用户id 平台 频道id
for i in tsugu.handler('查卡 ars 1x', '1528593481', 'red', '666808414'):
    # 字符串
    print(i) if isinstance(i, str) else None
    # 图片
    print(f"[图像大小: {len(i) / 1024:.2f}KB]") if isinstance(i, bytes) else None
    # from PIL import Image
    # Image.open(io.BytesIO(i)).show() if isinstance(i, bytes) else None
```

> 在常用的qqbot中，群号就是 `channel_id`。   
> 当你使用QQ号作为 `user_id` 时，`platform` 可以填写 `red`。   


- 异步框架下，可以使用 `run_in_executor` 方法:

> 以 lagrange-python 群聊为例，其他异步框架请自行查阅文档。
```python
loop = asyncio.get_running_loop()
args = (event.msg, str(event.uin), 'red', str(event.grp_id))
response = await loop.run_in_executor(None, tsugu.handler, *args)

# 不发送消息
if not response:
    return

msg_list = []
for item in response:
    # 处理文本类型的消息
    msg_list.append(Text(item)) if isinstance(item, str) else None
    msg_list.append(await client.upload_grp_image(BytesIO(item), event.grp_id)) if isinstance(item, bytes) else None

await client.send_grp_msg(msg_list, event.grp_id)
```

## 调用 `tsugu.database`

```py
import tsugu

tsugu.database(path="./data.db")

# 此操作会自动创建或使用本地数据库为 tsugu.bot 提供用户数据。
# 远程数据库将不使用。
# 更多功能可能在未来版本中添加。
```
> 注意，先进行此操作，后进行 `load_config_json` 操作，旧版本 `config.json` 会覆盖数据库路径，导致数据库无法使用。


## 查看与更改 `tsugu.config` 配置

- 输出配置到 `config.json` 文件:
```py
import tsugu

tsugu.config.output_config_json('./config.json')
```

- 利用此文件，你可以更改配置项，然后重新加载配置:
```py
import tsugu

tsugu.config.load_config_json('./config.json')
```


- 你也可以直接更改配置，但不推荐:   

```py
import tsugu

# 更改的后端地址。
tsugu.config.backend = "http://127.0.0.0.1:3000"

# 添加关闭抽卡模拟的群号。
tsugu.config.ban_gacha_simulate_group_data = ["114514", "1919810"]
```
> 注意，不清楚的配置项请不要更改，更改配置项可能会导致不可预知的错误。




## 使用 `tsugu.router` 路由与内部方法

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

- 此外还暴露了一些内部方法，需要可以使用:

```py
import tsugu

tsugu.interior_local_method.bind_player_verification("red", "1234567890", True)
tsugu.interior_remote_method.bind_player_verification("red", "1234567890", 0, '1000011232', True)

tsugu.interior_local_method.submit_car_number_msg("123456 大分q1", "1234567890", "red")
```


***

<h2 align="center"> 相对应登录端 </h2>

| 部署方式 | 传送门 |
| --- | --- |
| **lpt 登陆端部署** | [![release](https://img.shields.io/github/v/release/kumoSleeping/lgr-tsugu-py?style=flat-square)](https://github.com/kumoSleeping/lgr-tsugu-py) |

基于 v2 api 的 `Go` + `Lagrange` 的登录端正由 [WindowsSov8](https://github.com/WindowsSov8forUs) 开发中，敬请期待。
基于 v2 api 的 `C#` + `Lagrange` 的登录端正由 [棱镜](https://github.com/DreamPrism) 开发中，敬请期待。   
基于本项目的 `NoneBot2` 插件也由 [zhaomaoniu](https://github.com/zhaomaoniu) 开发中，敬请期待。

 <details>
<summary><b>客服ano酱指导(这里可以点击)</b></summary>
 
**注意，如果你不知道什么是BanGDream，请不要随意加群**    
**本群还是欢迎加群的（**    
[BanGDreamBot开发聊天群](https://qm.qq.com/q/zjUPQkrdpm)   
温馨的聊天环境～   

</details>


