#!/bin/python
# -*- coding:utf-8 -*-
__author__ = 'likun'

import sys
import pymssql
import rrtcfg
import simplejson as json


tplSQL = ''
archive = {}
queryRows = []
sysname = None
sqlCursor = None



def init(cfg):
    # 初始化数据库连接等信息
    global  tplSQL, sqlCursor, sysname

    cfgs = json.loads(cfg)
    dbname = cfgs[u'dbname']
    tplSQL = cfgs[u'sqltpl']
    sysname = cfgs[u'sysname']
    # print tplSQL
    sqlConn = pymssql.connect(host=rrtcfg.db['host'], user=rrtcfg.db['user'], as_dict=True, \
                              password=rrtcfg.db['password'], database=dbname)
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
    if archive.has_key('id'):
        return archive['id']
    return  0


def setArchive(arch):
    # 设置archive的某一选项
    global archive
    archive['id'] = arch[u'id']
    archive['lasttime'] = arch[u'opttime']


def query(endtime=None):
    # 数据库查询
    global sqlCursor, tplSQL
    fetchedRows = []
    start = getLastTime()
    if endtime:
        #print tplSQL % (start, endtime)
        sqlCursor.execute(tplSQL % (start, endtime))
    else:
        endtime = '2037-01-01'
        #print tplSQL % (start, endtime)
        sqlCursor.execute(tplSQL % (start, endtime))
    #读取数据
    while True:
        row = sqlCursor.fetchone()
        if row:
            frow = formatRow(row)
            fetchedRows.append(frow)
        else: break
    return fetchedRows


def formatRow(row):
    """
    格式化row
    :param row:
    :return:
    """
    global sysname

    ftrow = {}
    ftrow['sysname'] = sysname
    # 本笔金额
    ftrow['amount'] = str(row[u'amount'])
    # 最后操作时间
    ftrow['opttime'] = str(row[u'opttime'])
    # archive 表的id，方便取数据
    ftrow['archiveid'] = str(getArchiveId())
    # 从财务系统获取的原始数据
    ftrow['rawdata'] = json.dumps(transform(row))
    return ftrow


def transform(row):
    newrow = {}
    for key in row:
        try:
            nkey = str(key)
            newrow[nkey] = unicode(row[key])
        except:
            print key, row[key]
    return  newrow




def done():
    # 数据库操作完成
    global sqlserverConn
    sqlserverConn.close()



########################################################################################################
# 百威财务SQL
# 时间判断时，必须用 > 或 < 否则会出现无限重复最后的数据。
########################################################################################################
#   SELECT top 100
#   a.sheet_no,a.branch_no,a.cust_no,a.sale_man,a.oper_id,a.item_no,a.pos_qty,a.pos_amt,a.pos_ret_qty,a.pos_ret_amt,
#   a.pos_give_qty,a.so_qty,a.ri_qty,a.sale_price,a.real_price,a.so_amt,a.ri_amt,a.voucher_no,a.oper_date,a.pay_date,
#   a.other1,a.other2,a.other3,a.num1,a.num2,a.num3,a.unit_no,a.unit_factor,a.discount ,b.item_subno,b.item_barcode,b.item_base_price2,
#   b.item_base_price3,b.item_base_price4,b.item_base_price5,b.item_vip_price2,b.item_vip_price3,b.item_abc,b.item_valid_day,b.item_name,
#   b.item_subname,b.item_clsno,b.item_brand,b.item_brandname,b.item_unit_no,b.item_size,b.item_product_area,b.item_price,b.item_base_price,
#   b.item_sale_price,b.item_sup_no,b.item_vip_price,b.item_counter_code,b.item_other1,b.item_other2,b.item_other3,
#   a.oper_date as opttime, a.pos_amt as amount
#   FROM view_pfpos_detail_union  a , view_item_info  b
#   WHERE ( a.item_no = b.item_no ) And ( a.oper_date > '%s') And ( a.oper_date < '%s') And ( left(a.branch_no,2) in (select branch_no from fn_branch_area ('00'))) order by a.oper_date ,a.item_no
########################################################################################################