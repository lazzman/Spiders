#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests
from pyquery import PyQuery as pq
from multiprocessing import Pool
from requests.exceptions import RequestException
import json
from config import *

# 会话
session = requests.Session()
cookies = {"PHPSESSID": PHPSESSID}

def crawlVideoList(courseUrl):
    """
    爬取课程页面视频列表
    :param courseUrl: 课程页面网址 例如：http://vip.qiyikt.com/my/course/415
    """
    try:
        print('抓取程页面视频列表开始...')
        response = session.get(courseUrl,cookies=cookies)
        if response.status_code == 200:
            print('抓取程页面视频列表完成...')
            print(response.text)
            print('多进程抓取视频地址开始...')
    except RequestException:
        print('抓取课程页面视频列表解析失败...')


def parseVideoList(htmlText):
    '''
    解析课程页面视频列表详细视频网址
    :param htmlText: 课程页面HTML
    '''



if __name__ == '__main__':
    crawlVideoList("http://vip.qiyikt.com/my/course/415")