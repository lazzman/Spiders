#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests
from pyquery import PyQuery as pq
from multiprocessing import Pool
from requests.exceptions import RequestException
import json
from config import *
from lxml import etree

# 会话
session = requests.Session()
cookies = {"PHPSESSID": PHPSESSID}

def checkSession():
    '''
    校验session是否有效
    :return: true有效 false无效
    '''
    session.get(CHECKURL,cookies=cookies)


def crawlVideoList(courseUrl):
    """
    爬取课程页面视频列表
    :param courseUrl: 课程页面网址 例如：http://vip.qiyikt.com/course/415
    """
    try:
        ratio = 0
        everyPageNum = 24
        videoPageList = []
        print('抓取程页面视频列表开始...')
        while (1):
            url = courseUrl + '/tasks/paging?offsetSeq=' + str(1 + ratio * everyPageNum)
            response = session.get(url, cookies=cookies)
            if response.status_code == 200:
                resultList = parseVideoList(response.text)
                videoPageList.extend(resultList)
                if len(resultList) < 1:
                    print('抓取程页面视频列表完成...')
                    break
                ratio = ratio + 1
        print('多进程抓取视频地址开始...')
        print(videoPageSet)
    except RequestException:
        print('抓取课程页面视频列表解析失败...')
    except Exception as err:
        print(err)


def parseVideoList(htmlText):
    '''
    解析课程页面视频列表详细视频网址
    :param htmlText: 课程页面HTML
    :return 视频地址数组
    '''
    doc = pq(etree.fromstring(htmlText))
    lis = doc("div.course-detail-content > ul > li > a.title")
    # 视频地址数组
    resultList = []
    flag = 0
    for li in lis.items():
        result = {"title": li.text(), "href": ADDRESSPRE + li.attr("href")}
        resultList.append(result)
    return resultList


if __name__ == '__main__':
    crawlVideoList("http://vip.qiyikt.com/course/415")
