#-*- coding:utf-8 -*-
__author__ = 'likun'



import os
import time
import inspect
import logging
import traceback
import win32gui

import rrtdb.normal as rrtdb
import rrtnet
import rrtcfg


class Monitor():


    def __init__(self):
        self.logger = self._getLogger()
        self.isAlive = True


    def _getLogger(self):
        logger = logging.getLogger('[Monitor]')
        this_file = inspect.getfile(inspect.currentframe())
        dirpath = os.path.abspath(os.path.dirname(this_file))
        handler = logging.FileHandler(os.path.join(dirpath, "monitor.log"))
        formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        return logger


    def start(self):
        #####################################
        self.logger.error("monitor is starting....")
        try:
            # 检查网络
            while True:
                if rrtnet.ping():
                    self.logger.error("ping back.")
                    break
                else:
                    self.logger.error('ping time out.')
                    time.sleep(30)
                    continue
            # 获取数据库配置信息
            config = rrtnet.config()
            self.logger.error('loading config...')
            # 获取最后访问时间
            arch = rrtnet.archive()
            self.logger.error('loading archive...')
            # 初始化数据库
            rrtdb.init(config)
            self.logger.error('init db')
            rrtdb.setArchive(arch)
            # 开始
            while self.isAlive:
                rows = rrtdb.query()
                if len(rows) == 0:
                    time.sleep(30); continue
                for row in rows:
                    while True:
                        rst = rrtnet.send(row)
                        if rst==False: time.sleep(10); self.logger.error('net work error, waitting 10s')
                        else: break
                    if str(rst)<>'null': rrtdb.setLastTime(rst)
                    time.sleep(2)
                del rows
        except:
            errinfo = traceback.format_exc()
            self.logger.error(errinfo)


    def stop(self):
        self.isAlive = False


if __name__=='__main__':
	mntr = Monitor()
	mntr.start()