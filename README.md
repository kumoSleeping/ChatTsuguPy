
<h1 align="center"> tsugu-bangdream-bot-lite-py </h1>


<div align="center"> <img src="./logo.jpg" width="120"/> </div>
<div align="center">v1.0.0</div>
<div align="center">  Python编写的Tsugu前端、登陆端脚本 基于<a href="https://github.com/Yamamoto-2/tsugu-bangdream-bot">tsugu-bangdream-bot</a>后端
</div>

</div>

***

<h2 align="center"> TsuguLitePython好处都有啥？ </h2>
<div align="center"> 谁说对了就给他（ </div>


<details>
<summary><b>1.用户优先性</b></summary>
 
群聊开关，即开即关   
`swc off <name>` `swc on <name>`   
无空格指令触发，方便用户   
`查卡947` `查活动ppp 红`    
cn / jp / en 指定服务器，无需使用 `主服务器` 命令   
`ycx20 jp` `玩家状态 en`   
统一的远程玩家状态绑定数据库，绑定方便，一次绑定多bot共享     
`绑定玩家 xxxx jp`  

</details>


 <details>
<summary><b>2.维护轻松</b></summary>
 
部署/更新 方便。小版本更新只需替换`./tsuguLP.py`
大版本更新按需求替换文件 / 配置即可。 

</details>
 


 <details>
<summary><b>3.扩展简单</b></summary>
 
