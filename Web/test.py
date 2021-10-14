import time

import requests
from bs4 import BeautifulSoup

if __name__ == '__main__':
    cookie = "JSESSIONID=F4D50C6F468B7B24CD69C94F741E0700.TA1"
    url = "http://gradinfo.cau.edu.cn/j_acegi_security_check;jsessionid=" + cookie
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh,zh-CN;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Length': '93',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': cookie,
        'Host': 'gradinfo.cau.edu.cn',
        'Origin': 'http://gradinfo.cau.edu.cn',
        'Referer': 'http://gradinfo.cau.edu.cn/index.do',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36'
    }
    data = {
        'j_username': "SY20213213219",
        'j_password': "e4c4cb223079bafa59e4a4b8c8a1a4bc",
        'j_captcha': "02314",
        'groupId': ''
    }
    ret = requests.post(url, data, headers = headers)
    print(ret.history[0].headers['Set-Cookie'].split(';')[0])