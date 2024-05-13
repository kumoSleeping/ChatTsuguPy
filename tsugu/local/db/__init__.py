import os
import sys
import sqlite3
from loguru import logger
import json
import random
import urllib3
import re

from ...utils import config
from ...utils import text_response, server_exists, ns_2_is, n_2_i, i_2_n, is_2_ns
import tsugu_api


class DatabaseManager:
    def __init__(self, path):
        self.path = path
        self.conn = None
        self.cursor = None
        self.init_db(self.path)

    def init_db(self, path):
        if path:
            self.conn = sqlite3.connect(path, check_same_thread=False)
            logger.success(f'数据库连接成功，路径: {path}')
            self.cursor = self.conn.cursor()
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT UNIQUE,
                    platform TEXT,
                    server_mode INTEGER,
                    default_server TEXT,
                    car INTEGER,
                    game_ids TEXT,
                    verify_code TEXT
                )
            ''')
            self.conn.commit()
        else:
            # 如果不使用数据库，设置连接为 None
            self.conn = None
            # logger.info('不使用数据库')

    def close_db(self):
        if self.conn:
            self.conn.close()

    def execute_query(self, query):
        if self.cursor:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        else:
            return []


db_manager = DatabaseManager(config._user_database_path)


def database(path: str = None):
    '''
    启用本地用户数据库，同时不再使用远程数据库
    本地数据库不存在时自动创建
    :param path: 数据库文件路径
    :return:
    '''
    if not path:
        path = (os.path.dirname(sys.modules['__main__'].__file__))
    config._user_database_path = path
    db_manager.init_db(path)


def get_user_data(platform: str, user_id: str):

    cursor = db_manager.conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ? AND platform = ?", (user_id, platform))
    row = cursor.fetchone()

    if row:
        data = {
            "user_id": row[1],
            "platform": row[2],
            "server_mode": row[3],
            "default_server": list(json.loads(row[4])),
            "car": row[5],
            "game_ids": row[6],
            "verify_code": row[7]
        }
    else:
        data = {
            "user_id": user_id,
            "platform": platform,
            "server_mode": 3,
            "default_server": [3, 0],
            "car": 1,
            "game_ids": json.dumps([]),
            "verify_code": ""
        }
        cursor.execute('''
        INSERT INTO users (user_id, platform, server_mode, default_server, car, game_ids)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, platform, 3, json.dumps([3, 0]), 1, json.dumps([])))
        db_manager.conn.commit()
    result = {
        "status": "success",
        "data": data
    }
    return result