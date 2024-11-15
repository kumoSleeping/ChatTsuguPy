


<div align="center">

\[Tsugu-bot^2backend\]✨<img src="./logo.jpg" width="30" width="30" height="30" alt="tsugu"/>✨



_✨ user (Natural language) -> ⬆⬆⬆⬆  -> [Tsugu BanG Dream Bot](https://github.com/Yamamoto-2/tsugu-bangdream-bot?tab=readme-ov-file)  ✨_
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

## 📦 Install

```shell
pip install tsugu
```

> API powered by  <a href="https://github.com/WindowsSov8forUs/tsugu-api-python?tab=readme-ov-file">tsugu-api-python</a>

> Command matching provided by <a href="https://github.com/ArcletProject/Alconna">Alconna</a>

***

## 🚗 App
| 项目 | 说明 |
| --- | --- |
| [Tsugu QQ 官方机器人](https://bot.q.qq.com/s/b2vuxpu4g?id=102076262) | 主力项目 |
| Tomorin 私家机器人 | 私家车，基于标准用户数据库 |
| [一个 NoneBot 插件](https://github.com/zhaomaoniu/tsugu-bangdream-bot-py) | 无人维护，不如去用[这个](https://github.com/WindowsSov8forUs/nonebot-plugin-tsugu-bangdream-bot) |
|[lgr-py Tsugu](https://github.com/kumoSleeping/lgr-tsugu-py) | 无人维护，似了 |


## 📜 Feat

- 为改善用户体验，本包与 `koishi 插件` 在部分行为上略有不同。
  - 默认不需要命令头后跟上完整的空格（可关闭）。
  - `绑定玩家` `解除绑定` `刷新验证吗` 等自验证策略。
  - 基于 `Alconna` 的真 “可选参数” 。
  - 车站相关功能不主动支持绑定账号的配队信息，但被动渲染车站给出的配队信息。
  - 参数错误时输出完整的命令帮助信息。
  - 略有不同的车站屏蔽词策略。
  - 增加 `上传车牌` 命令，但仍然支持自动从文本开头提取车牌。
  - `主账号` 和 `解除绑定` 的不同行为。
- 争议功能
  - 暂时支持 玩家状态 \<serverName\> 策略
  - 暂不支持 shortcut类指令
    - 暂不支持 `国服模式` `国服玩家状态` 等指令
    - 而应该使用 `主服务器 国服` `玩家状态 国服` 等指令式响应。
  - 暂不支持 Tsugu 内部车站互通，只通 `bangdori station` 。
- 为了适应官方 BOT 的特性，本包提供了隐式一些非通用方法。
  - 当解除绑定用户数据库返回特定值时会被认定为安全模式，触发直接解除绑定操作。



## 📚 Async & Higher-Order Function
`cmd_generator` 是一个异步方法，用于直接处理用户输入的自然语言并返回查询结果:   


- 测试可用

```python
-------------
预发布版暂无示例
-------------
```

- 生产实操：以 `satori-python` + `chronocat` 为例

```python
from tsugu import cmd_generator

-------------
预发布版暂无示例
-------------
```
> 在常用的qqbot中，群号就是 `channel_id`。   
> 当你使用QQ号作为 `user_id` 时，`platform` 默认 `red`。   


## ✏️ Env

> Chat Tsugu Py 使用读取环境变量的方式改变一些配置

```zsh
# 命令头后是否必须跟上完整的空格才能匹配，例如 `查卡947` 与 `查卡 947` 。（默认值：false）
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


---