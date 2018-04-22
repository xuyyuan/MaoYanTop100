# coding=utf-8
# author: xuyyuan time: 2018/4/10

import requests
import re
from requests.exceptions import RequestException
import json
from multiprocessing import Pool # 引入一个进程池，实现秒抓，多进程

def get_one_page(url):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
    # res = requests.get(url, headers=headers).text
    # return res
    try:
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            return res.text
        return None
    except RequestException:
        return None

def parse_one_page(html):
     pattern = re.compile(r'<dd>.*?board-index.*?">(.*?)</i>' #可以写成\d+
                          +r'.*?src.*?">.*?src="(.*?)"'
                         +r'.*?name".*?">(.*?)</a>'
                         +r'.*?star">(.*?)</p>'
                         +r'.*?releasetime">(.*?)</p>'
                         +r'.*?integer">(.*?)</i>'     # 不能写成\d+     !!!!!!!
                         +'.*?fraction">(.*?)</i>.*?</dd>', re.S) #可以写成\d+
     items = re.findall(pattern, html)
     # print(items)
     for item in items:
         yield {
             'index':item[0],
             'image':item[1],
             'name':item[2],
             'star':item[3].strip()[3:],
             'releasetime':item[4].strip()[5:],
             'score':item[5]+item[6]
         }
     # 生成器的知识要巩固下
     # 注意图片的链接scr或者scr-data不知道用怎样的正则表达式!!!!!!!!!!
def save_to_file(content):
    with open('result.txt', 'a',encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n' )
    # content是字典的形式，我们需要用json.dumps将其转换为字符串
    # 换行符最好加上
    #json.dumps()
    #open里面的encoding和json.dumps里面的参数要加上ensure_assic=False 这样才能保证中文正常写入

def main(offset):
    url = 'http://maoyan.com/board/4?offset=' + str(offset*10)
    html = get_one_page(url)
    # print(html)
    for item in parse_one_page(html):
        print(item)
        save_to_file(item)

if __name__ == '__main__':
    for i in range(10):
        main(i)
    # pool = Pool()
    # pool.map(main, [i for i in range(10)])

