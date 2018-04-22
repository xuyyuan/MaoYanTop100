import requests
import re
from requests.exceptions import RequestException
import json
from multiprocessing import Pool

def get_one_page(url):
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    }
    try:
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            return res.text
        return None
    except RequestException:
        return None

def parse_one_page(html):
    pattern = re.compile(r'<dd>.*?board-index.*?">(.*?)</i>'
                         +r'.*?poster-default.*?">.*?src="(.*?)"'
                         + r'.*?name">.*?">(.*?)</a>'
                         + r'.*?star">(.*?)</p>'
                         + r'.*?releasetime">(.*?)</p>'
                         + r'.*?integer">(.*?)</i>'
                         + r'.*?fraction">(\d+)</i>.*?</dd>', re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield {
            'index':item[0],
            'image':item[1],
            'name':item[2],
            'star':item[3].strip()[3:],
            'releasetime':item[4][5:],
            'score':item[5]+item[6]
        }

def save_to_file(content):
    with open('result2.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')

def main(page):
    url = 'http://maoyan.com/board/4?offset=' + str(page*10)
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        save_to_file(item)

if __name__ == "__main__":
    # for i in range(10):
    #     main(i)
    pool = Pool()
    pool.map(main, [i for i in range(10)])

