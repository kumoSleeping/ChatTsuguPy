
# Tsugu Backend Docs

## 1). 简介

Tsugu 后端是一个 Nodejs 搭建的 express 服务器，用于提供数据服务。
前端使用 POST 请求发送数据，后端返回 JSON 数据。 


## 2). 默认 API

默认 API 用于获取 Tsugu 最主要的出图 / 回复。   
默认V1 API 由于历史原因，有的参数切片由前端完成，请求参数较为混沌，已无二次使用价值，故不在此赘述。

Koishi 插件 tsugu-bangdeam-bot 使用默认 API，具体请求方式参阅源码。

## 3). V2 API

V2 API 用于获取 Tsugu 最主要的出图 / 回复。   

### 请求

V2 的特点是请求数据相同，参数切片由后端完成，前端只需原样传送用户输入的参数即可。


```json
data = {
    "default_servers": default_servers, // list
    "server": server, // int 0-4
    "text": text, // string 用户消息但去除命令头
    "useEasyBG": useEasyBG, // bool
    "compress": compress // bool
}
```

**V2 API 列表 (Path: /v2/...)**
- /v2/ycm
- /v2/card
- /v2/cardIllustration
- /v2/gacha
- /v2/gachaSimulate
- /v2/event
- /v2/song
- /v2/songMeta
- /v2/player
- /v2/character
- /v2/chart
- /v2/ycx
- /v2/ycxAll
- /v2/lsycx

使用例

用户输入:


> 查卡 ksm 红

前端需要处理为:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"default_servers": [0, 3], "server": 0, "text": "ksm 红", "useEasyBG": true, "compress": true}' http://localhost:3000/v2/card
```
### 返回

```json
[{"type": "string", "string": string},
{"type": "base64", "string": string}, ... ]
```
当 type 为 string 时，string 为消息内容，可以直接发送到客户端。   
当 type 为 base64 时，string 为图片的 base64 编码，需要解码后发送到客户端。   
可能会返回多个结果。  

## 4). user API

user API 用于用户数据获取与存储，需要后端启用数据库。

### 1.创建/获取用户数据。

#### 请求

- /user/getUserData

```json
{
    "platform": "red",
    "user_id": "1234567890"
}
```


#### 返回

```json
{'status': 'success', 'data': {'_id': 'yuanshen:114514', 'user_id': '114514', 'platform': 'yuanshen', 'server_mode': 3, 'default_server': [3, 0], 'car': True, 'server_list': [{'playerId': 0, 'bindingStatus': 0}, {'playerId': 0, 'bindingStatus': 0}, {'playerId': 0, 'bindingStatus': 0}, {'playerId': 0, 'bindingStatus': 0}, {'playerId': 0, 'bindingStatus': 0}]}}
```

### 2.修改用户配置数据(服务器列表, 车牌转发, 主服务器)

此 api 用于修改用户数据。

#### (2.1)通过传递 update 字段修改用户数据

##### 请求

- /user/changeUserData

```json
{
    "platform": "red",
    "user_id": "1234567890",
    "update": {  // 通常只传一个字段
        "server_mode": 3,
        "car": false,
        "default_server": [3, 0]
    }
}
```


tsugu-bangdream-bot 使用此 api，但推荐使用下方细分的 api。

#### (2.2) 修改用户主服务器设置

##### 请求

- /user/changeUserData/setServerMode


```json
{
    "platform": "red",
    "user_id": "1234567890",
    "text": "国服"
}
```

#### (2.3) 修改用户车牌转发设置

##### 请求

- /user/changeUserData/setCarForwarding

```json
{
    "platform": "red",
    "user_id": "1234567890",
    "status": true
}
```

#### (2.4) 修改用户默认服务器设置

##### 请求

- /user/changeUserData/setDefaultServer

此 api 用于修改用户数据中的 default_server 字段。

```json
{
    "platform": "red",
    "user_id": "1234567890",
    "text": "国服 日服"
}
```

### 3.绑定/解绑玩家数据

#### 请求

- bindPlayerRequest

```json
{
    "platform": "red",
    "user_id": "1234567890",
    "server": 3,
    "bindType": true,  //true为绑定，false为解绑
    "playerId": 123456
}
```

### 4.验证绑定/解绑玩家数据

#### 请求

- bindPlayerVerification

```json
{
    "platform": "red",
    "user_id": "1234567890",
    "server": 3,
    "bindType": true,  //true为绑定，false为解绑
    "playerId": 123456
}
```

## station API

主要用于自建车站，需要后端启用数据库。



## eventReport 与 eventPreview 专栏生成 API

用于 Bilibili Tsugu_Official 专栏生成，需要 `process.env.ARTICLE` 为 `true`。

## utils API

用于一些工具。

### 1.根据服务器文字获取服务器ID

#### 请求

- /utils/getServerIdByText

```json
{
    "text": "国服"
}
```