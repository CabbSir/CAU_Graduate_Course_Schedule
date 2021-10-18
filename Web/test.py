import calendar
from datetime import datetime, timedelta
import re
import time

import requests
from bs4 import BeautifulSoup


def get_season():
    url = 'http://gradinfo.cau.edu.cn/calendar/index.do?groupId=&moduleId=28001'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh,zh-CN;q=0.9',
        'Connection': 'keep-alive',
        'Cookie': 'JSESSIONID=A26DBFB9E98A92267C64C666352B03F5.TA1',
        'Host': 'gradinfo.cau.edu.cn',
        'Referer': 'http://gradinfo.cau.edu.cn/listLeft.do?',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
    }
    ret = requests.get(url, headers = headers)
    soup = BeautifulSoup(ret.text, "html.parser")
    table = soup.body.table
    trs = table.find_all('tr')
    del (trs[0])
    total_num = len(trs)
    i = 0
    for tr in trs:
        i += 1
        tds = tr.find_all('td')
        year = tds[0].get_text(strip = True)
        season = 1 if tds[1].get_text(strip = True) == '春' else 2
        begin_date = tds[2].get_text(strip = True)
        total_weeks = tds[3].get_text(strip = True)
        is_now = 1 if i == total_num else 2
        now = int(time.time())


def build_calendar():
    print(datetime.today().strftime("%Y-%m-%d"))

def str_function():
    str_list = [
        '第8周：周一1-4节，周二5-8节，周五1-4节，周六1-4节上课；第9周：周一9-12节，周二5-8节，周五5-8节，周六9-12节上课。',
        '第13周：周四1-4节，周五1-3节上课；第14周：周一1-4节，周二1-4节，周四1-4节，周五1-3节上课；第15周：周一1-4节，周二1-4节，周三1-4节，周四1-4节上课。',
        '第7周：周一5-8节，周二1-4节，周三5-8节上课；第8周：周一5-8节，周三5-8节上课；第10周：周一1-4节，周二5-8节，周三1-4节，周四1-4节上课。',
        '11-12周：周六1-4，周日1-4；13-14周：周三1-4，周六1-4；15周：周六1-4，周日1-4。资源与环境专业（土院，资环学院），土木水利专业，能源动力专业，电子信息专业的同学必选.',
        '第5周：周五9-11节，周六5-8节，周日5-8节，9-11节上课；第6周：周一1-4节，周二9-12节上课。'
    ]

    for s in str_list:
        resource_str = s.split('。')[0]  # 首先用句号分割正文
        # 然后用；分割周次
        weeks = resource_str.split('；')
        for week in weeks:
            # 用冒号分割天数
            week_str = week.split('：')[0]
            week_str = week_str.replace('第', '').replace('周', '')
            if week_str.find('-') != -1:
                begin = week_str.split('-')[0]
                end = week_str.split('-')[1]
                week_list = []
                for i in range(int(begin), int(end) + 1):
                    week_list.append(i)
            else:
                week_list = [week_str]
            days = week.split('：')[1]
            # 分割days,
            for w in week_list:
                week_str = str(w)
                last_week_day = ''
                for day in days.split('，'):
                    if day[0] == '周':
                        weekday = day[0: 2]
                        last_week_day = weekday
                    else:
                        weekday = last_week_day
                    hour_begin = re.findall('\d+', day.split('-')[0])[0]
                    hour_end = re.findall('\d+', day.split('-')[1])[0]
                    print(week_str + " " + weekday + " " + hour_begin + " " + hour_end)
        print('——————————————————————————————')


# 处理字符串的方法，

if __name__ == '__main__':
    build_calendar()
