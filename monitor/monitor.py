#-*- coding:utf-8 -*-
__author__ = 'likun'


import os
import sys
import time
import inspect
import logging
import traceback

import rrtdb.normal as rrtdb
import rrtnet
import rrtcfg


class Monitor():


    def __init__(self):
        self.config = None
        self.isAlive = True
        self.logger = self._getLogger()


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
            self.config = rrtnet.config()
            self.logger.error('loading config...')

            # 处理特殊任务
            self.procTask()

            # 处理常规提交
            self.procNormal()
        except:
            errinfo = traceback.format_exc()
            print errinfo
            self.logger.error(errinfo)


    def procTask(self):
        """
        处理特殊命令
        """
        cmmd = rrtnet.task()
        self.logger.error('loading task...')

        if not cmmd:
            print 'no task'
            self.logger.error('no task.')
        else:
            # 初始化数据库
            rrtdb.init(self.config)
            rrtdb.setLastTime(cmmd['start'])
            while(True):
                # 一次取100条数据
                rows = rrtdb.query(cmmd['end'])
                #print 'get %d rows'% len(rows)
                if len(rows) <= 0: break
                for row in rows:
                    rst = rrtnet.send(row, False)
                    #print rst
                    ltt = row['opttime'].strip('000')
                    if str(rst)<>'null': rrtdb.setLastTime(ltt)
                    time.sleep(0.2)
                # 更新任务时间
                fresh = { 'id':cmmd['id'], 'now':ltt }
                rrtnet.taskover(fresh)
                del rows
        return True


    def procNormal(self):
        """
        正常处理
        """
        # 初始化数据库
        rrtdb.init(self.config)
        self.logger.error('init db')
        # 获取最后访问时间
        arch = rrtnet.archive()
        self.logger.error('loading archive...')
        rrtdb.setArchive(arch)
        # 开始
        while self.isAlive:
            self.logger.error('pid: %s :: loop...'%(str(os.getpid())))
            rows = rrtdb.query()
            print 'get %d rows'% len(rows),
            print time.strftime('%H:%M:%S')
            if len(rows) == 0:
                time.sleep(30); continue
            for row in rows:
                rst = rrtnet.send(row)
                ltt = row['opttime'].strip('000')
                if str(rst)<>'null': rrtdb.setLastTime(ltt)
                time.sleep(0.2)
            del rows
        return True


    def stop(self):
        self.isAlive = False


if __name__=='__main__':
	mntr = Monitor()
	mntr.start()