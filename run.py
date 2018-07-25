# -*- coding: utf-8 -*-
'''
File: run.py
Project: em_news_live
Created Date: Tuesday July 24th 2018
Author: Xin Zhang
'''

import json
import requests
import datetime
import time
from em_news_live.utils.regex_tool import handle_content_list
from em_news_live.utils.db_tool import DB_FOLD,SqliteDb

def print_content(cont):
    print('\n')
    print(
        '<%s> %s:\n' %
        (datetime.datetime.fromtimestamp(cont['showtime']).strftime('%Y-%m-%d %H:%M:%S'),
         cont['full_title']))
    print(cont['content'])
    print('\n')


def fetch_news():
    res = requests.get('http://newsapi.eastmoney.com/kuaixun/v1/getlist_102_ajaxResult_50_1_.html?r=0.02990722472765195&_=1532423736326')
    cont = json.loads(res.text.lstrip('var ajaxResult='))['LivesList'][::-1]
    msg = handle_content_list(cont)
    return msg


def main():
    sdb = SqliteDb('em_news', DB_FOLD)
    sdb.init_db()
    sdb.update_news_id_list()
    while  True:
        msg = fetch_news()
        ins_msg = [m for m in msg if m['newsid'] not in sdb.news_id_list]
        sdb.insert(ins_msg)
        sdb.update_news_id_list()
        for c in ins_msg:
            print_content(c)
        time.sleep(30)

if __name__ == '__main__':
    main()