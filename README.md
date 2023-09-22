
<h1 align="center"> tsugu-bangdream-bot-lite-py </h1>


<div align="center"> <img src="./logo.jpg" width="120"/> </div>
<div align="center">v0.3.0</div>
<div align="center">  Python编写的Tsugu前端、登陆端脚本 基于<a href="https://github.com/Yamamoto-2/tsugu-bangdream-bot">tsugu-bangdream-bot</a>后端
</div>
<div align="center">  Tsugu部署方法(长期更新)：http://ks.ksm.ink/#/tsugu </a>
</div>

***

**环境需求:**
> 推荐Python3.10 - 3.12
> ~~安装时记得勾选添加到环境变量PATH~~

```shell
# 检测是否安装pip
pip -v

# 安装所需外部库
pip install pillow requests websockets aiohttp flask pydantic

# 如果缺少内部库pip install即可
# 可能需要尝试检查环境变量或使用pip3
```

<h2 align="center"> 使用Chronocat（推荐） </h2>

***

### 配置Chronocat登录到聊天平台

请前往[Chronocat](https://chronocat.vercel.app/)官网下载LiteLoaderQQNT版本的Chronocat

在0.0.46版本以后，请浏览https://chronocat.vercel.app/config/
修改配置，获取token


```markdown
0.0.45方法：使用Chronocat无需配置，token 被默认存储在 `%AppData%/BetterUniverse/QQNT/RED_PROTOCOL_TOKEN` 或 `~/BetterUniverse/QQNT/RED_PROTOCOL_TOKEN` 中， 首次启动 Chronocat 时会自动生成，并保持不变。

*Windows用户打开文件管理器，在地址栏输入`%AppData%`即可跳转*

未来几个版本，如果是新安装的用户，RED_PROTOCOL_TOKEN文件仍然会生成，并保持和chronocat.yml里token一致，这样先前做了自动获取token逻辑的框架仍然能正常工作，不会因为用户安装的是0.0.46就找不到token了。
但不建议再使用这个文件。新框架从0.0.46起建议让用户在chronocat.yml里获取tojen。
```




### 配置登陆端

**直接命令行运行Chronocat登陆端**   

```shell
cd 目标文件夹
python catbot3.py
# python3 catbot3
```
会出现类似下面的提示，表示创建好了tsugu_config文件夹，请修改文件夹内的config.json


```markdown
已创建personal_config文件/Users/kumo/tsugu-bangdream-bot-lite-py/Chronocat登陆端/tsugu_config/personal_config.json
默认配置已写入到: /Users/kumo/tsugu-bangdream-bot-lite-py/Chronocat登陆端/tsugu_config/config.json
请修改配置后重启。
免责声明：
    ......
```
tsugu_config文件夹目录内容：
```
- tsugu_config
  - config.json  总配置项 需要修改
  - help_config.txt  总配置项修改帮助指南
  - personal_config.json  用户个人配置，无需手动修改

注意json基本语法规则，不能有注释，注意英文逗号，英文双引号
```

其中，玩家状态后端地址`BindPlayer_url`是必须要修改的，可加入[BanGDreamBot开发聊天群](https://qm.qq.com/q/zjUPQkrdpm)获取，或根据[方案](https://github.com/kumoSleeping/GetQPlayerUid)自己实现



**再次命令行运行Chronocat登陆端，至此，Tsugu已经可以使用。**
<h2 align="center"> 使用Onebot </h2>

***


本项目含有Onebot登陆端(v11)   
经过测试可用。
**使用Onebot ：[gocqhttp](https://docs.go-cqhttp.org) + [qsign](https://github.com/fuqiuluo/unidbg-fetch-qsign)**

*默认Onebot对接gocq端使用string，如果您使用array请自行提取raw_message字段*

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



<h2 align="center"> 接入自己的python程序/bot </h2>

***

使用`tsuguLP.py`接入您的同步代码，接入方法参考登陆端的`c_p_3`或`menu`即可。

`tsuguLP.py`位于登陆端文件夹，两登陆端的`tsuguLP.py`文件是一样的，


> zhaomaoniu(2023 9.16 20:16): 现在我可以跑同步代码了 😋 不维护 aiohttp 的菇 了

~~实际上转换成异步也是简单的~~


<h2 align="center"> 自建后端(非必需步骤) </h2>

***

tsugu的仓库：https://github.com/Yamamoto-2/tsugu-bangdream-bot

   

***小提示：建议安装pm2定时任务插件，控制日志内存占用。***



