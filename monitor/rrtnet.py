#!/bin/python
# -*- coding: utf-8 -*-
__author__ = 'likun'

import time
import hashlib
import traceback
import rrtcfg
import simplejson as json


class RrtProtocol(object):
    """ 定义接口的通信协议 """

    data = {}
    ApiUrl = "/finance/"
    Passcode = "0x170484"
    ApiQuery = {'head': {}, 'body': {}}
    ServerUrl = 'http://api.dev2.renrentou.com'

    Request = {}
    #
    Response = {}

    def __init__(self, apiname):
        self.setQueryHeader()
        self.setRequestUrl(apiname)


    def setRequestUrl(self, apiname):
        """ 获取api请求地址 """
        self.ApiUrl = self.ServerUrl + self.ApiUrl + apiname


    def setQueryDataItem(self, value, name=None):
        """
        设置data内的kv数据
        :param name: string name
        :param value: value
        """
        if(name):
            self.data[name] = value
        else:
            self.data = value


    def setQueryHeader(self):
        """
        自动填充query.head 数据
        :return: none
        """
        cfg = rrtcfg.product
        fcfg = rrtcfg.finance
        self.ApiQuery['head']['userid'] = str(cfg['userid'])
        self.ApiQuery['head']['projectid'] = str(cfg['productid'])
        self.ApiQuery['head']['storeid'] = str(cfg['storeid'])
        self.ApiQuery['head']['posid'] = str(cfg['posid'])
        self.ApiQuery['head']['software'] = str(fcfg['software'])
        self.ApiQuery['head']['time'] = str(int(time.time()))
        v = self.ApiQuery['head']
        headStrig = v['projectid'] + v['storeid'] + v['posid'] + v['software'] + v['time'] + self.Passcode
        headStrig.encode('utf-8')
        self.ApiQuery['head']['sign'] = hashlib.md5(headStrig).hexdigest()


    def setQueryBody(self):
        """ 设置请求消息体 """
        self.ApiQuery['body']['data'] = json.dumps(self.data)
        bdstr = self.ApiQuery['body']['data']+self.Passcode
        #print bdstr
        self.ApiQuery['body']['sign'] = hashlib.md5(bdstr).hexdigest()


    def getRequestQuery(self):
        """
        返回整个query的json
        :return: json
        """
        self.setQueryBody()
        self.Request = json.dumps(self.ApiQuery)
        return self.Response


    def parseResponse(self, data):
        """
        将data解析为json格式的数据
        :param data: http response string
        :return: none
        """
        try:
            data.encode("UTF-8")
            self.Response = json.loads(data)
        except:
            print data



    def checkResponseCode(self):
        """
        检查返回状态信息
        :return: boolean
        """
        if self.Response['head']['code'] == u'200':
            return True
        if rrtcfg.mode == 'dev': print self.Response
        return False


    def getResponseData(self):
        """
        获取返回的参数，并且先做完整性验证
        :return: false|data
        """
        bdstr = self.Response['body']['data']+self.Passcode
        sign = hashlib.md5(bdstr).hexdigest()
        if sign <> self.Response['body']['sign']:
            if rrtcfg.mode == 'dev': print self.Response
            return 'null'
        return self.Response['body']['data']




import urllib2


def ping():
        """
        测试两端的连通性
        :return: boolean
        """
        try:
            api = RrtProtocol('ping')
            api.getRequestQuery()
            req = urllib2.Request(api.ApiUrl)
            fd = urllib2.urlopen(req, api.Request)
            info = fd.info()
            resp = fd.read(int(info['Content-Length']))
            fd.close()
            # 解析返回结果
            # print resp
            api.parseResponse(resp)
            data = api.getResponseData()
            # 判断状态
            if data == 'ok':
                return True
            return False
        except:
            print 'error happend：',
            print traceback.format_exc()
            return False


def archive():
        # 获取服务器上存储的最后更新时间
        try:
            api = RrtProtocol('archive')
            api.getRequestQuery()
            # print api.ApiUrl
            req = urllib2.Request(api.ApiUrl)
            fd = urllib2.urlopen(req, api.Request)
            info = fd.info()
            resp = fd.read(int(info['Content-Length']))
            fd.close()
            # 解析返回结果
            api.parseResponse(resp)
            data = json.loads(api.getResponseData())
            return data
        except:
            print traceback.format_exc()
            return False


def  config():
        # 获取服务器上的配置SQL
        try:
            api = RrtProtocol('config')
            api.getRequestQuery()
            # print api.ApiUrl
            req = urllib2.Request(api.ApiUrl)
            fd = urllib2.urlopen(req, api.Request)
            info = fd.info()
            resp = fd.read(int(info['Content-Length']))
            fd.close()
            # 解析返回结果
            # print resp
            api.parseResponse(resp)
            data = api.getResponseData()
            return data
        except:
            print traceback.format_exc()
            return False


def send(dat):
        # 发送数据人人投服务器
        try:
            api = RrtProtocol('send')
            api.setQueryDataItem(dat)
            api.getRequestQuery()
            api.setQueryDataItem(dat)
            req = urllib2.Request(api.ApiUrl)
            fd = urllib2.urlopen(req, api.Request)
            info = fd.info()
            resp = fd.read(int(info['Content-Length']))
            fd.close()
            # 解析返回结果
            api.parseResponse(resp)
            data = api.getResponseData()
            # 判断状态
            return data
        except:
            return False



if __name__ == '__main__':
    #if ping(): pass
    #print config()

    #
    name = 123
    dat = {'uuid':'1234-askdf-23ewr-asdfv', 'age':123, 'isone':True}
    print send(name, dat)
