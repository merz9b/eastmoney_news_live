# -*- coding: utf-8 -*-
'''
File: regex_tool.py
Project: utils
Created Date: Wednesday July 25th 2018
Author: Xin Zhang
'''

import datetime


def split_by_sign(string):
    first_location = string.find('】')
    return string[:first_location + 1], string[first_location + 1:]



def handle_content_list(ct_list):
    ct_l = []
    for ct in ct_list:
        ct_tmp = {}
        ct_tmp['newsid'] = ct['newsid']
        ct_tmp['title'] = ct['title']
        ct_tmp['news_type'] = ct['newstype']
        ct_tmp['m_type'] = ct['type']
        f_t, cont = split_by_sign(ct['digest'])
        ct_tmp['full_title'] = f_t
        ct_tmp['content'] = cont
        ct_tmp['ordertime'] = datetime.datetime.strptime(
            ct['ordertime'], '%Y-%m-%d %H:%M:%S').timestamp()
        ct_tmp['showtime'] = datetime.datetime.strptime(
            ct['showtime'], '%Y-%m-%d %H:%M:%S').timestamp()
        ct_l.append(ct_tmp)
    return ct_l


