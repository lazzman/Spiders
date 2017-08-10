#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests
import re
from multiprocessing import Pool
from requests.exceptions import RequestException
import json

'''
Created on 2017年5月15日

@author: NodCat
'''

def get_one_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

def parse_one_page(html):
    pattern = re.compile(r'<dd>.*?<i.*?class="board-index.*?">(\d+)</i>.*?data-src="(.*?)".*?title.*?data-act.*?data-val.*?">(.*?)</a></p>.*?class="star">(.*?)</p>.*?releasetime">(.*?)</p>.*?integer">(.*?)</i>.*?fraction">(\d+)</i></p>', re.RegexFlag.S)
    items = re.findall(pattern, html)
    for item in items:
        yield {
            'index':item[0],
            'image':item[1],
            'title':item[2],
            'star':re.sub('\s', '', item[3])[3:],  # 使用正则替换所有空白字符
            'time':item[4].strip()[5:],
            'score':item[5] + item[6]
        }

def write_to_file(content):
    with open("result.txt", 'a' , encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')
   
def main(offset):
    url = 'http://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        write_to_file(item)


if __name__ == '__main__':
    pool = Pool()
    pool.map(main, [i * 10 for i in range(10)])


