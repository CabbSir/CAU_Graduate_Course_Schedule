import base64

import requests

if __name__ == '__main__':
    url = "http://gradinfo.cau.edu.cn/"
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh',
        'Host': 'gradinfo.cau.edu.cn',
        'Proxy-Connection': 'keep - alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
    }
    ret = requests.get(url, headers = headers, allow_redirects = False)
    cookie = ret.headers.get('Set-Cookie').split(';')[0]
    url = 'http://gradinfo.cau.edu.cn/getCaptcha.do'
    headers = {
        'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh,zh-CN;q=0.9',
        'Connection': 'keep-alive',
        'Cookie': cookie,
        'Host': 'gradinfo.cau.edu.cn',
        'Referer': 'http://gradinfo.cau.edu.cn/index.do',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
    }
    ret = requests.get(url, headers=headers)
    base64_data = base64.b64encode(ret.content)
    print("data:image/png;base64," + str(base64_data, encoding = "utf-8"))