
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


## 📖 使用

### handler & handler_raw

- `handler` 是一个同步方法，用于直接处理用户输入的自然语言并返回查询结果:   
- 如果你方便使用 base64，`handler_raw` 方法或许会更好，`tsugu` 后端本身返回此数据结构，这个方法可以节省不必要的开销。
```python
import tsugu

# 四个参数，分别意味着 消息内容 用户id 平台 频道id
for i in tsugu.handler(message='查卡 ars 1x', user_id='1528593481', platform='red', channel_id='666808414'):
    print('文本: ',i) if isinstance(i, str) else None
    print(f"[图片]") if isinstance(i, bytes) else None

for i in tsugu.handler_raw(message='查卡 ars 1x', user_id='1528593481', platform='red', channel_id='666808414'):
    print('文本: ',i) if i['type'] == 'text' else None
    print(f"[图片]") if i['type'] == 'base64' else None
```


> 在常用的qqbot中，群号就是 `channel_id`。   
> 当你使用QQ号作为 `user_id` 时，`platform` 可以填写 `red`。   

## 📚 异步支持


### handler_async & handler_raw_async

- `handler_async` 是 `handler` 的异步版本，使用方法与 `handler` 相同。
- `handler_raw_async` 同理。


## 🧵多线程支持

- tsugu 在导入时完成了 `Alconna` 的初始化，避免了多线程 `context` 错误，因此可以在多线程中使用 `tsugu`。


## ⚙️ api settings

> 安装 `tsugu` 后可以直接导入 `tsugu_api_core` 的 `settings` 修改配置项。


```py 
from tsugu_api_core import settings

...
```

[tsugu_api settings 详细内容](https://github.com/WindowsSov8forUs/tsugu-api-python/blob/main/tsugu_api_core/settings.py)


---