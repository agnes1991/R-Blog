#!/usr/bin/env python
#coding:utf-8

import urllib
import urllib2
import requests
from cStringIO import StringIO
import gzip
import json
from multiprocessing import Process

bodyData={
  "sysInfo": {
    "id": "FF-CN-MS838A-I-UD00:30:1b:ba:02:db",
    "deviceType": "FF-CN-MS838A-I-UD",
    "Mac": "00:30:1b:ba:02:db",
    "sendTime": "1501835778126",
    "device_id": "000",
    "device_num": "123456",
    "userCenterId": "543079336",
    "userCenterName": "雷鸟用户",
    "userCenterphone": "13823257169",
    "userCenterBirthDay": "1988.08.01",
    "userCenterTid": "117120189",
    "userCenterUrl": "http:\/\/uc.huan.tv\/avatar\/543079336\/1501676810416.png"
  },
  "appInfos": [
    {
      "appBasic": {
        "userId": "584f9c5bab31fb1d59e138e1",
        "projectId": "24cbd0d8a3f6447ea9153058f53efc7b",
        "channel": "TCL_APPSTORE",
        "packageNm": "com.tcl.article.news",
        "appNm": "今日头条",
        "appVersionName": "9.0.01",
        "appVersionCode": "9006"
      },
      "dataInfos": [
        {
          "type": "3J6DFCL4U1",
          "videoId": "6901585a64594a0e8f8398176a2test1",
          "count": "1",
          "videoName": "帅哥抛弃小伙伴偷偷去相亲，小伙伴们不能忍必须要跟他一决高                                                                                                                                                             下",
          "categoryId": "3"
        },
        {
          "type": "3J6DFCL4U1",
          "videoId": "6901585a64594a0e8f8398176a2test2",
          "count": "1",
          "videoName": "文飞Test",
          "categoryId": "6"
        }
      ]
    }
  ]
}

self.mutex = threading.Lock()

def add_mutex(func):
    def decor(*args, **kwargs):
        time.sleep(1)
        self.mutex.acquire()
        func(*args, **kwargs)
        self.mutex.release()
    return decor

@add_mutex
def safe_print(content):
    print content

def post(url,postData):
    request = urllib2.Request(url,postData)
    request.add_header('Content-Encoding', 'gzip')
    response = urllib2.urlopen(request)
    return response.read()

def gzip_compress(raw_data):
    buf = StringIO()
    f = gzip.GzipFile(mode='wb', fileobj=buf)
    try:
        f.write(raw_data)
    finally:
        f.close()
    return buf.getvalue()


def worker(n):
    url = 'http://192.168.10.100/report/customSecond'
    jsonData = json.dumps(bodyData)
    compressedstream = gzip_compress("sendInfos="+jsonData)
    for i in xrange(n):
        post(url,compressedstream)
        safe_print(str(i)+'Worker has done!')


if __name__ == '__main__':
    #url = 'http://124.251.43.48/report/customSecond'
    #jsonData = json.dumps(bodyData)
    #compressedstream = gzip_compress("sendInfos="+jsonData)

    p_list = []
    for i in xrange(10):
        p1 = Process(target = worker, args = (100000,))
        p_list.append(p1)
        p1.daemon = True

    for p in p_list:
        p.start()

    for p in p_list:
        p.join()
    #print compressedstream
    #print type(jsonData),jsonData
    #reponse_data = post(url,compressedstream)
    #print reponse_data
#     for i in xrange(1):
#         result = post(url,compressedstream)
#         result = requests.post(url, files=compressedstream)
#         print i,result.content
