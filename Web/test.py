import requests
from bs4 import BeautifulSoup

if __name__ == '__main__':
    url = 'http://gradinfo.cau.edu.cn/studentschedule/showStudentSchedule.do?groupId=&moduleId=20101'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh,zh-CN;q=0.9',
        'Cookie': 'JSESSIONID=07DB6B25516F0D3EA565429FFC88DD31.TA2',
        'Host': 'gradinfo.cau.edu.cn',
        'Referer': 'http://gradinfo.cau.edu.cn/index.do',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36'
    }
    ret = requests.get(url, headers = headers)
    soup = BeautifulSoup(ret.text, "html.parser")
    table = soup.body.table
    trs = table.find_all('tr')
    for tr in trs:
        for td in tr.find_all('td'):
            print(td.get_text(strip=True), end='')
            print(" ")