import requests
import execjs  # 这个库是PyExecJS
import re
import random
import time
import os
# print(execjs.get().name)  查看node版本
user_agent_list = [
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) \
    Ubuntu Chromium/81.0.4044.138 Chrome/81.0.4044.138 Safari/537.36',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv,2.0.1) Gecko/20100101 Firefox/4.0.1',
    'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; \
    SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) \
Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
]

base = os.path.dirname(os.path.abspath(__file__))
print(os.path.abspath(__file__))


def get_content(start, key_word):
    base_url = 'https://search.douban.com/movie/subject_search'
    headers = {
        'User-Agent': random.choice(user_agent_list),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,\
                            image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    }
    response = requests.get(base_url, headers=headers, params={'search_text': key_word, 'start': start})
    # print(type(response.text),response.text)
    r = re.findall('window.__DATA__ = "(.+?)"', response.text)[0]
    # print(r)
    # .group(1)  # 加密的数据
    # 导入js
    time.sleep(1)
    with open(base+'/main.js', 'r', encoding='gbk') as f:
        decrypt_js = f.read()
    ctx = execjs.compile(decrypt_js)
# data是所需的数据，将每项数据按字典存储
    data = ctx.call('decrypt', r)['payload']['items']
    print(data)
    if data is False:
        return False
    return data


def detail_data(data):
    print(data)
    result = []
    for item in data:
        temp = []
        if item['tpl_name'] == 'search_subject':
            temp.append(item['title'])
            temp.append(item['url'])
            temp.append('演职表：' + item['abstract_2'])
            temp.append('概括：' + item['abstract'])
            temp.append('评分：'+str(item['rating']['value']))
            result.append(temp)
    return result


