
<h1 align="center"> tsugu-bangdream-bot-lite-py </h1>


<div align="center"> <img src="./logo.jpg" width="120"/> </div>
<div align="center">v0.4.0</div>
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

### 1.配置Chronocat登录到“聊天平台”

请前往 [Chronocat](https://chronocat.vercel.app/) 官网下载 LiteLoaderQQNT 版本的 Chronocat

### 2.下载并配置 tsuguLP_amd64_windows.exe
> 目前只打包了 Windows 的 amd64 版本，不满足条件请跳到 [环境需求](https://github.com/kumoSleeping/tsugu-bangdream-bot-lite-py#-%E7%8E%AF%E5%A2%83%E9%9C%80%E6%B1%82-)

在本项目的 release 中获取 tsuguLP_amd64_windows.exe 的最新版本后，双击运行，根据提示填写 config.yml

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
**使用Onebot ：[gocqhttp](https://docs.go-cqhttp.org) + [qsign](https://github.com/fuqiuluo/unidbg-fetch-qsign)**

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



