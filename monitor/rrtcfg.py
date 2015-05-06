#!/bin/python
# -*- coding: utf-8 -*-
__author__ = 'likun'

import ConfigParser


# 错误信息
ERRORS = []
# 开发模式
mode = 'dev'
# parse
cfgr = None
# 数据库配置
db = {}
# 人人投项目设置
product = {}
# 财务系统配置
finance = {}


def init():
    global db, product, finance, cfgr

    # 读取文件
    cfgr = ConfigParser.ConfigParser()
    cfgd = file('config.ini')
    cfgr.readfp(cfgd)
    cfgd.close()
    # db 初始化
    db = load('db')
    product = load('product')
    finance = load('finance')


def load(item):
    global cfgr

    dicts = {}
    cfgset = cfgr.items(item)
    for itm in cfgset:
        (key,val) = itm
        dicts[key]=val
    return dicts


init()

if __name__ == '__main__':
    print db
    print product
    print finance
