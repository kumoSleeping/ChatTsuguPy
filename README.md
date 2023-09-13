
<h1 align="center"> tsugu-bangdream-bot-lite-py </h1>


<div align="center"> <img src="/logo.jpg" width="120"/> </div>

<div align="center">  Python编写的Tsugu前端、登陆端脚本 基于<a href="https://github.com/Yamamoto-2/tsugu-bangdream-bot">tsugu-bangdream-bot</a>后端
</div>
<div align="center">  Tsugu部署方法(长期更新)：http://ks.ksm.ink/#/tsugu </a>
</div>

***

### 部署第一步：配置环境
> 环境需求：python3
> 推荐Python3.10 - 3.12
> ~~安装时记得勾选添加到环境变量PATH~~

```shell
# 检测是否安装pip
pip -v

# 安装所需外部库
pip install pillow requests websockets aiohttp flask

# 如果缺少内部库pip install即可
# 可能需要尝试检查环境变量或使用pip3
```

### 部署第二步：配置聊天平台登录程序

**使用Chronocat（推荐）：[Chronocat](http://chronocat.ksm.ink)**

使用Chronocat无需配置，token 被默认存储在 `%AppData%/BetterUniverse/QQNT/RED_PROTOCOL_TOKEN` 或 `~/BetterUniverse/QQNT/RED_PROTOCOL_TOKEN` 中， 首次启动 Chronocat 时会自动生成，并保持不变。

*Windows用户打开文件管理器，在地址栏输入`%AppData%`即可跳转*

### 部署第三步：配置登陆端与tsuguLP.py文件配置

**使用Chronocat登陆端：**

1.以编辑形式打开 `c_p_3.py` 文件，在"your_token"填写你在上一步找到的token
```python
class Msg:
    IP = 'localhost'
    PORT = '16530'
    TOKEN = "your_token"
```
保存文件。

2.打开同目录下`tsuguLP.py`文件，修改开头信息。
```python
BACKEND_URL = 'http://tsugubot.com:8080'  # 后端地址
default_use_easy_bg = True  # 是否使用简易背景
default_servers = ["3", "0"]   # 默认服务器顺序
BindPlayer_url = ''  # 请填写玩家绑定数据库API
self_id = 'tsugu'  # bot称呼，后面会用到 swc off 称呼 来关闭bot
help_word = 'help'  # help 触发词（不能有空格）

folder_path = Path('tsugu_config')  # 配置文件存储位置，可以不管
bandoriStationToken = 'ZtV4EX2K9Onb'
source = 'Tsugu'
```

其中，玩家状态后端地址`BindPlayer_url`是必须要修改的，可加入[BanGDreamBot开发聊天群](https://qm.qq.com/q/zjUPQkrdpm)获取，或根据[方案](https://github.com/kumoSleeping/GetQPlayerUid)自己实现

3.终端 / cmd / powershell 运行`catbot3.py`
```shell
cd 目标文件夹
python catbot3
# python3 catbot3
```
**至此，如果不出意外，Tsugu已经可以使用。**



### 其他聊天平台登录程序...(非必需步骤)

本项目含有Onebot登陆段(v11)但未经过测试。

**使用Onebot ：[gocqhttp](https://docs.go-cqhttp.org) + [qsign](https://github.com/fuqiuluo/unidbg-fetch-qsign)**

使用gocqhttp需要选择http协议：
```yml
# 连接服务列表
servers:
  - http: # HTTP 通信设置
      address: 0.0.0.0:5700 # HTTP(flask)监听地址
      version: 11     # OneBot协议版本, 支持 11/12
      timeout: 5      # 反向 HTTP 超时时间, 单位秒，<5 时将被忽略
      long-polling:   # 长轮询拓展
        enabled: false       # 是否开启
        max-queue-size: 2000 # 消息队列大小，0 表示不限制队列大小，谨慎使用
      middlewares:
        <<: *default # 引用默认中间件
      post:           # 反向HTTP POST地址列表
      - url: http://localhost:5701
        secret: ''                  # 密钥
        max-retries: 0             # 最大重试，0 时禁用
        retries-interval: 100000      # 重试时间，单位毫秒，0 时立即
```


**尝试接入自己的python程序/bot：...**
使用`tsuguLP.py`或`tsuguLP_async.py`接入您的同步或异步代码，接入方法参考登陆端的`c_p_3`或`menu`即可。

`tsuguLP.py`位于登陆端文件夹，两登陆端的`tsuguLP.py`文件是一样的，
`tsuguLP_async.py`位于scripts_async`scripts_async`文件夹，具有异步特性，理论上无其他改动，由@zhaomaoniu 维护。


### 自建后端(非必需步骤)
tsugu的仓库：https://github.com/Yamamoto-2/tsugu-bangdream-bot

首先，请确保你安装了node.js v18：https://nodejs.cn/download/   
目前Tsugu开发时的环境为v18.16.0

后端在Tsugu仓库的/backend目录，请安装对应的依赖   
在/backend目录启动命令行，输入`npm install`   
直接运行tsugu后端，或者使用命令行运行tsugu后端   
在/backend目录运行`ts-node .\src\app.ts`   

在这个基础上，请安装ts-node，可以安装pm2来保证稳定性   
在命令行输入:   
`npm install -g ts-node`     
`npm install -g pm2`   

使用pm2:   
`pm2 start ecosystem.config.js`   

***建议安装pm2定时任务插件，控制日志内存占用。***



