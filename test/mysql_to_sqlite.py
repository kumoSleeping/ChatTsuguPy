import sqlite3
import pymysql
import json


# 数据库连接配置
config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'xxxxxxxxx.',
    'db': 'koishi'
}

# 连接到数据库
conn_mysql = pymysql.connect(**config)


with conn_mysql.cursor() as cursor:
    # SQL 查询语句
    sql = "SELECT * FROM user"
    cursor.execute(sql)
    # 获取所有记录列表
    results = cursor.fetchall()

# 重新连接数据库
conn = sqlite3.connect('output.db')
c = conn.cursor()

# 创建表
c.execute('''CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT UNIQUE,
    platform TEXT,
    server_mode INTEGER,
    default_server TEXT,
    car INTEGER,
    game_ids TEXT,
    verify_code TEXT
)''')

for record in results:
    _, _, _, _, _, _, _, _, user_id, platform, server_mode, default_server, car, game_ids_json, _, _ = record

    # 如果game_ids_json为None，将其视为一个空的JSON字符串
    game_ids_json = game_ids_json if game_ids_json is not None else "[]"
    game_ids = json.loads(game_ids_json)

    # 构建新的game_ids列表，不包含bindingStatus，包含server信息
    game_ids = [{"game_id": str(game_id["gameID"]), "server": index} for index, game_id in enumerate(game_ids) if
                   game_id["gameID"] != 0]

    # 如果没有有效的游戏ID，则跳过这条记录
    if not game_ids:
        continue

    # 把类似 "3, 0" 换成 [3, 0]
    default_server = json.dumps([int(i) for i in default_server.replace(" ", "").split(",")])
    # 插入语句
    insert_stmt = '''INSERT INTO users (user_id, platform, server_mode, default_server, car, game_ids, verify_code) VALUES (?, ?, ?, ?, ?, ?, ?)'''
    c.execute(insert_stmt, (user_id, platform, server_mode, default_server, 1, json.dumps(game_ids), None))

# 提交事务并关闭连接
conn.commit()


conn.close()
conn_mysql.close()