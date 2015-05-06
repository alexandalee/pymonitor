#coding=utf8
__author__ = 'likun'

import rrtdb
import rrtnet
import rrtcfg

import os
import sys
import time
import json
import inspect
import logging
import traceback

logger = None


def getLogger():
        logger = logging.getLogger('[RrtMonitor]')
        this_file = inspect.getfile(inspect.currentframe())
        dirpath = os.path.abspath(os.path.dirname(this_file))
        handler = logging.FileHandler(os.path.join(dirpath, "service.log"))
        formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        return logger


def runit():

    global logger
    isAlive = True
    lasttime = None

    logger.error("service is starting....")
    try:
        if rrtnet.ping():
            logger.error("ping back.")
        else:
            logger.error('ping time out.')

        # 获取数据库配置信息
        config = rrtnet.config()
        logger.error('load config.')
        # 获取最后访问时间
        arch = rrtnet.archive()
        logger.error('load archive: %s' % arch)
        # 初始化数据库
        rrtdb.init(config)
        # 开始
        while isAlive:
            # 数据库
            rows = rrtdb.query(lasttime)
            for row in rows:
                rst = rrtnet.send(row)
                if rst: lasttime = rst
            logger.error("I am alive.")
            time.sleep(300)
    except:
        err = traceback.format_exc()
        logger.error(err)


def tlog():
    loger = getLogger()
    loger.warning('warnnig...')
    loger.error('error...')


if __name__ == '__main__':
    print ("service is starting....")

    try:
        if rrtnet.ping():
            print ("ping back.")
        else:
            print ('ping time out.')
            sys.exit()
        # 获取数据库配置信息
        config = rrtnet.config()
        # print config
        print ('load config.')

        # 获取最后访问时间
        arch = rrtnet.archive()
        print 'archive got', arch

        # 初始化数据库
        rrtdb.init(config)
        print 'db init'
        rrtdb.setArchive(arch)



        # 开始
        while 1:
            # 数据库
            rows = rrtdb.query()

            print len(rows)
            if len(rows) == 0:
                print 'sleep 30'
                time.sleep(30)
                continue

            for row in rows:
                rst = rrtnet.send(row)
                print rst, row['flownum']
                if rst:rrtdb.setLastTime(rst)
                time.sleep(2)

            del rows
            print 'sleeping 10'
            time.sleep(10)
        print 'done!'
    except:
        err = traceback.format_exc()
        print err

