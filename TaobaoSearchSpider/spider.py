#!/usr/local/bin/python
# coding: utf-8
import os
from hashlib import md5
import pymongo
import requests
from pyquery import PyQuery as pq
from requests import RequestException
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from TaobaoSearchSpider.config import *

browser = webdriver.PhantomJS(service_args=PHANTOM_ARGS)
browser.set_window_size(1400, 900)  # 设置窗口大小，否则PhantomJS会出问题
wait = WebDriverWait(browser, 10)
current_page = 1
input_keyword = ''

# 初始化pymongo
client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]


def search(keyword):
    '''
    进入淘宝主页搜索指定关键字
    :param keyword: 
    :return: 
    '''
    try:
        # browser.get("https://www.baidu.com")
        browser.get("https://www.taobao.com/")
        print('初始化加载淘宝首页...')
        search_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#q')))  # 搜索输入框
        search_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.btn-search')))  # 搜索按钮
        search_input.send_keys(keyword)  # 输入关键字
        search_button.click()  # 点击搜索
        total_page = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, '#J_relative > div.sort-row > div > div.pager > ul > li:nth-child(2)')))
        print('搜索', keyword, '成功，当前位于搜素结果第', total_page.text.split('/')[0], '页，结果共计', total_page.text.split('/')[1],
              '页')
        get_products()
        return total_page.text.split('/')[1]

    except TimeoutException:
        print("加载页面超时，url：", "https://www.taobao.com/")
        search(keyword)
        # except WebDriverException:
        #     print("加载页面失败，url：", "https://www.taobao.com/", '正在重试')
        #     search(keyword)


def nextPage():
    '''
    跳转到下一页
    :return: 
    '''
    try:
        global current_page
        # 获取当前页码
        current_page = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, '#J_relative > div.sort-row > div > div.pager > ul > li:nth-child(2) > span'))).text
        print('目前页码：', current_page, '正在跳转到下一页')
        next_button = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '#J_relative > div.sort-row > div > div.pager > ul > li:nth-child(3) > a')))  # 下一页按钮
        next_button.click()
        current_page = str(int(current_page) + 1)  # 页码+1
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,
                                                     '#J_relative > div.sort-row > div > div.pager > ul > li:nth-child(2) > span'
                                                     ), current_page))
        print('跳转到下一页成功，当前页码：', current_page)
        get_products()
    except TimeoutException:
        print("加载页面超时，url：", browser.current_url, '当前页码：', current_page)
        nextPage()
    except TimeoutError:
        print("加载页面超时，url：", browser.current_url, '当前页码：', current_page)
        nextPage()


def get_products():
    '''
    获取商品详情
    :return: 
    '''
    # 等待商品列表加载完毕
    # wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#mainsrp-itemlist .items .item')))

    print('开始获取商品详情...')
    # 让页面从上滚动到下，加载所有的图片
    i_iter = [i * 50 for i in range(120)]
    for i in enumerate(i_iter):
        browser.execute_script('window.scrollTo(0,' + str(i) + ')')
    # 页面滚动到最上面
    browser.execute_script('window.scrollTo(0, 0)')
    html = browser.page_source
    doc = pq(html)
    # 注意写法(去除淘宝广告商品)
    items = doc('#mainsrp-itemlist .items .item.J_MouserOnverReq').items()

    for item in items:
        if item.find('.pic .img').attr('src') == '//g.alicdn.com/s.gif':
            print('页面还没加载完！！！等等。。。')
            return get_products()
        product = {
            'image': item.find('.pic .img').attr('src'),
            'price': item.find('.ctx-box .price').text()[2:],
            'deal_cnt': item.find('.deal-cnt').text()[:-3],
            'title': item.find('.title').text(),
            'shop_name': item.find('.shop').text(),
            'location': item.find('.location').text()
        }
        # 保存到mongo
        save_to_mongo(product)
        # 下载商品图片（淘宝的图片前面没有协议头，需要自己添加）
        download_save_image('http:' + product['image'])


def save_to_mongo(result):
    '''
    将数据存储到MongoDB中
    :param result: Json格式的数据
    :return: 
    '''
    try:
        if db[MONGO_TABLE + '_' + input_keyword].insert(result):
            print('存储成功...', result)
    except Exception:
        print('存储失败...', result)


def download_save_image(url):
    '''
    下载商品图片保存到本地
    :param url: 
    :return: 
    '''
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # 如果images文件夹不存在，则创建images文件夹
            dirpath = os.getcwd() + '/images_' + input_keyword
            if not os.path.exists(dirpath):
                os.makedirs(dirpath)
            filePath = '{0}/{1}.{2}'.format(os.getcwd() + '/images_' + input_keyword,
                                            md5(url.encode('utf-8')).hexdigest(), 'jpg')
            if not os.path.exists(filePath):
                with open(filePath, 'wb') as f:
                    f.write(response.content)
                print('保存图片完毕...')
    except RequestException:
        print('下载图片失败，图片URL：', url)


def main():
    '''
    程序主方法
    :return: 
    '''
    try:
        global input_keyword
        input_keyword = input('输入搜索的商品名称：')
        search(input_keyword)
        print('搜索完毕，开始遍历搜索结果页...')
        # 从第2页开始获取后面9页的内容
        for i in range(9):
            nextPage()

    finally:
        browser.close()


if __name__ == '__main__':
    main()
