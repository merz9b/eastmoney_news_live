# -*- coding: utf-8 -*-
'''
File: db_tool.py
Project: utils
Created Date: Wednesday July 25th 2018
Author: Xin Zhang
'''

import os
import sqlite3 as sl3

CURRENT_FILE_PATH = os.path.dirname(__file__)
DB_FOLD = os.path.join(os.path.dirname(CURRENT_FILE_PATH), 'data')

def cast_news_dict_to_tuple(d):
    return (d['newsid'],
            int(d['ordertime']),
            int(d['showtime']),
            d['m_type'],
            d['news_type'],
            d['title'],
            d['full_title'],
            d['content'])



class SqliteDb:
    def __init__(self, db_name, fold_path):
        self._fold_path = fold_path
        full_db_name = '%s.db' % db_name
        self._path = os.path.join(fold_path, full_db_name)
        self._db_name = db_name
        self._conn = sl3.connect(self._path)
        self.is_inited = False
        self.news_id_list = None

    def init_db(self):
        with self._conn:
            self._conn.execute(
                '''CREATE TABLE IF NOT EXISTS em_news_live(
                    newsid TEXT PRIMARY KEY NOT NULL,
                    ordertime INTEGER,
                    showtime INTEGER,
                    m_type INTEGER,
                    news_type INTEGER,
                    title  TEXT,
                    full_title TEXT,
                    content TEXT
                    )''')
            self._conn.execute('PRAGMA synchronous = OFF')
        self.is_inited = True

    def insert_data(self, data: list):
        with self._conn:
            self._conn.executemany(
                'INSERT INTO em_news_live VALUES (?,?,?,?,?,?,?,?)', data)

    def update_news_id_list(self):
        with self._conn:
            res = self._conn.execute(
                '''select newsid from em_news_live''').fetchall()
            self.news_id_list = [s[0] for s in res]

    def insert(self, data):
        if data:
            ins_list = [cast_news_dict_to_tuple(d) for d in data]
            self.insert_data(ins_list)