核心文件只有tsuguLP.py且为同步代码，可以轻松编写内容扩展，接入自己的PythonBot，如[Nonebot](https://github.com/nonebot/nonebot2).  

导入后直接 `rpl: list = tsugu_main(mm, user_id, group_id)`，然后解析`rpl`即可。接入方法参考登陆端的`c_p_3`或`menu`即可。   


</details>
 
 <details>
<summary><b>4.客服Ano酱在线指导安装（</b></summary>
 
[BanGDreamBot开发聊天群](https://qm.qq.com/q/zjUPQkrdpm) 过于温馨的聊天环境～   
装不上自罚演奏春日影，包您安装成功～   

</details>



**未来还会继续完善以及同步更新的，感谢大家的支持！**   

<h2 align="center"> 最简方案 </h2>

# 注意 ⚠️！！！Chronocat项目已结束，请使用Onebot + python运行此项目！
或点击上面的4.客服Ano酱在线指导安装（查看解决方法

### 2.下载并配置 tsuguLP_amd64_windows.exe
> 目前只打包了 Windows 的 amd64 版本，不满足条件请跳到 [环境需求](https://github.com/kumoSleeping/tsugu-bangdream-bot-lite-py#-%E7%8E%AF%E5%A2%83%E9%9C%80%E6%B1%82-)

在本项目的 [release](https://github.com/kumoSleeping/tsugu-bangdream-bot-lite-py/releases) 中获取 tsuguLP_amd64_windows.exe 的最新版本后，双击运行，根据提示填写 config.yml

一般来说，你只需要修改 `token` 的值，使其与 [Chronocat 的配置文件](https://chronocat.vercel.app/config/#%E4%BD%8D%E7%BD%AE)中的 `token` 一致即可

不出意外的话，当你第二次打开 tsuguLP_amd64_windows.exe 时，屏幕上会出现 `猫猫，启动！`

结论：你已经成功配置并运行了 tsuguLP

<h2 align="center"> 环境需求 </h2>


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

### 1.配置Chronocat登录到“聊天平台”

请前往[Chronocat](https://chronocat.vercel.app/)官网下载LiteLoaderQQNT版本的Chronocat


**请确保已按照Chronocat官网要求完成安装。**



### 2.填入 TOKEN 到 catbot3.py  


下载zip / git clone 后

右键以编辑形式打开 Chronocat登陆端/c_p_3.py，你会在开头看到
```py
# 用于设置red实例基础信息
class Msg:
    IP = 'localhost'
    PORT = '16530'
    TOKEN = "your_token"
```
你需要将 TOKEN 的内容填入your_token   
  
**TOKEN获取(0.0.46版本以后):**   

浏览 https://chronocat.vercel.app/config/    

 <details>
<summary><b>0.0.45及以前版本（目前0.0.46版本以后也可以用）</b></summary>
     
使用Chronocat无需配置，token 被默认存储在 `%AppData%/BetterUniverse/QQNT/RED_PROTOCOL_TOKEN` 或 `~/BetterUniverse/QQNT/RED_PROTOCOL_TOKEN` 中， 首次启动 Chronocat 时会自动生成，并保持不变。

*Windows用户打开文件管理器，在地址栏输入`%AppData%`即可跳转*

未来几个版本，如果是新安装的用户，RED_PROTOCOL_TOKEN文件仍然会生成，并保持和chronocat.yml里token一致，这样先前做了自动获取token逻辑的框架仍然能正常工作，不会因为用户安装的是0.0.46就找不到token了。
但不建议再使用这个文件。新框架从0.0.46起建议让用户在chronocat.yml里获取token。

</details>


### 3.运行 catbot3.py  
推荐命令行运行   
```shell
cd 目标文件夹
python catbot3.py
# python3 catbot3
```
命令行会出现**提示**

***请认真阅读！***


**再次命令行运行 catbot3.py ，至此，Tsugu已经可以使用。**



<h2 align="center"> 使用Onebot </h2>

***


本项目含有Onebot登陆端(v11)   
经过测试可用。
**使用go-cqhttp ：[gocqhttp](https://docs.go-cqhttp.org) + [qsign](https://github.com/fuqiuluo/unidbg-fetch-qsign)**

*默认Onebot对接gocq端使用string，如果您使用array请自行提取raw_message字段*

***默认 Onebot 文件夹内不存在`tsuguLP.py`，麻烦您动动小手把文件搬到 Onebot 文件夹内（）***
 <details>
<summary><b>使用gocqhttp需要选择http协议，配置：</b></summary>
 

```yml
# 连接服务列表
servers:
  - http: # HTTP 通信设置
      address: 0.0.0.0:5700 # HTTP(flask)监听地址
      version: 11     # OneBot协议版本, 支持 11/12
      timeout: 600      # 反向 HTTP 超时时间, 单位秒，<5 时将被忽略 这个建议大于5分钟，有时候后端出图很慢
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

</details>


*然后不出意外的运行就行了*  

**使用shamrock ：[shamrock](https://whitechi73.github.io/OpenShamrock/)**
 <details>
<summary><b>使用shamrock需要注意的地方</b></summary>

shamrock：状态-接口信息-主动HTTP端口 需要与main.py中的HTTP_PORT相同，默认为5700

shamrock：状态-接口信息-回调HTTP地址设置为
```
http://{tsugu_IP}:{FLASK_PORT}/
```
其中tsugu_IP为tsugu运行在的IP，如果在本机环境一般为127.0.0.1，局域网环境可以参考tsugu的启动输出，其它情况请参考下方说明。
FLASK_PORT默认为5701

main.py中的 SEND_IP 需要改为shamrock所运行在的IP。

如果您使用手机或模拟器运行shamrock，使用服务器运行tsugu，则可能需要使用frp将shamrock的主动HTTP端口穿透到公网。
[frp 项目地址](https://github.com/fatedier/frp) 
[frp Mobile 项目地址](https://github.com/HaidyCao/frp)

*参考配置*

服务器端的frps.ini

```ini
[common]
bind_port = 您的frp service的运行端口 默认为7000
token = 您的frp server token
```

shamrock端的frpc.ini：

```ini

[common]
server_addr = 您的服务器地址
server_port = 您的frp service的运行端口 默认为7000
token = 您的frp server token

[web]
type = http
local_ip = 127.0.0.1
local_port = 5701
remote_port = 5701
```

frp搭建完成后，将main.py中的 SEND_IP 改为frpc运行在的IP。

最后，打开shamrock 状态-功能设置-HTTP回调，并完全重启QQ即可。


</details>



使用 Onebot 默认您具有一定的基础，当然如果您没有基础也欢迎来我们小群咨询～



<h2 align="center"> 接入自己的python程序/bot </h2>

***

使用`tsuguLP.py`接入您的同步代码，接入方法参考登陆端的`c_p_3`或`menu`即可。

`tsuguLP.py`位于登陆端文件夹，两登陆端的`tsuguLP.py`文件是一样的，


> zhaomaoniu(2023 9.16 20:16): 现在我可以跑同步代码了 😋 不维护 aiohttp 的菇 了

~~实际上转换成异步也是简单的~~


<h2 align="center"> 自建后端(非必需步骤) </h2>

***

tsugu的仓库：https://github.com/Yamamoto-2/tsugu-bangdream-bot

看专栏，有教程（
   

***小提示：建议安装pm2定时任务插件，控制日志内存占用。***





# 下面全是大饼


<h1 align="center"> tsugu-bangdream-bot-lite-py </h1>




<div align="center"> <img src="./logo.jpg" width="120"/> </div>


<div align="center">v2.0.0 ------------</div>



<div align="center">  Py编写的Tsugu前端、登陆端脚本 基于<a href="https://github.com/Yamamoto-2/tsugu-bangdream-bot">Tsugu</a>后端
</div>


</div>

***

<h2 align="center"> 广泛的适用性 </h2>


### Satori
> 经过时间考验，面向未来的成熟协议

Satori作为 koishi 的协议层，已经支持20余个主流聊天平台，拥有极强的跨平台性。

[Chronocat](https://chronocat.vercel.app/)   
[Satori.js](https://satori.js.org/zh-CN/)   
[Koishi](https://koishi.chat/zh-CN/)   
...

### Onebot_v11（cqcode）
> 截止2023年最广泛的生态，历史的见证

[Shamrock](https://github.com/linxinrao/Shamrock)   
[go-cqhttp](https://docs.go-cqhttp.org/)   
[Mirai](https://github.com/mamoe/mirai)   
...

### Red-Protocol
> 某聊天软件下产生的畸形协议

[Chronocat](https://chronocat.vercel.app/)

### Http 服务
> 使用 `Http Post` 跨编程语言接入Tsugu

例如您有自己编写的 Bot，可以使用 Http Post 服务让您的Bot在五分钟之内对接 Tsugu。


### Web 服务
> 让您在浏览器中使用Tsugu

可用于啥我也不知道（
### Console 服务
> 让您在控制台中使用Tsugu

可用于测试


***


<h2 align="center"> 应该选择什么服务 </h2>



如果你指的是对接某T字开头公司Q字开头平台，可以选择 **Red-Protocol** 服务。
然后对接[Chronocat](https://chronocat.vercel.app/)。
```
并前往请前往Chronocat官网
下载LiteLoaderQQNT版本的Chronocat
然后确保已按照Chronocat官网要求完成安装并启动

生成的Config文件夹里有使用各个服务的配置教程，请仔细阅读。
```
</details>
 
 <details>
<summary><b>可以来这个平台的群里找客服Ano酱在线指导（</b></summary>

**注意，如果没有相关bot疑问或者学习目的，请不要随意加群**    
**注意，如果你不知道什么是BanGDream，也请不要随意加群**    
**注意，本群还是欢迎加群的（**    
[BanGDreamBot开发聊天群](https://qm.qq.com/q/zjUPQkrdpm)   
温馨的聊天环境～   


</details>

***


<h2 align="center"> 使用 .exe 文件开始 </h2>





**下载并配置 tsuguLP_amd64_windows.exe**
>   注意：使用exe运行就不需要使用Python运行了。
> 
> 目前只打包了 Windows 的 amd64 版本，不满足条件请跳到使用 Python 运行此项目。

在本项目的 [release](https://github.com/kumoSleeping/tsugu-bangdream-bot-lite-py/releases) 中获取 tsuguLP_amd64_windows.exe 的最新版本后，双击运行，然后选择你**需要使用的服务**。

此时会生成 config.yml 以及 Config 文件夹。  

> config.yml 决定启动哪种服务。  
> 服务各自的配置在 Config 文件夹里。  

**Config文件夹里有使用各个服务的配置教程，请仔细阅读。**   



***



<h2 align="center"> 开始 Python 开始 </h2>


> 推荐Python3.10 - 3.12
> ~~安装时记得勾选添加到环境变量PATH~~
```shell
# 检测是否安装pip
pip -v

# 安装所需外部库
pip install pillow requests websockets aiohttp flask pydantic

# 如果缺少内部库pip install即可

# 可能需要尝试检查环境变量或使用pip3
python server.py
# 可能需要尝试检查环境变量或使用python3
```

此时会生成 config.yml 以及 Config 文件夹。  

> config.yml 决定启动哪种服务。  
> 服务各自的配置在 Config 文件夹里。  

**Config文件夹里有使用各个服务的配置教程，请仔细阅读。**   

***

<h2 align="center"> [开发] 利用 Http 服务跨语言 / 框架接入自己的Bot </h2>


本项目提供了 Http 服务，您只需要每次把Bot收到的 `消息内容` `用户ID` `群组ID`  Http Post 到本程序，就会得到相应的返回json，您只需要解析即可。

如果您使用Python，可以直接将 `Tsugu` 文件夹作为您项目插件的一部分，导入之后，依旧只需要传入每条消息的 `消息内容` `用户ID` `群组ID` 即可得到相应的返回json，您只需要解析即可。    
提示：如果您的代码是异步还需要自己适配。



***



<h2 align="center"> 须知 </h2>


本项目功能与官方Tsugu使用上略有不同
 
 
1.无空格指令触发   
`查卡947` `查活动ppp 红`    

2.查询时可以使用 cn / jp / en 指定服务器   
`ycx20 jp` `玩家状态 en`   

3.用户服务器顺序，车牌转发等配置会被本地保留。   
玩家状态绑定会被长期远程保留。

4.提供群聊开关，即开即关   
`swc off <name>` `swc on <name>`  

此项目已得到Tsugu开发者认可（



