#!/bin/python
# -*- coding:utf-8 -*-
__author__ = 'likun'

import sys
import pymssql
import rrtcfg
import json


tplSQL = ''
archive = {}
queryRows = []
sqlCursor = None


def init(cfg):
    # 初始化数据库连接等信息
    global  tplSQL, sqlCursor

    cfgs = json.loads(cfg)
    tplSQL = cfgs[u'sqltpl'] #.encode("ascii")
    # print tplSQL
    sqlConn = pymssql.connect(host=rrtcfg.db['host'], user=rrtcfg.db['user'], as_dict=True, \
                         password=rrtcfg.db['password'], database=rrtcfg.db['dbname'])
    sqlCursor = sqlConn.cursor()


def setLastTime(lasttime):
    # 设置最后更新时间
    global archive
    archive['lasttime'] = lasttime


def getLastTime():
    # get last tiem
    global archive
    return archive['lasttime']


def getArchiveId():
    # get last tiem
    global archive
    return archive['id']


def setArchive(arch):
    # 设置archive的某一选项
    global archive
    archive['id'] = arch[u'id']
    archive['lasttime'] = arch[u'opttime']


def query():
    # 数据库查询   todo
    global sqlCursor
    fetchedRows = []
    sqlCursor.execute(tplSQL % getLastTime())
    row = sqlCursor.fetchone()
    while row:
        fetchedRows.append(formatRow(row))
        row = sqlCursor.fetchone()
    return fetchedRows


def formatRow(row):
    # 把row格式化为 {}
    global archiveid
    ftrow = {}
    ftrow['amount'] = str(row[u'amount'])
    ftrow['opttime'] = str(row[u'opttime'])
    ftrow['cashtype'] = str(row[u'cashtype'])
    ftrow['archiveid'] = str(getArchiveId())
    ftrow['flownum'] = str(row[u'flownum'])+str(row[u'flowid'])+str(row[u'man'])
    return  ftrow


def done():
    # 数据库操作完成
    global sqlserverConn
    sqlserverConn.close()



########################################################################################################
# sql server pay list sql
########################################################################################################
# SELECT flow_no as flownum, pay_amount*coin_rate as amount, coin_no as cashtype, oper_date as opttime,
# flow_id as flowid, oper_id as man,
# from pos_t_payflow
# WHERE sell_way<>'D' and oper_date > '%s'
# ORDER BY oper_date
########################################################################################################