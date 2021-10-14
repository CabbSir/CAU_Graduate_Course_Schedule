import time

import requests
from bs4 import BeautifulSoup

if __name__ == '__main__':
    url = 'http://gradinfo.cau.edu.cn/stuelectcourse/listCourse.do'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh,zh-CN;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Length': '157',
        'Cookie': "JSESSIONID=527EAE926B5C325F2B3CDE668FC01A9C.TA1",
        'Host': 'gradinfo.cau.edu.cn',
        'Origin': 'http://gradinfo.cau.edu.cn',
        'Referer': 'http://gradinfo.cau.edu.cn/stuelectcourse/preQueryCourse.do?groupId=&moduleId=24104',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36'
    }

    data = {
        'paging_action': 'paging',
        'depid': '1',
        'coursecode': "科技摄影与美学实践",
        'teacher': '',
        'courseSort': '',
        'week': '',
        'section': ''
    }
    ret = requests.post(url, data, headers = headers)
    soup = BeautifulSoup(ret.text, "html.parser")
    table = soup.body.table
    trs = table.find_all('tr')
    del trs[0]
    del trs[0]
    del trs[0]
    # 确认课程条目
    for tr in trs:
        tds = tr.find_all('td')
        no = tds[0].get_text(strip = True)
        class_no = tds[2].get_text(strip = True)
        # 确定是这个，入库
        classroom = tds[9].get_text(strip = True)
        create_time = int(time.time())
        modify_time = int(time.time())
        # 先生成列表
        for time_list in tds[11].get_text(strip = True).split("。")[0].split("；"):
            week = time_list.split('：')[0]
            t_list = time_list.split('：')[1].split('，')
            for t in t_list:
                weekday = t[0: 2]
                class_start = t[2]
                class_end = t[4]
                print(weekday + ' ' + class_start + ' ' + class_end)
